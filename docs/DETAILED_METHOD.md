# Theoretical Framework for GTFP Measurement

## 1. Scope

Green total factor productivity (GTFP) measures changes in production performance after desirable and undesirable outputs are considered jointly. This document presents two closely related theoretical approaches: the directional distance function–Malmquist–Luenberger (DDF–ML) framework and the undesirable-output slacks-based measure (SBM) Malmquist framework. Both belong to data envelopment analysis, but their distance measures have different meanings and must not be substituted for one another.

## 2. Units of analysis and notation

Each prefecture-level city in each year is treated as a decision-making unit (DMU). For city $i$ in year $t$, define

$$
z_{i,t}=(x_{i,t},y_{i,t},b_{i,t}),
$$

where

- $x_{i,t}\in\mathbb{R}_{+}^{N}$ is the input vector;
- $y_{i,t}\in\mathbb{R}_{+}^{M}$ is the desirable-output vector; and
- $b_{i,t}\in\mathbb{R}_{+}^{I}$ is the undesirable-output vector.

The Guangdong application uses three inputs ($N=3$), one desirable output ($M=1$), and one undesirable output ($I=1$). The original balanced panel contains 21 cities observed from 2000 through 2018. The first year supplies the base observations, so adjacent-period productivity changes are dated 2001–2018.

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

where $I_{i,t}$ is real fixed-asset investment after price deflation. The original study initializes the series as

$$
K_{i,2000}=\frac{I_{i,2000}}{0.10}.
$$

All monetary variables must use the same base year. Units must remain consistent across cities and years. DEA is invariant to some simple rescalings, but inconsistent units alter the estimated production frontier.

### 3.2 Positivity and panel checks

Every model variable must be finite and strictly positive. Each city-year pair must be unique, and the set of cities must remain unchanged between adjacent periods. Missing or infeasible values must be reported; they must not be silently replaced by zero, one, or manually selected values.

## 4. Environmental production technologies

### 4.1 Contemporaneous technology

The contemporaneous frontier for year $t$ uses only the DMUs observed in that year. Under constant returns to scale (CRS), the technology is

$$
P^{t}=\left\lbrace(x,y,b):
X^{t}\lambda\leq x,
\quad Y^{t}\lambda\geq y,
\quad B^{t}\lambda\leq b,
\quad \lambda\geq0
\right\rbrace.
$$

The reference combination cannot use more input than the evaluated DMU, must produce at least as much desirable output, and cannot produce more undesirable output. CRS does not impose a convexity constraint. Adding

$$
\mathbf{1}^{\prime}\lambda=1
$$

changes the model to variable returns to scale (VRS). CRS and VRS results have different interpretations and must not be mixed without an explicit scale-efficiency decomposition.

### 4.2 Sequential technology

A sequential technology for year $t$ pools all observations from the initial period through $t$:

$$
P_{\mathrm{seq}}^{t}=\mathrm{conv}
\left(P^{2000}\cup P^{2001}\cup\cdots\cup P^{t}\right).
$$

The sequential construction prevents the reference frontier from contracting when previously feasible technologies disappear. However, an adjacent-period Malmquist index only identifies the pair of periods being compared; it does not by itself imply that a sequential reference set is used.

### 4.3 Global technology

The global technology pools observations from all periods into one common reference set:

$$
P^{G}=\mathrm{conv}
\left(P^{2000}\cup P^{2001}\cup\cdots\cup P^{T}\right).
$$

Because every observation is evaluated against the same technology, the global index is circular and is less exposed to infeasible cross-period programs. Its technical-change interpretation differs from the contemporaneous four-distance index, so estimates from the two specifications should not be combined without explicit justification.

## 5. Directional distance function

The output-oriented environmental DDF expands desirable output and contracts undesirable output while holding inputs fixed. For direction $g=(g_y,-g_b)$, define

