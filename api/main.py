from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from drift import drift_report, simulate_current
from optimizer import run_optimization

DATA_PATH = Path(__file__).parent / "data" / "customer_effects.csv"
customers = pd.read_csv(DATA_PATH)

app = FastAPI(title="EconoCausal API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class OptimizeRequest(BaseModel):
    budget: float = 5000
    avg_order_value: float = 100


@app.get("/health")
def health():
    return {"status": "ok", "customers": len(customers)}


@app.post("/optimize")
def optimize(req: OptimizeRequest):
    return run_optimization(customers, req.budget, req.avg_order_value)


@app.get("/drift")
def drift(income_shift: float = 0.0):
    """Demo: compares the training customers against a simulated 'current' batch.
    income_shift adds a constant to income in the simulated batch to mimic a behaviour change."""
    current = simulate_current(customers, income_shift=income_shift)
    return drift_report(customers, current)