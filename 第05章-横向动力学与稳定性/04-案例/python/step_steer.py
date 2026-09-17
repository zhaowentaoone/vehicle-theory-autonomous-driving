from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from lateral_2dof import kus, lateral_AB  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def simulate(vx: float, delta: float, T: float = 5.0, dt: float = 0.01):
    A, B = lateral_AB(vx)
    n = int(T / dt)
    x = np.zeros(2)
    xs = np.zeros((n + 1, 2))
    for k in range(n):
        x = x + dt * (A @ x + B.ravel() * delta)
        xs[k + 1] = x
    t = np.linspace(0.0, T, n + 1)
    return t, xs


def main() -> None:
    delta = np.deg2rad(3.0)
    print(f"K_us = {kus():.4e} rad/(m/s^2)  (>0 understeer)")
    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    for vx, style in [(10.0, "-"), (20.0, "--"), (30.0, ":")]:
        t, xs = simulate(vx, delta)
        beta = xs[:, 0] / vx
        axes[0].plot(t, np.rad2deg(xs[:, 1]), "k" + style, label=f"vx={vx:.0f}")
        axes[1].plot(t, np.rad2deg(beta), "k" + style)
        print(f"vx={vx:.0f} m/s  steady r={xs[-1,1]:.3f} rad/s  beta={np.rad2deg(beta[-1]):.2f} deg")
    axes[0].set_ylabel("yaw rate r (deg/s)")
    axes[0].grid(True)
    axes[0].legend()
    axes[1].set_ylabel("beta (deg)")
    axes[1].set_xlabel("t (s)")
    axes[1].grid(True)
    fig.suptitle("Step steer 3 deg, linear 2DOF")
    fig.tight_layout()
    out = Path(__file__).with_name("step_steer.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
