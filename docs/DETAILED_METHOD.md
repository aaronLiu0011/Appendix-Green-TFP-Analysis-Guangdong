# Detailed GTFP Measurement Method

## 1. Scope and methodological decision

This repository separates two related but non-equivalent measurement systems. The theoretical materials describe an environmental production technology evaluated with a directional distance function (DDF) and a Malmquist–Luenberger (ML) productivity index. The archived MaxDEA summary instead records a non-oriented, maximum-distance-to-frontier slacks-based measure (SBM), super-efficiency, and adjacent-period Malmquist aggregation. The archived calculation should therefore be described as a **super-efficiency SBM Malmquist calculation**, not as an exact implementation of the Chung–Fare–Grosskopf DDF–ML index.

Two defensible publication routes follow from this distinction:

1. **Retain the archived numerical results.** Describe them as CRS super-efficiency SBM Malmquist results and present this repository as an open methodological audit. Do not claim exact numerical replication.
2. **Re-estimate GTFP with an open method.** Use the global Malmquist–Luenberger (`global-ml`) implementation, then regenerate every descriptive statistic, regional comparison, figure, and regression that uses GTFP.

The second route is the recommended fully open workflow because the global technology produces a common reference set and avoids the cross-period infeasibility that affects the classical four-distance formulation in this panel.

## 2. Units of analysis and notation

Each prefecture-level city in each year is treated as a decision-making unit (DMU). For city \(i\) in year \(t\), define

$$
z_{i,t}=(x_{i,t},y_{i,t},b_{i,t}),
$$

where

- \(x_{i,t}\in\mathbb{R}_{+}^{N}\) is the input vector;
- \(y_{i,t}\in\mathbb{R}_{+}^{M}\) is the desirable-output vector; and
- \(b_{i,t}\in\mathbb{R}_{+}^{I}\) is the undesirable-output vector.

The Guangdong application uses three inputs (\(N=3\)), one desirable output (\(M=1\)), and one undesirable output (\(I=1\)). The original balanced panel contains 21 cities observed from 2000 through 2018. The first year supplies the base observations, so adjacent-period productivity changes are dated 2001–2018.

## 3. Variable construction

| Role | Variable | Construction | Preferred direction |
| --- | --- | --- | --- |
| Input | Real capital stock | Deflate nominal fixed-asset investment and apply the perpetual inventory method | Less is better |
| Input | Labor | Total employment, smoothed with a two-year moving average | Less is better |
| Input | Energy | Total electricity consumption | Less is better |
| Desirable output | Real GDP | GDP at constant 2000 prices | More is better |
| Undesirable output | Carbon dioxide emissions | City-level apparent CO2 emissions | Less is better |

### 3.1 Capital stock

Real capital stock is constructed with the perpetual inventory method:

$$
K_{i,t}=(1-\delta)K_{i,t-1}+I_{i,t},
\qquad \delta=0.096,
$$

where \(I_{i,t}\) is real fixed-asset investment after price deflation. The original study initializes the series as

$$
K_{i,2000}=\frac{I_{i,2000}}{0.10}.
$$

All monetary variables must use the same base year. Units must remain consistent across cities and years. DEA is invariant to some simple rescalings, but inconsistent units alter the estimated production frontier.

### 3.2 Positivity and panel checks

Every model variable must be finite and strictly positive. Each city-year pair must be unique, and the set of cities must remain unchanged between adjacent periods. Missing or infeasible values must be reported; they must not be silently replaced by zero, one, or manually selected values.

## 4. Environmental production technologies

### 4.1 Contemporaneous technology

The contemporaneous frontier for year \(t\) uses only the DMUs observed in that year. Under constant returns to scale (CRS), the technology is

$$
P^{t}=\left\{(x,y,b):
X^{t}\lambda\leq x,
\quad Y^{t}\lambda\geq y,
\quad B^{t}\lambda\leq b,
\quad \lambda\geq0
\right\}.
$$

The reference combination cannot use more input than the evaluated DMU, must produce at least as much desirable output, and cannot produce more undesirable output. CRS does not impose a convexity constraint. Adding

