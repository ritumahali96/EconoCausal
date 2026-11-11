import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import UploadData from "./pages/UploadData";
import BudgetSettings from "./pages/BudgetSettings";
import ITEExplorer from "./pages/ITEExplorer";
import Prescription from "./pages/Prescription";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: "flex", gap: "1rem", padding: "1rem", borderBottom: "1px solid #333" }}>
        <Link to="/">Upload Data</Link>
        <Link to="/budget">Budget Settings</Link>
        <Link to="/ite">ITE Explorer</Link>
        <Link to="/prescription">Prescription</Link>
      </nav>
      <Routes>
        <Route path="/" element={<UploadData />} />
        <Route path="/budget" element={<BudgetSettings />} />
        <Route path="/ite" element={<ITEExplorer />} />
        <Route path="/prescription" element={<Prescription />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;