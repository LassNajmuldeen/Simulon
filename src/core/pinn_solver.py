import torch
import torch.nn as nn
import numpy as np

class PINNHeatEquationSolver:
    """
    Physics-Informed Neural Network (PINN) for the 1D Heat Equation:
        du/dt = alpha * d^2u/dx^2
    """
    def __init__(self, alpha, device=None, hidden_layers=3, hidden_dim=32):
        self.alpha = alpha
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.build_model(hidden_layers, hidden_dim).to(self.device)

    def build_model(self, hidden_layers, hidden_dim):
        layers = [nn.Linear(2, hidden_dim), nn.Tanh()]
        for _ in range(hidden_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.Tanh()]
        layers += [nn.Linear(hidden_dim, 1)]
        return nn.Sequential(*layers)

    def pde_residual(self, x, t):
        """Compute the PDE residual at (x, t)."""
        x = x.requires_grad_()
        t = t.requires_grad_()
        u = self.model(torch.cat([x, t], dim=1))
        u_t = torch.autograd.grad(u, t, grad_outputs=torch.ones_like(u), create_graph=True)[0]
        u_x = torch.autograd.grad(u, x, grad_outputs=torch.ones_like(u), create_graph=True)[0]
        u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u_x), create_graph=True)[0]
        return u_t - self.alpha * u_xx

    def loss(self, x_f, t_f, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc):
        # PDE residual loss (interior)
        f = self.pde_residual(x_f, t_f)
        loss_f = torch.mean(f**2)
        # Initial condition loss
        u_pred_ic = self.model(torch.cat([x_ic, t_ic], dim=1))
        loss_ic = torch.mean((u_pred_ic - u_ic)**2)
        # Boundary condition loss
        u_pred_bc = self.model(torch.cat([x_bc, t_bc], dim=1))
        loss_bc = torch.mean((u_pred_bc - u_bc)**2)
        return loss_f + loss_ic + loss_bc

    def train(self, x_f, t_f, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc, epochs=5000, lr=1e-3, verbose=100):
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        for epoch in range(1, epochs+1):
            optimizer.zero_grad()
            loss = self.loss(x_f, t_f, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc)
            loss.backward()
            optimizer.step()
            if verbose and epoch % verbose == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.6f}")
        return self.model

    def predict(self, x, t):
        self.model.eval()
        with torch.no_grad():
            xt = torch.cat([torch.tensor(x, dtype=torch.float32).unsqueeze(1),
                            torch.tensor(t, dtype=torch.float32).unsqueeze(1)], dim=1).to(self.device)
            u_pred = self.model(xt)
        return u_pred.cpu().numpy().flatten() 