from fastapi import FastAPI
from pydantic import BaseModel
from physion_core import run_simulation

app = FastAPI(
    title="Physion V20 Web Simulation Engine",
    version="1.0.0"
)

class SimulationInput(BaseModel):
    C_rate: float = 1.0
    n_cycles: int = 1
    T_cell: float = 298.15

@app.post("/simulate")
def simulate(input: SimulationInput):
    result = run_simulation(input.dict())
    return {
        "status": "ok",
        "input": input.dict(),
        "result": result
    }
