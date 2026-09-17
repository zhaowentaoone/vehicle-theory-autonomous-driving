from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from vehicle_params import VEH  # noqa: E402


def forces(v: float, Fx: float) -> float:
    Froll = VEH.m * VEH.g * VEH.fr
    Faero = 0.5 * VEH.rho * VEH.Cd * VEH.Af * v * abs(v)
    return Fx - Froll - Faero


def main() -> None:
    dt = 0.01
    Fx_max, Fx_min = 4000.0, -VEH.m * 0.7 * VEH.g
    v = 0.0
    t, vs, xs = [0.0], [0.0], [0.0]
    x = 0.0
    phase = "accel"
    t_100 = None
    s_brake_start = None
    while t[-1] < 40.0:
        if phase == "accel":
            Fx = Fx_max
            if v >= 28.0:
                phase = "brake"
                s_brake_start = x
        else:
            Fx = Fx_min
        ax = forces(v, Fx) / VEH.m
        v = max(v + dt * ax, 0.0)
        x += dt * v
        t.append(t[-1] + dt)
        vs.append(v)
        xs.append(x)
        if t_100 is None and v >= 100.0 / 3.6:
            t_100 = t[-1]
        if phase == "brake" and v <= 0.05:
            break

    vkmh = np.array(vs) * 3.6
    print(f"0-100 km/h time ≈ {t_100:.2f} s" if t_100 else "did not reach 100 km/h")
    if s_brake_start is not None:
        print(f"brake distance from {vs[int(np.argmax(vs))]*3.6:.1f} km/h: {xs[-1]-s_brake_start:.1f} m")

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(t, vkmh, "k-")
    axes[0].set_ylabel("speed (km/h)")
    axes[0].grid(True)
    axes[1].plot(t, xs, "k-")
    axes[1].set_xlabel("t (s)")
    axes[1].set_ylabel("distance (m)")
    axes[1].grid(True)
    fig.suptitle("Longitudinal accel then brake")
    fig.tight_layout()
    out = Path(__file__).with_name("longitudinal_sim.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
