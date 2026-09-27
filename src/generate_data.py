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
