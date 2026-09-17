from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from idm import idm_accel  # noqa: E402


def main() -> None:
    dt = 0.02
    T = 25.0
    n = int(T / dt)
    v, vp, s = 18.0, 20.0, 40.0
    t = np.linspace(0, T, n + 1)
    vs = np.zeros(n + 1)
    vps = np.zeros(n + 1)
    ss = np.zeros(n + 1)
    vs[0], vps[0], ss[0] = v, vp, s
    for k in range(n):
        ap = 0.0 if t[k] < 10.0 else (-3.0 if vp > 2.0 else 0.0)
        a = idm_accel(v, vp, s)
        v = max(v + dt * a, 0.0)
        vp = max(vp + dt * ap, 0.0)
        s = max(s + dt * (vp - v), 0.1)
        vs[k + 1], vps[k + 1], ss[k + 1] = v, vp, s
    print(f"min spacing = {ss.min():.2f} m")
    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(t, vs, "k-", t, vps, "k--")
    axes[0].legend(["ego", "lead"])
    axes[0].grid(True)
    axes[0].set_ylabel("m/s")
    axes[1].plot(t, ss, "k-")
    axes[1].grid(True)
    axes[1].set_ylabel("spacing (m)")
    axes[1].set_xlabel("t (s)")
    fig.suptitle("IDM car-following")
    fig.tight_layout()
    out = Path(__file__).with_name("idm_follow.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
