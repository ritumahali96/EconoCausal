# Causal Graphing Notes

- Treatment: discount_given -- the lever we control ($0/$10/$20)
- Outcome: purchased -- the result we care about (1/0)
- Confounders: loyalty_score, income -- affect BOTH treatment and
  outcome. Ignoring them biases the estimated effect.
- DAG: a map of arrows (cause -> effect) that tells DoWhy exactly
  what to statistically control for, before any modeling happens.
