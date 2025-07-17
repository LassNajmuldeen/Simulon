from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import uuid
from fastapi.responses import FileResponse
import os

from src.core.heat_solver import HeatEquationSolver
from src.core.pinn_solver import PINNHeatEquationSolver
from src.visualizer.heat_visualizer import animate_heat_solution

app = FastAPI(title="Simulon: Scientific Simulation API")

# In-memory storage for simulation results (for demo purposes)
simulations = {}

class NumericalRequest(BaseModel):
    length: float
    nx: int
    alpha: float
    dt: float
    t_final: float
    u0: list  # Initial condition as list of floats
    bc_left: float
    bc_right: float
    save_every: Optional[int] = 1

class PINNRequest(BaseModel):
    alpha: float
    epochs: int = 5000
    lr: float = 1e-3
    # TODO: Add more config as needed

@app.post("/solve/numerical")
def solve_numerical(req: NumericalRequest):
    """
    Solve the 1D heat equation numerically.
    """
    def u_init(x):
        return np.array(req.u0)
    solver = HeatEquationSolver(
        length=req.length,
        nx=req.nx,
        alpha=req.alpha,
        dt=req.dt,
        t_final=req.t_final,
        u_init=u_init,
        bc_left=req.bc_left,
        bc_right=req.bc_right
    )
    sol = solver.solve(save_every=req.save_every)
    sim_id = str(uuid.uuid4())
    simulations[sim_id] = {"type": "numerical", "solution": sol.tolist()}
    return {"simulation_id": sim_id, "solution_shape": sol.shape}

@app.post("/solve/pinn")
def solve_pinn(req: PINNRequest):
    """
    Solve the 1D heat equation using a Physics-Informed Neural Network (PINN).
    """
    # Placeholder: actual data prep and training needed
    pinn = PINNHeatEquationSolver(alpha=req.alpha)
    # TODO: Prepare training data and call pinn.train(...)
    sim_id = str(uuid.uuid4())
    simulations[sim_id] = {"type": "pinn", "solution": None}  # Placeholder
    return {"simulation_id": sim_id, "message": "PINN training not yet implemented"}

@app.get("/visualize/{sim_id}")
def visualize(sim_id: str):
    """
    Visualize the simulation result as an animated plot or GIF.
    """
    if sim_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    sim = simulations[sim_id]
    if sim["type"] == "numerical":
        solution = np.array(sim["solution"])
        nt, nx = solution.shape
        # Reconstruct x and dt (assume uniform grid and time step for demo)
        x = np.linspace(0, 1, nx)
        dt = 0.01  # Placeholder, should be stored with simulation
        gif_path = f"/tmp/{sim_id}.gif"
        animate_heat_solution(solution, x, dt, save_path=gif_path)
        return FileResponse(gif_path, media_type="image/gif")
    return {"message": f"Visualization for {sim_id} not yet implemented"} 