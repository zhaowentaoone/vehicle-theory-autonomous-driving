from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from lateral_2dof import lateral_AB  # noqa: E402


def step_second_order(zeta: float, wn: float = 4.0, T: float = 5.0, dt: float = 0.001):
    n = int(T / dt)
    y = 0.0
    yd = 0.0
    ys = np.zeros(n + 1)
    for k in range(n):
        ydd = wn**2 * (1.0 - y) - 2 * zeta * wn * yd
        yd += dt * ydd
        y += dt * yd
        ys[k + 1] = y
    t = np.linspace(0.0, T, n + 1)
    return t, ys


def main() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    for zeta, ls in [(0.3, "-"), (0.7, "--"), (1.2, ":")]:
        t, y = step_second_order(zeta)
        ax.plot(t, y, "k" + ls, label=f"zeta={zeta}")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()
    ax.set_title("Second-order step response")
    fig.tight_layout()
    out = Path(__file__).with_name("step_response.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")

    for vx in (10.0, 20.0, 30.0):
        A, _ = lateral_AB(vx)
        eigs = np.linalg.eigvals(A)
        print(f"vx={vx:.0f}  poles = {eigs}")
    plt.show()


if __name__ == "__main__":
    main()
