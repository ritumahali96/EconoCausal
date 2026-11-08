import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import identity, hstack, csr_matrix


def optimize_discounts(gain10, gain20, budget):
    """Choose $0 / $10 / $20 per customer to maximise total gain within the budget."""
    n = len(gain10)
    c = -np.concatenate([gain10, gain20])  # milp minimises, so negate
    budget_row = csr_matrix(
        np.concatenate([np.full(n, 10.0), np.full(n, 20.0)]).reshape(1, -1)
    )
    one_row = hstack([identity(n), identity(n)], format="csr")
    constraints = [
        LinearConstraint(budget_row, -np.inf, budget),  # total spend <= budget
        LinearConstraint(one_row, -np.inf, 1),          # at most one discount each
    ]
    res = milp(c, constraints=constraints, integrality=np.ones(2 * n), bounds=Bounds(0, 1))
    x = np.round(res.x).astype(int)
    discount = np.where(x[:n] == 1, 10, np.where(x[n:] == 1, 20, 0))
    return discount, res


def run_optimization(df, budget, avg_order_value):
    gain10 = df["effect_10"].clip(lower=0).values * avg_order_value
    gain20 = df["effect_20"].clip(lower=0).values * avg_order_value
    discount, res = optimize_discounts(gain10, gain20, budget)

    chosen_gain = np.where(discount == 10, gain10, np.where(discount == 20, gain20, 0))
    opt_revenue = float(chosen_gain.sum())
    blanket_revenue = float(gain10.mean() * (budget // 10))  # $10 to as many customers as the budget allows, no targeting
    spend = float(discount.sum())
    n10, n20 = int((discount == 10).sum()), int((discount == 20).sum())

    diff = opt_revenue - blanket_revenue
    pct = (diff / blanket_revenue * 100) if blanket_revenue > 0 else 0.0
    summary = (
        f"This strategy gives ${spend:,.0f} in discounts to {n10 + n20} customers "
        f"({n20} at $20, {n10} at $10) and is projected to generate ${opt_revenue:,.0f} "
        f"in incremental revenue. That is ${diff:,.0f} ({pct:.0f}%) "
        f"{'more' if diff >= 0 else 'less'} than blanket targeting with the same budget."
    )

    chosen = df.assign(discount=discount, expected_gain=chosen_gain)
    chosen = chosen[chosen["discount"] > 0].sort_values("expected_gain", ascending=False)
    prescription = [
        {
            "customer_id": int(r.customer_id),
            "income": float(r.income),
            "loyalty_score": float(r.loyalty_score),
            "discount": int(r.discount),
            "expected_gain": round(float(r.expected_gain), 2),
        }
        for r in chosen.itertuples()
    ]
    return {
        "summary": summary,
        "budget": budget,
        "spend": spend,
        "customers_at_10": n10,
        "customers_at_20": n20,
        "optimized_revenue": round(opt_revenue, 2),
        "blanket_revenue": round(blanket_revenue, 2),
        "prescription": prescription,
    }