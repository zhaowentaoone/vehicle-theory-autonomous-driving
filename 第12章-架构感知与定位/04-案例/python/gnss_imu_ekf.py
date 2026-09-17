from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from bicycle_kinematic import bicycle_euler, wrap_to_pi  # noqa: E402
from kalman import kf_update  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(2)
    dt = 0.05
    T = 20.0
    n = int(T / dt)
    x_true = np.array([0.0, 0.0, 0.0])
    v = 12.0
    x_hat = np.array([0.5, -0.5, 0.1])
    P = np.diag([9.0, 9.0, 0.2])
    Q = np.diag([0.05, 0.05, 0.002]) * dt
    R = np.diag([4.0, 4.0])
    C = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    traj_t = np.zeros((n, 2))
    traj_g = np.zeros((n, 2))
    traj_e = np.zeros((n, 2))
    openloop = x_hat.copy()
    traj_o = np.zeros((n, 2))
    for k in range(n):
        delta = np.deg2rad(4.0) * np.sin(2 * np.pi * k * dt / 12.0)
        x_true = bicycle_euler(x_true, v, delta, dt, VEH.L)
        r_meas = (v / VEH.L) * np.tan(delta) + rng.normal(0.0, 0.02)
        # IMU-driven prediction (v, r)
        psi = x_hat[2]
        A = np.array(
            [
                [1.0, 0.0, -v * dt * np.sin(psi)],
                [0.0, 1.0, v * dt * np.cos(psi)],
                [0.0, 0.0, 1.0],
            ]
        )
        x_hat = x_hat + np.array([v * dt * np.cos(psi), v * dt * np.sin(psi), r_meas * dt])
        x_hat[2] = wrap_to_pi(x_hat[2])
        P = A @ P @ A.T + Q
        openloop = openloop + np.array(
            [v * dt * np.cos(openloop[2]), v * dt * np.sin(openloop[2]), r_meas * dt]
        )
        y = x_true[:2] + rng.normal(0.0, 2.0, size=2)
        x_hat, P, _ = kf_update(x_hat, P, y, C, R)
        x_hat[2] = wrap_to_pi(x_hat[2])
        traj_t[k] = x_true[:2]
        traj_g[k] = y
        traj_e[k] = x_hat[:2]
        traj_o[k] = openloop[:2]
    rmse_g = np.sqrt(np.mean(np.sum((traj_g - traj_t) ** 2, axis=1)))
    rmse_e = np.sqrt(np.mean(np.sum((traj_e - traj_t) ** 2, axis=1)))
    print(f"GNSS RMSE={rmse_g:.3f} m  EKF RMSE={rmse_e:.3f} m")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(traj_t[:, 0], traj_t[:, 1], "k-", label="true")
    ax.plot(traj_g[:, 0], traj_g[:, 1], ".", color="0.6", ms=3, label="GNSS")
    ax.plot(traj_e[:, 0], traj_e[:, 1], "k--", label="EKF")
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()
    ax.set_title("GNSS + yaw-rate EKF")
    fig.tight_layout()
    out = Path(__file__).with_name("gnss_imu_ekf.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
