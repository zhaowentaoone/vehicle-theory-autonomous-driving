from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from bicycle_kinematic import bicycle_euler, wrap_to_pi  # noqa: E402
from dlqr import dlqr  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def path_at(X: float) -> tuple[float, float]:
    Y = 0.8 * np.sin(2 * np.pi * X / 80.0)
    dY = 0.8 * (2 * np.pi / 80.0) * np.cos(2 * np.pi * X / 80.0)
    psi = np.arctan(dY)
    return Y, psi


def main() -> None:
    v = 15.0
    dt = 0.05
    Ac = np.array([[0.0, v], [0.0, 0.0]])
    Bc = np.array([[0.0], [v / VEH.L]])
    A = np.eye(2) + Ac * dt
    B = Bc * dt
    Q = np.diag([4.0, 8.0])
    R = np.array([[1.0]])
    K = dlqr(A, B, Q, R)
    print("K =", K.ravel())

    x = np.array([0.0, 1.5, 0.0])  # start off the path
    T = 20.0
    n = int(T / dt)
    traj = np.zeros((n + 1, 3))
    eys = np.zeros(n + 1)
    traj[0] = x
    Yp, psip = path_at(x[0])
    eys[0] = x[1] - Yp
    for k in range(n):
        Yp, psip = path_at(x[0])
        ey = x[1] - Yp
        epsi = wrap_to_pi(x[2] - psip)
        delta = float(np.clip(-(K @ np.array([ey, epsi]))[0], -np.deg2rad(35), np.deg2rad(35)))
        x = bicycle_euler(x, v, delta, dt, VEH.L)
        traj[k + 1] = x
        eys[k + 1] = x[1] - path_at(x[0])[0]
    print(f"RMSE ey={np.sqrt(np.mean(eys**2)):.3f} m, final ey={eys[-1]:.3f} m")

    Xs = np.linspace(0, traj[-1, 0], 200)
    Ys = [path_at(X)[0] for X in Xs]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].plot(Xs, Ys, "k--", label="path")
    axes[0].plot(traj[:, 0], traj[:, 1], "k-", label="LQR")
    axes[0].set_aspect("equal")
    axes[0].grid(True)
    axes[0].legend()
    t = np.linspace(0, T, n + 1)
    axes[1].plot(t, eys, "k-")
    axes[1].set_xlabel("t (s)")
    axes[1].set_ylabel("ey (m)")
    axes[1].grid(True)
    fig.suptitle("Kinematic LQR lane keeping")
    fig.tight_layout()
    out = Path(__file__).with_name("lqr_lane.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
