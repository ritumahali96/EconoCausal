"""
generate_data.py
-----------------
Simulating a retail marketing campaign that already happened
(observational data, not a clean randomized experiment). We build it
ourselves so we secretly KNOW the true causal effect, and can later
check whether our causal model finds that same true number.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

n_customers = 2000

# loyalty_score: 0 = brand new customer, 1 = super loyal
loyalty_score = np.random.beta(2, 3, n_customers)

# income: in thousands of dollars
income = np.random.normal(60, 20, n_customers).clip(15, 200)

# age: not a confounder here, just a normal cause of purchase
age = np.random.normal(38, 12, n_customers).clip(18, 80)

# NOTE: loyalty_score and income are CONFOUNDERS -- they affect both
# who gets a bigger discount AND who buys anyway. age is NOT a
# confounder -- it affects purchase but not discount assignment.

# discount_propensity: combines loyalty + income into one bias score
discount_propensity = 0.3 * loyalty_score + 0.002 * income

discount_options = np.array([0, 10, 20])  # dollars

discount_given = np.array([
    np.random.choice(
        discount_options,
        p=(w := np.clip([0.6 - 0.5 * prop, 0.25, 0.15 + 0.5 * prop], 0.01, None)) / w.sum()
    )
    for prop in discount_propensity
])

# NOTE: this is NOT a random A/B test. Higher-propensity customers are
# more likely to land on a bigger discount -- this bias is exactly what
# confuses naive ML and what DoWhy must correct for later.

# The REAL, secret causal effect we're hiding inside the data:
true_effect_per_10_dollars = 0.04

base_purchase_prob = 0.10  # baseline chance, everyone starts here

base_purchase_prob += 0.55 * loyalty_score  # confounder -> outcome

base_purchase_prob += 0.002 * income  # confounder -> outcome

base_purchase_prob += true_effect_per_10_dollars * (discount_given / 10)  # TRUE treatment effect

base_purchase_prob = np.clip(base_purchase_prob, 0.01, 0.99)

purchased = np.random.binomial(1, base_purchase_prob)

customer_id = range(1, n_customers + 1)

df = pd.DataFrame({
    "customer_id": customer_id,
    "age": age.round(1),
    "income": income.round(1),
    "loyalty_score": loyalty_score.round(3),
    "discount_given": discount_given,
    "purchased": purchased,
})

df.to_csv("data/retail_campaign_data.csv", index=False)

print("Saved data/retail_campaign_data.csv")

print(df.head(8))

print("\n--- Naive (WRONG) correlation view ---")
print(df.groupby("discount_given")["purchased"].mean())

# The gap you see above between $0 and $20 groups is BIGGER than our
# real, secret 8-point effect (0.04 * 2) -- that extra gap is the
# loyalty/income confounder leaking into the naive average.

assert set(purchased) <= {0, 1}, "purchased must only contain 0 or 1"

assert set(discount_given) <= {0, 10, 20}, "discount_given must only be 0, 10, or 20"

assert df.isnull().sum().sum() == 0, "dataframe must not contain missing values"
