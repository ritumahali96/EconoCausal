
import { useEffect, useMemo, useState } from "react";
import Papa from "papaparse";
import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js-dist-min";

const Plot = createPlotlyComponent(Plotly);

const chartLayout = {
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "rgba(0,0,0,0)",
  font: { color: "#ccc" },
  margin: { t: 40 },
  autosize: true,
};

function ITEExplorer() {
  const [rows, setRows] = useState([]);
  const [decile, setDecile] = useState("all");
  const [minIncome, setMinIncome] = useState(0);

  useEffect(() => {
    Papa.parse("/customer_ite_scores.csv", {
      download: true,
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (res) => setRows(res.data),
    });
  }, []);

  const filtered = useMemo(
    () =>
      rows.filter(
        (r) =>
          (decile === "all" || r.decile === Number(decile)) &&
          r.income >= minIncome
      ),
    [rows, decile, minIncome]
  );

  const avgIte = filtered.length
    ? filtered.reduce((sum, r) => sum + r.ite, 0) / filtered.length
    : 0;

  if (rows.length === 0) {
    return <div style={{ padding: "2rem" }}>Loading customer ITE scores...</div>;
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Customer ITE Explorer</h1>

      <div style={{ display: "flex", gap: "2rem", marginBottom: "1rem" }}>
        <label>
          Decile:{" "}
          <select value={decile} onChange={(e) => setDecile(e.target.value)}>
            <option value="all">All</option>
            {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </label>
        <label>
          Minimum income (k$): {minIncome}{" "}
          <input
            type="range"
            min="0"
            max="150"
            value={minIncome}
            onChange={(e) => setMinIncome(Number(e.target.value))}
          />
        </label>
      </div>

      <p>
        Showing {filtered.length} of {rows.length} customers | Average ITE:{" "}
        {avgIte.toFixed(4)}
      </p>

      <Plot
        data={[{ x: filtered.map((r) => r.ite), type: "histogram", nbinsx: 40 }]}
        layout={{
          ...chartLayout,
          title: { text: "Distribution of ITE scores" },
          xaxis: { title: { text: "ITE" } },
        }}
        useResizeHandler
        style={{ width: "100%", height: "350px" }}
      />

      <Plot
        data={[
          {
            x: filtered.map((r) => r.income),
            y: filtered.map((r) => r.ite),
            mode: "markers",
            type: "scatter",
            marker: {
              color: filtered.map((r) => r.ite),
              colorscale: "Viridis",
              showscale: true,
              size: 6,
            },
          },
        ]}
        layout={{
          ...chartLayout,
          title: { text: "ITE vs income" },
          xaxis: { title: { text: "Income (k$)" } },
          yaxis: { title: { text: "ITE" } },
        }}
        useResizeHandler
        style={{ width: "100%", height: "400px" }}
      />
    </div>
  );
}

export default ITEExplorer;
