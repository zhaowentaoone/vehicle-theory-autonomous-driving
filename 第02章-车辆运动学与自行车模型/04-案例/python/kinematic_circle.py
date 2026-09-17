"""常转角开环：应走出半径 R = L / tan(delta) 的圆。"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from bicycle_kinematic import bicycle_euler  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def main() -> None:
    dt = 0.01
    T = 12.0
    v = 8.0
    delta = np.deg2rad(15.0)
    n = int(T / dt)
    x = np.array([0.0, 0.0, 0.0])
    traj = np.zeros((n + 1, 3))
    traj[0] = x
    for k in range(n):
        x = bicycle_euler(x, v, delta, dt, VEH.L)
        traj[k + 1] = x

    R_th = VEH.L / np.tan(delta)
    # 圆心在起步时的左侧：psi=0 时位于 (0, R)
    cx, cy = 0.0, R_th
    radii = np.hypot(traj[:, 0] - cx, traj[:, 1] - cy)
    print(f"L = {VEH.L:.3f} m, delta = 15 deg")
    print(f"theoretical R = {R_th:.3f} m")
    print(f"simulated R mean = {radii.mean():.3f} m, std = {radii.std():.4f} m")
    print(f"relative radius error = {abs(radii.mean() - R_th) / R_th * 100:.2f} %")

    t = np.linspace(0.0, T, n + 1)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    ax = axes[0]
    ax.plot(traj[:, 0], traj[:, 1], "k-")
    circ = plt.Circle((cx, cy), R_th, fill=False, ls="--", color="0.5", label="theory circle")
    ax.add_patch(circ)
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Open-loop kinematic bicycle")
    ax.legend()

    axes[1].plot(t, np.rad2deg(np.unwrap(traj[:, 2])), "k-")
    axes[1].set_xlabel("t (s)")
    axes[1].set_ylabel("yaw (deg)")
    axes[1].grid(True)
    axes[1].set_title("Yaw grows linearly at constant delta")
    fig.tight_layout()
    out = Path(__file__).with_name("kinematic_circle.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
