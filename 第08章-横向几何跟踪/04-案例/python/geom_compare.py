from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from bicycle_kinematic import bicycle_euler  # noqa: E402
from geom_track import make_path, nearest_index, pure_pursuit, signed_ey, stanley  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def run(name: str, ctrl, v: float = 12.0, dt: float = 0.02, T: float = 18.0):
    path = make_path()
    x = np.array([0.0, 1.2, 0.0])  # 故意横向偏置
    n = int(T / dt)
    traj = np.zeros((n + 1, 3))
    eys = np.zeros(n + 1)
    traj[0] = x
    idx = 0
    eys[0] = signed_ey(x[:2], path[0, :2], path[0, 2])
    for k in range(n):
        delta, idx = ctrl(x, path, idx)
        x = bicycle_euler(x, v, delta, dt, VEH.L)
        traj[k + 1] = x
        i = nearest_index(x[:2], path, idx)
        eys[k + 1] = signed_ey(x[:2], path[i, :2], path[i, 2])
    rmse = float(np.sqrt(np.mean(eys**2)))
    print(f"{name}: lateral RMSE = {rmse:.3f} m, max |ey| = {np.max(np.abs(eys)):.3f} m")
    return path, traj, eys, rmse


def main() -> None:
    def pp(x, path, idx):
        return pure_pursuit(x, path, VEH.L, ld=2.0 + 0.3 * 12.0, idx=idx)

    def st(x, path, idx):
        return stanley(x, path, VEH.L, k=2.2, v=12.0, idx=idx)

    path, t1, e1, _ = run("Pure Pursuit", pp)
    _, t2, e2, _ = run("Stanley", st)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    axes[0].plot(path[:, 0], path[:, 1], "k--", lw=1, label="path")
    axes[0].plot(t1[:, 0], t1[:, 1], "k-", label="PP")
    axes[0].plot(t2[:, 0], t2[:, 1], color="0.5", label="Stanley")
    axes[0].set_aspect("equal")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_xlabel("X (m)")
    axes[0].set_ylabel("Y (m)")
    t = np.linspace(0, 18, len(e1))
    axes[1].plot(t, e1, "k-", label="PP")
    axes[1].plot(t, e2, color="0.5", label="Stanley")
    axes[1].set_xlabel("t (s)")
    axes[1].set_ylabel("ey (m)")
    axes[1].grid(True)
    axes[1].legend()
    fig.suptitle("Geometric tracking")
    fig.tight_layout()
    out = Path(__file__).with_name("geom_compare.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
