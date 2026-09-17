from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from bicycle_kinematic import bicycle_euler, wrap_to_pi  # noqa: E402
from linear_mpc import mpc_step  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def path_at(X: float) -> tuple[float, float]:
    Y = 0.8 * np.sin(2 * np.pi * X / 80.0)
    dY = 0.8 * (2 * np.pi / 80.0) * np.cos(2 * np.pi * X / 80.0)
    return Y, np.arctan(dY)


def main() -> None:
    v = 15.0
    dt = 0.05
    N = 12
    Ac = np.array([[0.0, v], [0.0, 0.0]])
    Bc = np.array([[0.0], [v / VEH.L]])
    A = np.eye(2) + Ac * dt
    B = Bc * dt
    Q = np.diag([6.0, 10.0])
    R = 1.5
    dmax = np.deg2rad(8.0)
    dumax = np.deg2rad(4.0)

    x = np.array([0.0, 1.5, 0.0])
    T = 20.0
    n = int(T / dt)
    traj = np.zeros((n + 1, 3))
    eys = np.zeros(n + 1)
    deltas = np.zeros(n)
    traj[0] = x
    eys[0] = x[1] - path_at(x[0])[0]
    u_prev = 0.0
    sat = 0
    for k in range(n):
        Yp, psip = path_at(x[0])
        ey = x[1] - Yp
        epsi = wrap_to_pi(x[2] - psip)
        U = mpc_step(np.array([ey, epsi]), A, B, Q, R, N, -dmax, dmax, dumax, u_prev)
        delta = float(U[0])
        if abs(abs(delta) - dmax) < 1e-4:
            sat += 1
        deltas[k] = delta
        u_prev = delta
        x = bicycle_euler(x, v, delta, dt, VEH.L)
        traj[k + 1] = x
        eys[k + 1] = x[1] - path_at(x[0])[0]
    print(f"RMSE ey={np.sqrt(np.mean(eys**2)):.3f} m, sat_frac={sat/n:.2f}")

    Xs = np.linspace(0, traj[-1, 0], 200)
    Ys = [path_at(X)[0] for X in Xs]
    t = np.linspace(0, T, n + 1)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].plot(Xs, Ys, "k--", traj[:, 0], traj[:, 1], "k-")
    axes[0].set_aspect("equal")
    axes[0].grid(True)
    axes[0].set_title("MPC vs path")
    axes[1].plot(t, eys, "k-")
    axes[1].set_xlabel("t (s)")
    axes[1].set_ylabel("ey (m)")
    axes[1].grid(True)
    fig.tight_layout()
    out = Path(__file__).with_name("mpc_lane.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
