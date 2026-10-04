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
