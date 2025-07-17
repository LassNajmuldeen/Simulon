import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def animate_heat_solution(solution, x, dt, save_path=None, fps=20):
    """
    Animate the evolution of the 1D heat equation solution.

    Parameters:
        solution: np.ndarray, shape (nt, nx) - Solution array over time
        x: np.ndarray, shape (nx,) - Spatial grid
        dt: float - Time step between frames
        save_path: str or None - If provided, save animation as GIF/MP4
        fps: int - Frames per second for animation
    Returns:
        anim: matplotlib.animation.FuncAnimation object
    """
    nt, nx = solution.shape
    fig, ax = plt.subplots()
    line, = ax.plot(x, solution[0], color='r')
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(np.min(solution), np.max(solution))
    ax.set_xlabel('x')
    ax.set_ylabel('u(x, t)')
    ax.set_title('1D Heat Equation Evolution')

    def update(frame):
        line.set_ydata(solution[frame])
        ax.set_title(f"1D Heat Equation Evolution\nTime: {frame*dt:.3f}s")
        return line,

    anim = FuncAnimation(fig, update, frames=nt, interval=1000/fps, blit=True)

    if save_path:
        if save_path.endswith('.gif'):
            anim.save(save_path, writer=PillowWriter(fps=fps))
        else:
            anim.save(save_path, fps=fps)
    return anim 