import numpy as np

class HeatEquationSolver:
    """
    Solves the 1D heat equation using the explicit Euler finite-difference method.
    Equation: du/dt = alpha * d^2u/dx^2
    """
    def __init__(self, length, nx, alpha, dt, t_final, u_init, bc_left, bc_right):
        """
        length: Length of the rod (float)
        nx: Number of spatial grid points (int)
        alpha: Diffusion coefficient (float)
        dt: Time step (float)
        t_final: Final time (float)
        u_init: Initial condition function, u_init(x)
        bc_left: Boundary condition at x=0 (float or callable)
        bc_right: Boundary condition at x=L (float or callable)
        """
        self.length = length
        self.nx = nx
        self.alpha = alpha
        self.dt = dt
        self.t_final = t_final
        self.dx = length / (nx - 1)
        self.x = np.linspace(0, length, nx)
        self.u = u_init(self.x)
        self.bc_left = bc_left
        self.bc_right = bc_right
        self.nt = int(t_final / dt)

    def step(self):
        """Perform one time step using explicit Euler."""
        u_new = self.u.copy()
        for i in range(1, self.nx - 1):
            u_new[i] = self.u[i] + self.alpha * self.dt / self.dx**2 * (self.u[i+1] - 2*self.u[i] + self.u[i-1])
        # Apply boundary conditions
        u_new[0] = self.bc_left if not callable(self.bc_left) else self.bc_left()
        u_new[-1] = self.bc_right if not callable(self.bc_right) else self.bc_right()
        self.u = u_new

    def solve(self, save_every=1):
        """Solve the heat equation, returning the solution at each save interval."""
        solution = [self.u.copy()]
        for n in range(1, self.nt + 1):
            self.step()
            if n % save_every == 0:
                solution.append(self.u.copy())
        return np.array(solution) 