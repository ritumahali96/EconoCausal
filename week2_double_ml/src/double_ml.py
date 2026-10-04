import pandas as pd
import numpy as np

df = pd.read_csv("week1_causal_graphing/data/retail_campaign_data.csv")

df["treated"] = (df["discount_given"] > 0).astype(int)
