"""Direct SBM four-distance Malmquist calculation."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

from .model import solve_sbm


def _frontier_rows(panel: pd.DataFrame, period_column: str, period: object, mode: str) -> pd.DataFrame:
    if mode == "contemporaneous":
        return panel.loc[panel[period_column] == period]
    if mode == "sequential":
        return panel.loc[panel[period_column] <= period]
    raise ValueError("frontier must be 'contemporaneous' or 'sequential'")


def _score(row, reference, input_columns, desirable_columns, undesirable_columns, returns_to_scale):
    return solve_sbm(
        row[list(input_columns)].to_numpy(dtype=float),
        row[list(desirable_columns)].to_numpy(dtype=float),
        row[list(undesirable_columns)].to_numpy(dtype=float),
        reference[list(input_columns)].to_numpy(dtype=float).T,
        reference[list(desirable_columns)].to_numpy(dtype=float).T,
        reference[list(undesirable_columns)].to_numpy(dtype=float).T,
        returns_to_scale=returns_to_scale,
    ).score


def calculate_malmquist_panel(
    panel: pd.DataFrame,
    *,
    period_column: str = "period",
    dmu_column: str = "dmu",
    input_columns: Sequence[str] = ("capital", "labor", "energy"),
    desirable_columns: Sequence[str] = ("desirable_output",),
    undesirable_columns: Sequence[str] = ("undesirable_output",),
    frontier: str = "contemporaneous",
    returns_to_scale: str = "crs",
    identity_tolerance: float = 1e-7,
) -> pd.DataFrame:
    """Calculate the stated SBM index; fail visibly on infeasible cross distances."""

    columns = [period_column, dmu_column, *input_columns, *desirable_columns, *undesirable_columns]
    missing = [column for column in columns if column not in panel.columns]
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    if panel.duplicated([period_column, dmu_column]).any():
        raise ValueError("each period-DMU pair must be unique")
    work = panel[columns].copy()
    numeric_columns = [*input_columns, *desirable_columns, *undesirable_columns]
    work[numeric_columns] = work[numeric_columns].apply(pd.to_numeric, errors="raise")
    values = work[numeric_columns].to_numpy(dtype=float)
    if not np.all(np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("all input and output values must be finite and strictly positive")

    periods = sorted(work[period_column].unique())
    if len(periods) < 2:
        raise ValueError("at least two periods are required")
    output: list[dict[str, object]] = []
    for period_t, period_t1 in zip(periods[:-1], periods[1:]):
        rows_t = work.loc[work[period_column] == period_t].set_index(dmu_column)
        rows_t1 = work.loc[work[period_column] == period_t1].set_index(dmu_column)
        if set(rows_t.index) != set(rows_t1.index):
            raise ValueError(f"DMU membership differs between {period_t!r} and {period_t1!r}")
        frontier_t = _frontier_rows(work, period_column, period_t, frontier)
        frontier_t1 = _frontier_rows(work, period_column, period_t1, frontier)
        for dmu in sorted(rows_t.index, key=str):
            observation_t, observation_t1 = rows_t.loc[dmu], rows_t1.loc[dmu]
            try:
                args = (input_columns, desirable_columns, undesirable_columns, returns_to_scale)
                s_t_t = _score(observation_t, frontier_t, *args)
                s_t_t1 = _score(observation_t1, frontier_t, *args)
                s_t1_t = _score(observation_t, frontier_t1, *args)
                s_t1_t1 = _score(observation_t1, frontier_t1, *args)
            except RuntimeError as error:
                raise RuntimeError(
                    f"distance calculation failed for DMU {dmu!r}, period pair "
                    f"{period_t!r}-{period_t1!r}: {error}"
                ) from error
            scores = np.asarray([s_t_t, s_t_t1, s_t1_t, s_t1_t1])
            if np.any(scores <= 0):
                raise RuntimeError(f"non-positive distance score for DMU {dmu!r}")
            gtfp = float(np.sqrt((s_t_t1 / s_t_t) * (s_t1_t1 / s_t1_t)))
            ec = float(s_t1_t1 / s_t_t)
            tc = float(np.sqrt((s_t_t1 / s_t1_t1) * (s_t_t / s_t1_t)))
            if not np.isclose(gtfp, ec * tc, rtol=identity_tolerance, atol=identity_tolerance):
                raise RuntimeError("ML decomposition identity failed numerical validation")
            output.append({
                period_column: period_t1,
                dmu_column: dmu,
                "reference_period_start": period_t,
                "score_t_at_t": s_t_t,
                "score_t1_at_t": s_t_t1,
                "score_t_at_t1": s_t1_t,
                "score_t1_at_t1": s_t1_t1,
                "gtfp": gtfp,
                "ec": ec,
                "tc": tc,
                "method": "sbm-ml",
                "frontier": frontier,
                "returns_to_scale": returns_to_scale,
            })
    return pd.DataFrame(output)
