from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from pid import PID  # noqa: E402


def main() -> None:
    dt = 0.01
    T = 15.0
    n = int(T / dt)
    pid = PID(kp=0.8, ki=0.25, kd=0.0, umin=-4.0, umax=2.0)
    v = 10.0
    tau = 0.3
    a = 0.0
    ts = np.linspace(0.0, T, n + 1)
    vs = np.zeros(n + 1)
    refs = np.zeros(n + 1)
    vs[0] = v
    for k in range(n):
        vref = 15.0 if ts[k] < 4.0 else 25.0
        refs[k] = vref
        ades = pid.step(vref - v, dt)
        a += dt * (ades - a) / tau
        v += dt * a
        vs[k + 1] = v
    refs[-1] = refs[-2]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ts, vs, "k-", label="v")
    ax.plot(ts, refs, "k--", label="v_ref")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("m/s")
    ax.grid(True)
    ax.legend()
    ax.set_title("Cruise PI")
    fig.tight_layout()
    out = Path(__file__).with_name("cruise_pid.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
