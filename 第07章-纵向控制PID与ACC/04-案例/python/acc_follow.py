from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))


def main() -> None:
    dt = 0.01
    T = 25.0
    n = int(T / dt)
    h, s0 = 1.4, 5.0
    Ks, Kv = 0.25, 0.9
    v = 18.0
    vp = 20.0
    s = 40.0
    t = np.linspace(0.0, T, n + 1)
    ss = np.zeros(n + 1)
    vs = np.zeros(n + 1)
    vps = np.zeros(n + 1)
    ss[0], vs[0], vps[0] = s, v, vp
    for k in range(n):
        ap = 0.0 if t[k] < 8.0 else (-2.0 if vp > 10.0 else 0.0)
        s_des = s0 + h * v
        a = Ks * (s - s_des) + Kv * (vp - v)
        a = float(np.clip(a, -5.0, 2.0))
        v = max(v + dt * a, 0.0)
        vp = max(vp + dt * ap, 0.0)
        s = s + dt * (vp - v)
        ss[k + 1], vs[k + 1], vps[k + 1] = s, v, vp
    print(f"min spacing = {ss.min():.2f} m, final spacing = {ss[-1]:.2f} m")

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(t, vs, "k-", label="ego")
    axes[0].plot(t, vps, "k--", label="lead")
    axes[0].set_ylabel("m/s")
    axes[0].legend()
    axes[0].grid(True)
    axes[1].plot(t, ss, "k-")
    axes[1].plot(t, s0 + h * vs, "k--", label="s_des")
    axes[1].set_ylabel("spacing (m)")
    axes[1].set_xlabel("t (s)")
    axes[1].legend()
    axes[1].grid(True)
    fig.suptitle("ACC constant time-gap")
    fig.tight_layout()
    out = Path(__file__).with_name("acc_follow.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
