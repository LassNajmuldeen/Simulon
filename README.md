# Simulon: Scientific Simulation API

Simulon is an open-source backend and interactive API for simulating and visualizing scientific phenomena, starting with the 1D Heat Equation. It supports both classical numerical solvers and Physics-Informed Neural Networks (PINNs).

## Features
- Solve the 1D Heat Equation numerically (finite-difference)
- (Planned) Solve with PINNs (PyTorch)
- REST API for simulation and visualization
- Animated visualizations (coming soon)
- Full test coverage (coming soon)

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running the API
```bash
uvicorn src.api.main:app --reload
```

## API Endpoints
- `POST /solve/numerical` — Solve the heat equation numerically
- `POST /solve/pinn` — Solve with a PINN (WIP)
- `GET /visualize/{id}` — Visualize a simulation (WIP)

## Example Request (Numerical)
```json
{
  "length": 1.0,
  "nx": 50,
  "alpha": 0.01,
  "dt": 0.001,
  "t_final": 0.1,
  "u0": [0, 0, ..., 0],
  "bc_left": 0.0,
  "bc_right": 1.0
}
```

## License
MIT
