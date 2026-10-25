"""Command-line interface for open GTFP calculations."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .malmquist import calculate_malmquist_panel
from .open_methods import calculate_open_ml


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Calculate environmental productivity indices.")
    parser.add_argument("input", type=Path, help="private input panel (.csv or .xlsx)")
    parser.add_argument("output", type=Path, help="output file (.csv or .xlsx)")
    parser.add_argument(
        "--method",
        choices=["global-ml", "cfg-ml", "apz-ml", "sbm-ml"],
        default="global-ml",
        help="global-ml is the complete, infeasibility-resistant default",
    )
    parser.add_argument("--period-column", default="period")
    parser.add_argument("--dmu-column", default="dmu")
    parser.add_argument("--input-columns", nargs="+", default=["capital", "labor", "energy"])
    parser.add_argument("--desirable-columns", nargs="+", default=["desirable_output"])
    parser.add_argument("--undesirable-columns", nargs="+", default=["undesirable_output"])
    parser.add_argument(
        "--frontier",
        choices=["contemporaneous", "sequential"],
        default="contemporaneous",
        help="used only by the direct sbm-ml method",
    )
    parser.add_argument(
        "--returns-to-scale",
        choices=["crs", "vrs"],
        default="crs",
        help="used only by the direct sbm-ml method",
    )
    return parser


def _read(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xlsm"}:
        return pd.read_excel(path)
    raise ValueError("input must be a .csv, .xlsx, or .xlsm file")


def _write(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".csv":
        frame.to_csv(path, index=False)
        return
    if path.suffix.lower() in {".xlsx", ".xlsm"}:
        frame.to_excel(path, index=False)
        return
    raise ValueError("output must be a .csv, .xlsx, or .xlsm file")


def main() -> None:
    args = _parser().parse_args()
    panel = _read(args.input)
    common = {
        "period_column": args.period_column,
        "dmu_column": args.dmu_column,
        "input_columns": args.input_columns,
        "desirable_columns": args.desirable_columns,
        "undesirable_columns": args.undesirable_columns,
    }
    if args.method == "sbm-ml":
        result = calculate_malmquist_panel(
            panel,
            **common,
            frontier=args.frontier,
            returns_to_scale=args.returns_to_scale,
        )
    else:
        result = calculate_open_ml(panel, method=args.method, **common)
    _write(result, args.output)
    invalid = int((~result["score_valid"]).sum()) if "score_valid" in result else 0
    print(f"Wrote {len(result)} DMU-period indices to {args.output}; invalid rows: {invalid}")


if __name__ == "__main__":
    main()
