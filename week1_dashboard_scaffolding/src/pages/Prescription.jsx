import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

function Prescription() {
  const [budget, setBudget] = useState(5000);
  const [orderValue, setOrderValue] = useState(100);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [shift, setShift] = useState(0);
  const [drift, setDrift] = useState(null);

  const checkDrift = (incomeShift) => {
    fetch(`${API}/drift?income_shift=${incomeShift}`)
      .then((r) => r.json())
      .then(setDrift)
      .catch(() => setDrift(null));
  };

  useEffect(() => {
    checkDrift(0);
  }, []);

  const runOptimization = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/optimize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          budget: Number(budget),
          avg_order_value: Number(orderValue),
        }),
      });
      if (!res.ok) throw new Error(`API returned ${res.status}`);
      setResult(await res.json());
    } catch (e) {
      setError("Could not reach the API. Is uvicorn running on port 8000? (" + e.message + ")");
    } finally {
      setLoading(false);
    }
  };

  const box = { padding: "1rem", borderRadius: "8px", marginBottom: "1rem" };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Prescription</h1>
      <p>Optimal personalised discounts for a fixed marketing budget.</p>

      {drift && (
        <div
          style={{
            ...box,
            background: drift.status === "ok" ? "#12351f" : "#4a1d1d",
            border: `1px solid ${drift.status === "ok" ? "#2a9d8f" : "#e63946"}`,
          }}
        >
          <strong>Data drift check:</strong> {drift.message}
          <div style={{ marginTop: "0.5rem" }}>
            <label>
              Simulate income shift:{" "}
              <input
                type="number"
                value={shift}
                onChange={(e) => setShift(e.target.value)}
                style={{ width: "5rem" }}
              />
            </label>{" "}
            <button onClick={() => checkDrift(Number(shift))}>Check drift</button>
          </div>
        </div>
      )}

      <div style={{ display: "flex", gap: "2rem", marginBottom: "1rem", flexWrap: "wrap" }}>
        <label>
          Total budget ($):{" "}
          <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} />
        </label>
        <label>
          Avg order value ($):{" "}
          <input type="number" value={orderValue} onChange={(e) => setOrderValue(e.target.value)} />
        </label>
        <button onClick={runOptimization} disabled={loading}>
          {loading ? "Optimising..." : "Run optimisation"}
        </button>
      </div>

      {error && <div style={{ ...box, background: "#4a1d1d" }}>{error}</div>}

      {result && (
        <>
          <div style={{ ...box, background: "#1d2b3a", border: "1px solid #2a9d8f" }}>
            {result.summary}
          </div>

          <p>
            Spend: ${result.spend.toLocaleString()} of ${result.budget.toLocaleString()} |{" "}
            $20 customers: {result.customers_at_20} | $10 customers: {result.customers_at_10} |{" "}
            Projected incremental revenue: ${result.optimized_revenue.toLocaleString()} |{" "}
            Blanket baseline: ${result.blanket_revenue.toLocaleString()}
          </p>

          <p>
            Showing the top {Math.min(50, result.prescription.length)} of{" "}
            {result.prescription.length} prescribed customers.
          </p>
          <div style={{ maxHeight: "420px", overflowY: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ textAlign: "left", borderBottom: "1px solid #444" }}>
                  <th>Customer</th>
                  <th>Income (k$)</th>
                  <th>Loyalty</th>
                  <th>Discount</th>
                  <th>Expected gain ($)</th>
                </tr>
              </thead>
              <tbody>
                {result.prescription.slice(0, 50).map((r) => (
                  <tr key={r.customer_id} style={{ borderBottom: "1px solid #333" }}>
                    <td>{r.customer_id}</td>
                    <td>{r.income}</td>
                    <td>{r.loyalty_score}</td>
                    <td>${r.discount}</td>
                    <td>{r.expected_gain}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

export default Prescription;