$$
\mathbf{1}^{\prime}\lambda=1
$$

changes the model to variable returns to scale (VRS). CRS and VRS results have different interpretations and must not be mixed without an explicit scale-efficiency decomposition.

### 4.2 Sequential technology

A sequential technology for year \(t\) pools all observations from the initial period through \(t\):

$$
P_{\mathrm{seq}}^{t}=\operatorname{conv}
\left(P^{2000}\cup P^{2001}\cup\cdots\cup P^{t}\right).
$$

The sequential construction prevents the reference frontier from contracting when previously feasible technologies disappear. However, an “adjacent” Malmquist setting only identifies the pair of periods being compared; it does not prove that a sequential reference set was used. The archived MaxDEA summary confirms adjacent-period comparison but does not establish the original frontier mode.

### 4.3 Global technology

The global technology pools observations from all periods into one common reference set:

$$
P^{G}=\operatorname{conv}
\left(P^{2000}\cup P^{2001}\cup\cdots\cup P^{T}\right).
$$

Because every observation is evaluated against the same technology, the global index is circular and is less exposed to infeasible cross-period programs. Its technical-change interpretation differs from the contemporaneous four-distance index, so global estimates must be treated as a new empirical specification rather than inserted into tables produced by the archived MaxDEA model.

## 5. Directional distance function

The output-oriented environmental DDF expands desirable output and contracts undesirable output while holding inputs fixed. For direction \(g=(g_y,-g_b)\), define

$$
\overrightarrow{D}_{0}^{\,r}(x,y,b;g_y,-g_b)
=\sup\left\{\beta:
(y+\beta g_y,b-\beta g_b)\in P^{r}(x)
\right\}.
$$

The common observation-specific direction \(g=(y,-b)\) asks how far desirable output can be proportionally expanded while undesirable output is proportionally contracted. A value of \(\beta=0\) places the observation on the selected frontier; \(\beta>0\) indicates remaining improvement potential.

Under CRS and a sequential reference technology through period \(r\), the linear program for observation \(o\) is

$$
\begin{aligned}
\max_{\beta,\lambda}\quad & \beta \\
\text{s.t.}\quad
&\sum_{s=2000}^{r}\sum_j\lambda_{j,s}x_{j,s}\leq x_o,\\
&\sum_{s=2000}^{r}\sum_j\lambda_{j,s}y_{j,s}\geq(1+\beta)y_o,\\
&\sum_{s=2000}^{r}\sum_j\lambda_{j,s}b_{j,s}\leq(1-\beta)b_o,\\
&\lambda_{j,s}\geq0.
\end{aligned}
$$

Some environmental technologies impose equality on the undesirable-output constraint to represent weak disposability; others use an inequality that permits an independent reduction in bad output. These assumptions define different technologies. The code and the paper must use the same convention.

## 6. Classical Malmquist–Luenberger index

### 6.1 Four required distances

For adjacent periods \(t\) and \(t+1\), the classical index requires four distances:

1. \(D^{t}(z_t)\): the period-\(t\) observation against the period-\(t\) frontier;
2. \(D^{t}(z_{t+1})\): the period-\(t+1\) observation against the period-\(t\) frontier;
3. \(D^{t+1}(z_t)\): the period-\(t\) observation against the period-\(t+1\) frontier; and
4. \(D^{t+1}(z_{t+1})\): the period-\(t+1\) observation against the period-\(t+1\) frontier.

The second and third terms are cross-period evaluations and are the most common source of infeasibility.

### 6.2 Index and decomposition

When a larger DDF denotes more remaining improvement potential, the adjacent-period ML index is

$$
ML_{t,t+1}=
\left[
\frac{1+D^{t}(z_t)}{1+D^{t}(z_{t+1})}
\frac{1+D^{t+1}(z_t)}{1+D^{t+1}(z_{t+1})}
\right]^{1/2}.
$$

It can be decomposed into efficiency change and technical change:

$$
EC_{t,t+1}=
\frac{1+D^{t}(z_t)}{1+D^{t+1}(z_{t+1})},
$$

