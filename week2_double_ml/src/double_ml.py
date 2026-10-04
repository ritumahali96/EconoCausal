import pandas as pd
import numpy as np

df = pd.read_csv("week1_causal_graphing/data/retail_campaign_data.csv")

df["treated"] = (df["discount_given"] > 0).astype(int)

# NOTE: discount_given has 3 values (0/10/20). We simplify to binary
# treated (0/1) for this first DML pass, since EconML's core estimators
# work most cleanly with binary or continuous treatment.

from econml.dml import LinearDML

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

est = LinearDML(
    model_y=RandomForestRegressor(n_estimators=100, random_state=42),
    model_t=RandomForestClassifier(n_estimators=100, random_state=42),
    discrete_treatment=True,
    random_state=42,
)

# model_y predicts purchased from confounders alone (ignoring discount).
# model_t predicts treated from confounders alone.
# DML uses the leftover prediction error from both to isolate the
# true causal effect, cleaned of confounder bias.

# discrete_treatment=True tells EconML that T is a category (0/1),
# not a continuous number -- required when model_t is a Classifier.

est.fit(
    Y=df["purchased"],
    T=df["treated"],
    X=df[["loyalty_score", "income"]],
)

print("LinearDML trained!")

ate = est.ate(df[["loyalty_score", "income"]])

print(f"LinearDML estimated ATE: {ate:.4f}")

true_effect_per_10_dollars = 0.04
true_ate = (true_effect_per_10_dollars * (df.loc[df["treated"] == 1, "discount_given"] / 10)).mean()

print(f"True ATE (ground truth):  {true_ate:.4f}")
print(f"LinearDML estimated ATE:  {ate:.4f}")
print(f"Gap:                      {abs(true_ate - ate):.4f}")

# NOTE: LinearDML underestimates the true effect. Likely cause: weak
# overlap -- loyal/high-income customers almost always got a discount,
# so there are few comparable "twins" across treatment groups for the
# model to learn the clean effect from.

from econml.dml import CausalForestDML

est_cf = CausalForestDML(
    model_y=RandomForestRegressor(n_estimators=100, random_state=42),
    model_t=RandomForestClassifier(n_estimators=100, random_state=42),
    discrete_treatment=True,
    random_state=42,
)

est_cf.fit(Y=df["purchased"], T=df["treated"], X=df[["loyalty_score", "income"]])
ate_cf = est_cf.ate(df[["loyalty_score", "income"]])
print(f"CausalForestDML estimated ATE: {ate_cf:.4f}")

# Finding: CausalForestDML's ATE is similar to LinearDML's, both still
# below the true value. This suggests the gap is driven by data
# overlap, not estimator choice -- no model can fully compensate for
# weak overlap between treated/untreated groups on confounders.

df["ite"] = est_cf.effect(df[["loyalty_score", "income"]])

print(df[["customer_id", "loyalty_score", "income", "discount_given", "ite"]]
      .sort_values("ite", ascending=False).head(10))

# CAUTION: top-ranked customers may cluster in sparse regions of the
# confounder space (e.g. very high income), where the model has little
# data and can produce noisy, overconfident estimates.

print(df["ite"].describe())
print(f"Customers with income > 100: {(df['income'] > 100).sum()} out of {len(df)}")

# Finding: a small fraction of customers have very high income, giving
# the model little data there. Combined with a true effect that does
# NOT vary by income/loyalty, this confirms individual ITE values carry
# real noise -- decile-level grouping (next) is needed to see signal.

df["decile"] = pd.qcut(df["ite"], 10, labels=False, duplicates="drop")
df["decile"] = 9 - df["decile"]

uplift_by_decile = df.groupby("decile", group_keys=False).apply(
    lambda g: g.loc[g["treated"] == 1, "purchased"].mean() - g.loc[g["treated"] == 0, "purchased"].mean(),
    include_groups=False,
)

print(uplift_by_decile.sort_index())

# Finding: uplift trends downward from decile 0 to decile 9 overall,
# confirming the model's ranking carries real signal, despite
# individual-level noise -- exactly why grouping matters for evaluation.

import matplotlib.pyplot as plt

sorted_uplift = uplift_by_decile.sort_index()
plt.figure(figsize=(8, 5))
plt.bar(sorted_uplift.index.astype(str), sorted_uplift.values, color="#2a9d8f")
plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Decile (0 = highest predicted ITE / best targets, 9 = lowest)")
plt.ylabel("Observed uplift (treated - untreated purchase rate)")
plt.title("Uplift by ITE Decile")
plt.tight_layout()

plt.savefig("week2_double_ml/docs/uplift_chart.png", dpi=150)
print("Saved week2_double_ml/docs/uplift_chart.png")

df_sorted = df.sort_values("ite", ascending=False).reset_index(drop=True)
cum_treated_purchases = (df_sorted["treated"] * df_sorted["purchased"]).cumsum()
cum_untreated_purchases = ((1 - df_sorted["treated"]) * df_sorted["purchased"]).cumsum()
cum_treated_count = df_sorted["treated"].cumsum()
cum_untreated_count = (1 - df_sorted["treated"]).cumsum()
