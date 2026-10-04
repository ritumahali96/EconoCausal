# Week 2 Notes -- Double ML, ITE, and Uplift

- ITE (Individual Treatment Effect): how much a specific customer's
  purchase probability changes if given a discount, estimated via
  Double ML (CausalForestDML), controlling for loyalty_score and income.
- Individual ITE values are noisy, especially in sparse regions of the
  confounder space (e.g. very high income customers).
- Grouping customers into deciles by ITE and checking REAL observed
  uplift per group smooths out individual noise and reveals whether
  the ranking carries genuine signal.

## Qini curve
The Qini curve tracks cumulative incremental purchases as we target
customers in ranked order (best ITE first), compared to a random
targeting baseline. Our model's curve sits well above the random
baseline for most of the range, proving the ranking has real business
value -- targeting the top-ranked customers yields substantially more
incremental purchases than targeting randomly, for the same budget.
Both curves converge at the end, since targeting everyone is
equivalent regardless of order.
