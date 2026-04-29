# PMP Formulas

Exam-critical formulas. The agent may cite these directly in questions or use them
as the basis for calculation-style Qs.

---

## Earned Value Management (EVM)

### Variances
| Formula | Interpretation |
|---|---|
| `CV = EV − AC` | Cost variance. Negative = over budget. |
| `SV = EV − PV` | Schedule variance. Negative = behind schedule. |

### Performance Indices
| Formula | Interpretation |
|---|---|
| `CPI = EV / AC` | Cost Performance Index. < 1 = over budget. |
| `SPI = EV / PV` | Schedule Performance Index. < 1 = behind schedule. |

### Forecasting
| Formula | When to use |
|---|---|
| `EAC = BAC / CPI` | Current variance is **typical** (will continue). |
| `EAC = AC + (BAC − EV)` | Current variance is **atypical** (one-off). |
| `EAC = AC + [(BAC − EV) / (CPI × SPI)]` | Must meet schedule; both factors matter. |
| `ETC = EAC − AC` | Remaining expected cost. |
| `VAC = BAC − EAC` | Forecasted variance at completion. |
| `TCPI = (BAC − EV) / (BAC − AC)` | To-Complete Performance Index vs. BAC. |
| `TCPI = (BAC − EV) / (EAC − AC)` | TCPI vs. EAC. |

---

## Communication Channels

```
channels = n(n − 1) / 2
```
Where `n` = number of stakeholders (including the project manager).

Example: adding 1 person to a 5-person team changes channels from 10 to 15.

---

## Three-Point (PERT) Estimation

| Formula | Notes |
|---|---|
| `tE = (O + 4M + P) / 6` | Beta/PERT weighted mean. |
| `tE = (O + M + P) / 3` | Triangular (unweighted). |
| `σ = (P − O) / 6` | Activity standard deviation. |
| `Variance = σ²` | Variances are additive along a path. |

Where `O` = optimistic, `M` = most likely, `P` = pessimistic.

---

## Risk — Expected Monetary Value

```
EMV = probability × impact
```

For a decision tree, sum EMVs of each branch and pick the lowest-cost (threat) or
highest-value (opportunity) path.

---

## Point of Total Assumption (Fixed-Price Incentive Fee)

```
PTA = ((Ceiling Price − Target Price) / Buyer Share) + Target Cost
```

Above PTA, the seller bears 100% of additional cost.

---

## Present Value / Benefit-Cost

| Formula | Notes |
|---|---|
| `PV = FV / (1 + r)^n` | Present value of future amount. |
| `NPV` | Higher is better. Pick highest. |
| `IRR` | Higher is better. |
| `BCR (Benefit Cost Ratio)` | > 1 means benefits exceed costs. |
| `ROI` | Higher is better. |
| `Payback period` | Shorter is better. |
