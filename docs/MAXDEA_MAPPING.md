# Archived MaxDEA audit and open mapping

| Archived evidence | Interpretation | Open treatment |
| --- | --- | --- |
| Maximum Distance to Frontier / SBM | Non-radial SBM, not the directional-distance setting required for the classical ML index in the MaxDEA manual | `sbm-ml` implements the ordinary stated SBM; `global-ml` uses a documented directional-distance method |
| Nonoriented | Inputs, desirable output, and undesirable output are improved jointly | Ordinary SBM is non-oriented; environmental ML uses its source-qualified output direction |
| Undesirable output: CO2 | CO2 is not a desirable service output | Explicit bad-output role in every method |
| SuperEfficiency | Efficient and cross-period scores can exceed one | Archived output is preserved as evidence; no undocumented clone is attempted |
| Adjacent, mean of two indices, multiplicative and geometric mean | Four-distance adjacent-period productivity account | Implemented by `cfg-ml`, `apz-ml`, and `sbm-ml`; the global method uses its documented common-reference account |
| CRS output used in the paper | Constant returns to scale | Fixed by the environmental ML presets and selectable in `sbm-ml` |
| Paper says sequential DEA | The period technology may have accumulated historical observations | Supported only as an audit option in `sbm-ml`; not confirmed by the archived summary |

## Why exact replication is not claimed

The archived current-period scores include values above one, so super-efficiency was active. Ordinary SBM scores are bounded by one when each observation belongs to its own reference set. Combining undesirable-output SBM, super-efficiency, cross-period evaluation, and MaxDEA's infeasibility conventions requires details not preserved in the summary workbook.

MaxDEA's manual also distinguishes “Maximum Distance to Frontier / SBM” from “Directional Distance.” It instructs users to select Directional Distance for a Malmquist–Luenberger index with undesirable outputs. The archived run therefore should be described as a super-efficiency SBM Malmquist calculation, not automatically relabeled as a classical Chung–Färe–Grosskopf ML index.

## Publication choices

1. **Keep the published numbers.** Label them as archived MaxDEA super-efficiency SBM Malmquist results. Publish the open code as a methodological audit and do not claim exact replication.
2. **Adopt the open method.** Use `global-ml`, regenerate all GTFP values and downstream tables, and revise the method section.
3. **Recover exact replication later.** Obtain the original MaxDEA project or fully document the exact super-SBM cross-period program, then add an independently tested compatibility mode.
