"""Linear-programming implementation of a non-oriented undesirable-output SBM."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class SBMResult:
    score: float
    intensity: np.ndarray
    input_slack: np.ndarray
    desirable_slack: np.ndarray
    undesirable_slack: np.ndarray
    scale: float


def _positive_vector(values: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=float).reshape(-1)
    if array.size == 0 or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain finite values")
    if np.any(array <= 0):
        raise ValueError(f"{name} must be strictly positive")
    return array


def _reference_matrix(values: np.ndarray, rows: int, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 2 or array.shape[0] != rows or array.shape[1] == 0:
        raise ValueError(f"{name} must have shape ({rows}, number_of_reference_dmus)")
    if not np.all(np.isfinite(array)) or np.any(array <= 0):
        raise ValueError(f"{name} must contain finite, strictly positive values")
    return array


def solve_sbm(
    x: np.ndarray,
    y: np.ndarray,
    bad: np.ndarray,
    reference_x: np.ndarray,
    reference_y: np.ndarray,
    reference_bad: np.ndarray,
    *,
    returns_to_scale: str = "crs",
    tolerance: float = 1e-8,
) -> SBMResult:
    """Evaluate one observation against a reference technology.

    The fractional SBM is converted to a linear program with the
    Charnes-Cooper transformation and solved by SciPy/HiGHS. Reference
    matrices have variables in rows and reference DMUs in columns.
    """

    x = _positive_vector(x, "x")
    y = _positive_vector(y, "y")
    bad = _positive_vector(bad, "bad")
    reference_x = _reference_matrix(reference_x, x.size, "reference_x")
    reference_y = _reference_matrix(reference_y, y.size, "reference_y")
    reference_bad = _reference_matrix(reference_bad, bad.size, "reference_bad")
    reference_count = reference_x.shape[1]
    if reference_y.shape[1] != reference_count or reference_bad.shape[1] != reference_count:
        raise ValueError("all reference matrices must contain the same number of DMUs")
    if returns_to_scale not in {"crs", "vrs"}:
        raise ValueError("returns_to_scale must be 'crs' or 'vrs'")

    n_input, n_good, n_bad = x.size, y.size, bad.size
    i_lambda = slice(0, reference_count)
    i_sx = slice(i_lambda.stop, i_lambda.stop + n_input)
    i_sy = slice(i_sx.stop, i_sx.stop + n_good)
    i_sb = slice(i_sy.stop, i_sy.stop + n_bad)
    i_tau = i_sb.stop
    variable_count = i_tau + 1

    objective = np.zeros(variable_count)
    objective[i_sx] = -(1.0 / n_input) / x
    objective[i_tau] = 1.0
    rows: list[np.ndarray] = []
    rhs: list[float] = []

    for j in range(n_input):
        row = np.zeros(variable_count)
        row[i_lambda] = reference_x[j]
        row[i_sx.start + j] = 1.0
        row[i_tau] = -x[j]
        rows.append(row)
        rhs.append(0.0)
    for j in range(n_good):
        row = np.zeros(variable_count)
        row[i_lambda] = reference_y[j]
        row[i_sy.start + j] = -1.0
        row[i_tau] = -y[j]
        rows.append(row)
        rhs.append(0.0)
    for j in range(n_bad):
        row = np.zeros(variable_count)
        row[i_lambda] = reference_bad[j]
        row[i_sb.start + j] = 1.0
        row[i_tau] = -bad[j]
        rows.append(row)
        rhs.append(0.0)

    normalization = np.zeros(variable_count)
    output_count = n_good + n_bad
    normalization[i_sy] = (1.0 / output_count) / y
    normalization[i_sb] = (1.0 / output_count) / bad
    normalization[i_tau] = 1.0
    rows.append(normalization)
    rhs.append(1.0)

    if returns_to_scale == "vrs":
        row = np.zeros(variable_count)
        row[i_lambda] = 1.0
        row[i_tau] = -1.0
        rows.append(row)
        rhs.append(0.0)

    result = linprog(
        objective,
        A_eq=np.vstack(rows),
        b_eq=np.asarray(rhs),
        bounds=[(0.0, None)] * variable_count,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"SBM optimization failed: {result.message}")
    tau = float(result.x[i_tau])
    if tau <= tolerance:
        raise RuntimeError("SBM optimization returned a non-positive scaling variable")
    score = float(result.fun)
    if abs(score) < tolerance:
        score = 0.0
    return SBMResult(
        score=score,
        intensity=result.x[i_lambda] / tau,
        input_slack=result.x[i_sx] / tau,
        desirable_slack=result.x[i_sy] / tau,
        undesirable_slack=result.x[i_sb] / tau,
        scale=tau,
    )
