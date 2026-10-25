# Open GTFP Computation for Guangdong Cities

This code-only repository documents and implements open alternatives for calculating green total factor productivity (GTFP). It intentionally excludes the manuscript, appendix, empirical input data, regression data, and published results.

## What the archived MaxDEA run actually did

The preserved software summary records:

- a non-oriented maximum-distance-to-frontier SBM;
- three inputs and two outputs, with CO2 marked undesirable;
- super-efficiency;
- adjacent-period Malmquist indices;
- multiplicative/geometric-mean aggregation; and
- CRS, VRS, and decomposition output.

The archived scores include values above one, confirming that super-efficiency affected the calculation. This is not the same as the ordinary undesirable-output SBM equation alone. The lost MaxDEA project also leaves the paper's claim of a sequential frontier unverified.

## Open calculation routes

The command offers four explicit methods. None is silently presented as an exact MaxDEA clone.

| Method | Purpose | Expected behavior |
| --- | --- | --- |
| `global-ml` | Recommended open re-estimation using a global Malmquist–Luenberger index and directional distance | Complete and circular; changes the empirical method and therefore the results |
| `cfg-ml` | Classical Chung–Färe–Grosskopf Malmquist–Luenberger index | Can contain infeasible cross-period distances |
| `apz-ml` | Consistency-qualified APZ Malmquist–Luenberger index | Reduces, but may not eliminate, infeasibility |
| `sbm-ml` | Direct implementation of the ordinary non-oriented undesirable-output SBM equations stated in the paper | Transparent, but cross-period programs may be infeasible and it does not reproduce MaxDEA super-efficiency |

The first three routes use the open-source DEAPack implementation. The last route exposes the linear program in this repository and solves it with SciPy/HiGHS.

## Installation

Python 3.10 or newer is recommended.

```bash
python -m pip install -e .
```

## Private input format

Prepare a long-format CSV or Excel file with one row per city and year:

```text
period,dmu,capital,labor,energy,desirable_output,undesirable_output
```

All inputs and outputs must be finite and strictly positive. `examples/input_schema.csv` contains only the header.

## Recommended open re-estimation

```bash
gtfp-sbm private_input.xlsx private_output.csv \
  --method global-ml
```

If the private workbook uses different column labels, map them explicitly:

```bash
gtfp-sbm private_input.xlsx private_output.csv \
  --method global-ml \
  --period-column period \
  --dmu-column city \
  --input-columns capital labor energy \
  --desirable-columns real_gdp \
  --undesirable-columns co2_emissions
```

To audit the ordinary SBM equations stated in the paper:

```bash
gtfp-sbm private_input.xlsx private_sbm_output.csv \
  --method sbm-ml \
  --frontier contemporaneous \
  --returns-to-scale crs
```

The command reports invalid rows instead of filling failed distances or manually overwriting values.

## Repository contents

- `src/gtfp_sbm/model.py`: ordinary undesirable-output SBM linear program.
- `src/gtfp_sbm/malmquist.py`: four-distance SBM index and EC/TC decomposition.
- `src/gtfp_sbm/open_methods.py`: source-qualified open Malmquist–Luenberger alternatives.
- `docs/METHOD.md`: equations, variable construction, and interpretation.
- `docs/DETAILED_METHOD.md`: full theoretical derivation, model distinction, workflow, quality checks, and publication-ready method statements.
- `docs/MAXDEA_MAPPING.md`: archived setting audit and non-equivalence notes.
- `docs/VALIDATION.md`: private-panel compatibility test without publishing data or results.
- `docs/DATA_POLICY.md`: publication boundary.
- `tests/`: synthetic unit tests only.

## Tests

```bash
python -m pytest
```

If the published paper must retain its existing numerical tables, preserve those values as archived MaxDEA results and describe this repository as a transparent open re-estimation workflow. Do not claim exact software replication until the original MaxDEA project or a fully specified super-SBM productivity program is recovered.
