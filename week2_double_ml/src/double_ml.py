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
