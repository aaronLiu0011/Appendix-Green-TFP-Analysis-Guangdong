# GTFP calculation method

## Variables

Each city-year is a decision-making unit. The study uses three inputs, one desirable output, and one undesirable output.

| Role | Variable | Construction |
| --- | --- | --- |
| Input | Real capital stock | Perpetual inventory method; 9.6% depreciation; initial stock equal to 2000 real investment divided by 0.10 |
| Input | Labor | Total employment, smoothed with a two-year moving average |
| Input | Energy | Total electricity consumption |
| Desirable output | Real GDP | Constant 2000 prices |
| Undesirable output | CO2 emissions | City-level apparent emissions estimate |

No empirical values are distributed here.

## Ordinary undesirable-output SBM stated in the paper

Under CRS, the period technology satisfies

```text
X lambda <= x
Y lambda >= y
B lambda <= b
lambda >= 0.
```

For evaluated observation `o`, the non-oriented score is

```text
                 1 - (1/N) sum_n (sx_n / x_no)
rho = min  -------------------------------------------------
             1 + (1/(M+I)) [sum_m (sy_m / y_mo)
                              + sum_i (sb_i / b_io)]
```

subject to

```text
X lambda + sx = x_o
Y lambda - sy = y_o
B lambda + sb = b_o
lambda, sx, sy, sb >= 0.
```

`model.py` applies the Charnes–Cooper transformation and solves this program with SciPy/HiGHS.

## Four-distance productivity account

If all four scores exist, the adjacent-period index is

```text
GTFP(t,t+1) = sqrt([S^t(z_t+1) / S^t(z_t)]
                   [S^(t+1)(z_t+1) / S^(t+1)(z_t)])

EC(t,t+1) = S^(t+1)(z_t+1) / S^t(z_t)

TC(t,t+1) = sqrt([S^t(z_t+1) / S^(t+1)(z_t+1)]
                  [S^t(z_t) / S^(t+1)(z_t)])

GTFP = EC * TC.
```

Values above one indicate improvement, one indicates no change, and values below one indicate deterioration.

## Recommended open specification

The recommended replacement is `global-ml`, a global Malmquist–Luenberger index based on a CRS environmental directional-distance technology. A common global reference technology makes the index circular and avoids the cross-period infeasibility found in the classical four-distance specification.

This is a methodological revision, not an exact reconstruction of the archived MaxDEA SBM/super-efficiency run. It requires recalculating descriptive statistics, regional comparisons, and regressions if used in the paper.

## Frontier terminology

- `contemporaneous`: each year's observations define that year's frontier.
- `sequential`: period `t` pools all observations dated no later than `t`.
- `global`: one common technology pools all periods.

The paper says “sequential DEA,” but the preserved MaxDEA summary only confirms “Adjacent” Malmquist. Treat the original frontier mode as unresolved.