$$
\overrightarrow{D}_{0}^{r}(x,y,b;g_y,-g_b)
=\sup\left\lbrace\beta:
(y+\beta g_y,b-\beta g_b)\in P^{r}(x)
\right\rbrace.
$$

The common observation-specific direction $g=(y,-b)$ asks how far desirable output can be proportionally expanded while undesirable output is proportionally contracted. A value of $\beta=0$ places the observation on the selected frontier; $\beta>0$ indicates remaining improvement potential.

Under CRS and a sequential reference technology through period $r$, the linear program for observation $o$ is

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

Some environmental technologies impose equality on the undesirable-output constraint to represent weak disposability; others use an inequality that permits an independent reduction in bad output. These assumptions define different technologies, so the selected convention must be stated explicitly and applied consistently.

## 6. Classical Malmquist–Luenberger index

### 6.1 Four required distances

For adjacent periods $t$ and $t+1$, the classical index requires four distances:

1. $D^{t}(z_t)$: the period-$t$ observation against the period-$t$ frontier;
2. $D^{t}(z_{t+1})$: the period-$t+1$ observation against the period-$t$ frontier;
3. $D^{t+1}(z_t)$: the period-$t$ observation against the period-$t+1$ frontier; and
4. $D^{t+1}(z_{t+1})$: the period-$t+1$ observation against the period-$t+1$ frontier.

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

Values above one indicate improvement, values equal to one indicate no change, and values below one indicate deterioration. Specifically, $EC>1$ indicates movement toward the frontier, while $TC>1$ indicates a favorable movement of the reference technology.

## 7. Non-oriented undesirable-output SBM

The SBM directly incorporates input excess, desirable-output shortfall, and undesirable-output excess. For evaluated DMU $o$, the ordinary non-oriented undesirable-output SBM is

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

An ordinary SBM score is bounded by one when the evaluated DMU belongs to its own reference set. In a super-efficiency extension, an efficient DMU is removed from its own reference set and re-evaluated, allowing efficient observations to receive scores above one. Ordinary and super-efficiency SBM scores therefore have different feasible reference sets and interpretations.

## 8. Four-distance SBM productivity account

Let $S^{r}(z_s)$ denote an SBM score for observation $s$ against reference technology $r$, where a higher score represents better performance. If all four scores are feasible, define

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

The DDF equations use $1+D$, whereas the SBM equations use an efficiency score $S$. The two quantities have different meanings and directions and cannot be substituted for one another.

## 9. Empirical procedure

The empirical procedure consists of six stages. First, monetary variables are converted to constant 2000 prices, and capital stock is constructed with the perpetual inventory method. Second, the labor series is smoothed using the stated two-year moving average, while electricity consumption, real GDP, and carbon emissions are assembled in consistent units. Third, the balanced city-level panel is checked for uniqueness, completeness, and strictly positive values. Fourth, the production technology, returns-to-scale assumption, orientation, and treatment of undesirable output are specified consistently. Fifth, the relevant distance or efficiency measures are estimated for each adjacent-period comparison. Finally, GTFP is calculated and decomposed into efficiency change and technical change, with the identity $GTFP=EC\times TC$ used as an internal consistency check.

## 10. Interpretation and methodological consistency

For both index families, a productivity value above one indicates improvement, a value equal to one indicates no change, and a value below one indicates deterioration. Efficiency change describes movement toward or away from the reference frontier, whereas technical change captures movement of the frontier itself. The selected distance convention, production technology, returns-to-scale assumption, treatment of undesirable output, and reference set must remain consistent throughout estimation and interpretation. In particular, a DDF-based index expressed through $1+D$ is not numerically interchangeable with an SBM index expressed through efficiency score $S$.

## 11. References

- Chung, Y. H., Fare, R., and Grosskopf, S. (1997). Productivity and undesirable outputs: A directional distance function approach. *Journal of Environmental Management*, 51, 229–240.
- Tone, K. (2001). A slacks-based measure of efficiency in data envelopment analysis. *European Journal of Operational Research*, 130, 498–509.
