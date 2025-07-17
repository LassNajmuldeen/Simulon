import numpy as np
import pytest
from src.core.heat_solver import HeatEquationSolver

def test_boundary_conditions():
    length = 1.0
    nx = 10
    alpha = 0.01
    dt = 0.001
    t_final = 0.01
    u0 = lambda x: np.zeros_like(x)
    bc_left = 1.0
    bc_right = 0.0
    solver = HeatEquationSolver(length, nx, alpha, dt, t_final, u0, bc_left, bc_right)
    sol = solver.solve()
    # Check that boundaries are enforced at all times
    assert np.allclose(sol[:, 0], bc_left)
    assert np.allclose(sol[:, -1], bc_right)

def test_stability():
    length = 1.0
    nx = 10
    alpha = 0.01
    dt = 0.0001  # Small dt for stability
    t_final = 0.01
    u0 = lambda x: np.sin(np.pi * x)
    bc_left = 0.0
    bc_right = 0.0
    solver = HeatEquationSolver(length, nx, alpha, dt, t_final, u0, bc_left, bc_right)
    sol = solver.solve()
    # Solution should not blow up
    assert np.all(np.abs(sol) < 10)

def test_convergence_to_analytic():
    length = 1.0
    nx = 50
    alpha = 0.01
    dt = 0.0005
    t_final = 0.05
    u0 = lambda x: np.sin(np.pi * x)
    bc_left = 0.0
    bc_right = 0.0
    solver = HeatEquationSolver(length, nx, alpha, dt, t_final, u0, bc_left, bc_right)
    sol = solver.solve()
    x = np.linspace(0, length, nx)
    u_exact = np.exp(-alpha * np.pi**2 * t_final) * np.sin(np.pi * x)
    # Compare final time step to analytic solution
    assert np.allclose(sol[-1], u_exact, atol=0.05) 