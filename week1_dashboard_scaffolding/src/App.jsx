import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import UploadData from "./pages/UploadData";
import BudgetSettings from "./pages/BudgetSettings";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: "flex", gap: "1rem", padding: "1rem", borderBottom: "1px solid #333" }}>
        <Link to="/">Upload Data</Link>
        <Link to="/budget">Budget Settings</Link>
      </nav>
      <Routes>
        <Route path="/" element={<UploadData />} />
        <Route path="/budget" element={<BudgetSettings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;