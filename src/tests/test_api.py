import numpy as np
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_solve_numerical_and_visualize(tmp_path):
    nx = 10
    u0 = [0.0] * nx
    req = {
        "length": 1.0,
        "nx": nx,
        "alpha": 0.01,
        "dt": 0.001,
        "t_final": 0.01,
        "u0": u0,
        "bc_left": 1.0,
        "bc_right": 0.0
    }
    # Test numerical solve
    response = client.post("/solve/numerical", json=req)
    assert response.status_code == 200
    data = response.json()
    assert "simulation_id" in data
    sim_id = data["simulation_id"]
    # Test visualization endpoint (should return GIF or message)
    response = client.get(f"/visualize/{sim_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/gif" 