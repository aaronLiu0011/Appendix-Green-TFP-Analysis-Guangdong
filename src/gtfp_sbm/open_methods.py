"""Audited open-source Malmquist-Luenberger alternatives provided by DEAPack."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from deapack import (
    APZMalmquistLuenbergerDEA,
    DEAData,
    GlobalMalmquistLuenbergerDEA,
    MalmquistLuenbergerDEA,
)


_METHODS = {
    "cfg-ml": MalmquistLuenbergerDEA,
    "apz-ml": APZMalmquistLuenbergerDEA,
    "global-ml": GlobalMalmquistLuenbergerDEA,
}


def calculate_open_ml(
    panel: pd.DataFrame,
    *,
    method: str = "global-ml",
    period_column: str = "period",
    dmu_column: str = "dmu",
    input_columns: Sequence[str] = ("capital", "labor", "energy"),
    desirable_columns: Sequence[str] = ("desirable_output",),
    undesirable_columns: Sequence[str] = ("undesirable_output",),
) -> pd.DataFrame:
    """Calculate a source-qualified environmental productivity index."""

    if method not in _METHODS:
        raise ValueError(f"method must be one of: {', '.join(_METHODS)}")
    data = DEAData.from_frame(
        panel,
        dmu=dmu_column,
        period=period_column,
        inputs=list(input_columns),
        outputs=list(desirable_columns),
        bad_outputs=list(undesirable_columns),
    )
    summary = _METHODS[method]().fit(data).summary()
    concise = summary[
        [
            "period",
            "dmu_id",
            "base_period",
            "productivity_change",
            "efficiency_change",
            "technical_change",
            "score_valid",
            "solver_status",
            "failed_distance_count",
        ]
    ].rename(
        columns={
            "period": period_column,
            "dmu_id": dmu_column,
            "base_period": "reference_period_start",
            "productivity_change": "gtfp",
            "efficiency_change": "ec",
            "technical_change": "tc",
        }
    )
    concise["method"] = method
    return concise