$$
TC_{t,t+1}=
\left[
\frac{1+D^{t+1}(z_t)}{1+D^{t}(z_t)}
\frac{1+D^{t+1}(z_{t+1})}{1+D^{t}(z_{t+1})}
\right]^{1/2},
$$

so that

$$
ML_{t,t+1}=EC_{t,t+1}\times TC_{t,t+1}.
$$

Values above one indicate improvement, values equal to one indicate no change, and values below one indicate deterioration. Specifically, \(EC>1\) indicates movement toward the frontier, while \(TC>1\) indicates a favorable movement of the reference technology.

## 7. Non-oriented undesirable-output SBM

The SBM directly incorporates input excess, desirable-output shortfall, and undesirable-output excess. For evaluated DMU \(o\), the ordinary non-oriented undesirable-output SBM is

$$
\rho_o=\min
\frac{
1-\frac{1}{N}\sum_{n=1}^{N}s_n^x/x_{no}
}{
1+\frac{1}{M+I}
\left(
\sum_{m=1}^{M}s_m^y/y_{mo}
+\sum_{i=1}^{I}s_i^b/b_{io}
\right)
},
$$

subject to

$$
\begin{aligned}
X\lambda+s^x&=x_o,\\
Y\lambda-s^y&=y_o,\\
B\lambda+s^b&=b_o,\\
\lambda,s^x,s^y,s^b&\geq0.
\end{aligned}
$$

The implementation in `src/gtfp_sbm/model.py` applies the Charnes–Cooper transformation and solves the resulting linear program with SciPy/HiGHS.

An ordinary SBM score is bounded by one when the evaluated DMU belongs to its own reference set. The archived MaxDEA scores include values above one, which confirms that super-efficiency was active. Super-efficiency removes an efficient DMU from its own reference set and re-evaluates it, allowing efficient observations to receive scores above one. This procedure is not reproduced by merely adding a label to the ordinary SBM program.

## 8. Four-distance SBM productivity account

Let \(S^{r}(z_s)\) denote an SBM score for observation \(s\) against reference technology \(r\), where a higher score represents better performance. If all four scores are feasible, define

$$
GTFP_{t,t+1}=
\left[
\frac{S^{t}(z_{t+1})}{S^{t}(z_t)}
\frac{S^{t+1}(z_{t+1})}{S^{t+1}(z_t)}
\right]^{1/2},
$$

$$
EC_{t,t+1}=
\frac{S^{t+1}(z_{t+1})}{S^{t}(z_t)},
$$

and

$$
TC_{t,t+1}=
\left[
\frac{S^{t}(z_{t+1})}{S^{t+1}(z_{t+1})}
\frac{S^{t}(z_t)}{S^{t+1}(z_t)}
\right]^{1/2}.
$$

The decomposition satisfies

$$
GTFP_{t,t+1}=EC_{t,t+1}\times TC_{t,t+1}.
$$

The DDF equations use \(1+D\), whereas the SBM equations use an efficiency score \(S\). The two quantities have different meanings and directions and cannot be substituted for one another.

## 9. Archived MaxDEA specification

The preserved MaxDEA summary supports the following statements:

- model family: envelopment model;
- sample dimensions: 19 periods and 21 DMUs;
- variable roles: three inputs and two outputs, with CO2 treated as undesirable;
- distance type: maximum distance to frontier (SBM);
- orientation: non-oriented;
- extension: super-efficiency;
- productivity comparison: adjacent-period Malmquist;
- aggregation: multiplicative, geometric mean; and
- reported decompositions: CRS, VRS, scale effects, and extended components.

These settings identify the archived calculation as a super-efficiency SBM Malmquist application. The summary does not preserve the exact cross-period super-efficiency reference rules, infeasibility conventions, or proof that a sequential frontier was enabled. Consequently, this repository implements transparent open equations but does not claim bit-for-bit equivalence with MaxDEA.

## 10. Open implementation choices

