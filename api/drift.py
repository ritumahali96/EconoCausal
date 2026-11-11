import numpy as np
from scipy.stats import ks_2samp

FEATURES = ["age", "income", "loyalty_score"]


def drift_report(reference, current, alpha=0.01):
    """Two-sample Kolmogorov-Smirnov test per feature. Small p-value = distributions differ."""
    features = {}
    for col in FEATURES:
        stat, p = ks_2samp(reference[col], current[col])
        features[col] = {
            "ks_statistic": round(float(stat), 4),
            "p_value": float(p),
            "drifted": bool(p < alpha),
        }
    drifted = [c for c, v in features.items() if v["drifted"]]
    if drifted:
        message = (
            "WARNING: customer behaviour has shifted in: " + ", ".join(drifted)
            + ". The causal model may no longer be valid; consider retraining."
        )
    else:
        message = "No significant drift detected."
    return {"status": "drift" if drifted else "ok", "message": message, "features": features}


def simulate_current(reference, income_shift=0.0, seed=0):
    """Demo helper: a resample of the reference data, with income optionally shifted."""
    rng = np.random.default_rng(seed)
    current = reference.sample(n=len(reference), replace=True, random_state=int(rng.integers(1e6))).copy()
    current["income"] = current["income"] + income_shift
    return current