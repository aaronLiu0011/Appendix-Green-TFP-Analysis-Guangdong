# Private-panel compatibility test

The repository was tested against the private balanced panel without copying that panel or any calculated values into the release.

| Method | Requested city-year transitions | Invalid transitions | Conclusion |
| --- | ---: | ---: | --- |
| Classical CFG Malmquist–Luenberger | 378 | 105 | Not suitable as the sole production run for this panel |
| APZ Malmquist–Luenberger | 378 | 18 | Better feasibility, but still incomplete |
| Global Malmquist–Luenberger | 378 | 0 | Complete open re-estimation route |
| Ordinary four-distance SBM | 378 | Stops at the first infeasible cross-period program | Useful as an equation audit, not as the default production route |

Synthetic unit tests verify the ordinary SBM linearization and the multiplicative identity `GTFP = EC × TC`. The private-panel check verifies executable compatibility only. It does not establish equality with the archived MaxDEA values.
