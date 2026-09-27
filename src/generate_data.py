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