| Command | Method | Main advantage | Main limitation | Recommended use |
| --- | --- | --- | --- | --- |
| `--method global-ml` | Global DDF–ML | Common technology, circularity, complete open route for this panel | Produces a new empirical specification | Recommended open re-estimation |
| `--method cfg-ml` | Classical CFG DDF–ML | Closely follows the standard DDF–ML definition | Cross-period distances may be infeasible | Theoretical benchmark |
| `--method apz-ml` | APZ DDF–ML | Addresses consistency and feasibility weaknesses of classical ML | May still contain invalid transitions | Robustness analysis |
| `--method sbm-ml` | Ordinary four-distance SBM | Transparent LP and direct equation audit | No MaxDEA super-efficiency clone; cross-period programs may fail | Formula and data-structure audit |

The first three methods use DEAPack. The ordinary SBM route is implemented locally with SciPy/HiGHS.

## 11. Reproducible calculation workflow

1. Standardize city identifiers, years, units, and missing-value codes.
2. Convert fixed-asset investment and GDP to constant 2000 prices.
3. Construct capital stock with the perpetual inventory method and record the initialization and depreciation assumptions.
4. Apply the specified two-year moving average to labor while retaining the base-year observation.
5. Assemble electricity use, real GDP, and CO2 emissions and verify strict positivity.
6. Verify that each city-year pair is unique and that adjacent years contain the same DMUs.
7. Select one model family: DDF–ML, SBM Malmquist, or global ML. Do not mix their names or distance conventions.
8. Record the frontier mode: contemporaneous, sequential, or global.
9. Record returns to scale: omit the convexity constraint for CRS and impose \(\mathbf{1}^{\prime}\lambda=1\) for VRS.
10. Solve the required distance programs and preserve the solver status for every observation.
11. Compute GTFP, EC, and TC and verify the multiplicative identity within a stated numerical tolerance.
12. Aggregate city-level indices only after confirming that every annual group has the intended number of cities.
13. Merge the final index into downstream analysis by city and year.
14. Save the method name, frontier mode, returns-to-scale assumption, package versions, and command used for each run.

## 12. Quality-control checklist

| Check | Acceptance rule |
| --- | --- |
| Panel uniqueness | Every city-year pair appears exactly once |
| Panel balance | The intended cities are present in every period |
| Numerical validity | All model variables are finite and strictly positive |
| Transition coverage | Every intended adjacent-period city transition is represented |
| Decomposition identity | `gtfp` equals `ec * tc` within numerical tolerance |
| Infeasibility handling | Failed programs retain city, period pair, distance role, and solver status |
| Annual aggregation | Each annual mean uses a documented and consistent city set |
| Method metadata | Output records method, reference technology, returns to scale, and version |
| Paper consistency | Tables, figures, descriptive statistics, and regressions use the same GTFP version |

## 13. Suggested method statements

### 13.1 If the archived MaxDEA results are retained

> Green total factor productivity was estimated under constant returns to scale using a non-oriented super-efficiency slacks-based measure that jointly accounts for input excess, desirable-output shortfall, and undesirable-output excess. Adjacent-period Malmquist indices were formed by multiplicative geometric-mean aggregation and decomposed into efficiency change and technical change. Carbon dioxide emissions were treated as an undesirable output. Because the original MaxDEA project file is unavailable, the archived estimates are retained as software-generated results, while the accompanying open code documents the ordinary SBM equations and alternative open environmental productivity estimators rather than claiming exact numerical replication.

### 13.2 If the study is re-estimated with the open global method

> Green total factor productivity was estimated with a global Malmquist–Luenberger index under constant returns to scale. The environmental production technology contains real capital stock, labor, and electricity consumption as inputs, real GDP as the desirable output, and carbon dioxide emissions as the undesirable output. Directional distance functions expand desirable output and contract undesirable output relative to a common technology constructed from all city-year observations. The resulting productivity index is decomposed into efficiency change and technical change, with values above one indicating improvement. The common global technology ensures circularity and avoids the cross-period infeasibility associated with the classical four-distance formulation.

## 14. References

- Chung, Y. H., Fare, R., and Grosskopf, S. (1997). Productivity and undesirable outputs: A directional distance function approach. *Journal of Environmental Management*, 51, 229–240.
- Tone, K. (2001). A slacks-based measure of efficiency in data envelopment analysis. *European Journal of Operational Research*, 130, 498–509.

