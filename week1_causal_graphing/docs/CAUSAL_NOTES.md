# Causal Graphing Notes

- Treatment: discount_given -- the lever we control ($0/$10/$20)
- Outcome: purchased -- the result we care about (1/0)
- Confounders: loyalty_score, income -- affect BOTH treatment and
  outcome. Ignoring them biases the estimated effect.
- DAG: a map of arrows (cause -> effect) that tells DoWhy exactly
  what to statistically control for, before any modeling happens.

## What DoWhy told us
identify_effect() read our DAG and confirmed: to isolate the true
effect of discount_given on purchased, control for loyalty_score
and income. age does not need to be controlled for, since it only
affects the outcome, not the treatment.

Status: Causal graphing complete. Next: Week 2 Double ML training
to estimate Individual Treatment Effect (ITE).
