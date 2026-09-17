from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from bicycle_kinematic import bicycle_euler, wrap_to_pi  # noqa: E402
from vehicle_params import VEH  # noqa: E402


def path_at(X: float) -> tuple[float, float]:
    Y = 0.7 * np.sin(2 * np.pi * X / 90.0)
    dY = 0.7 * (2 * np.pi / 90.0) * np.cos(2 * np.pi * X / 90.0)
    return Y, np.arctan(dY)


def stanley_delta(x: np.ndarray, k: float = 2.0, v: float = 12.0) -> float:
    Yp, psip = path_at(x[0])
    ey = x[1] - Yp
    epsi = wrap_to_pi(psip - x[2])  # 路径切向减航向，与第08章 Stanley 一致
    delta = epsi - np.arctan(k * ey / (v + 0.1))
    return float(np.clip(delta, -np.deg2rad(35), np.deg2rad(35)))


def acc_a(s: float, v: float, vp: float, h: float = 1.4, s0: float = 6.0) -> float:
    sdes = s0 + h * v
    a = 0.25 * (s - sdes) + 0.9 * (vp - v)
    return float(np.clip(a, -5.0, 2.0))


def simulate(use_acc: bool = True, use_lka: bool = True, dt: float = 0.02, T: float = 25.0):
    n = int(T / dt)
    x = np.array([0.0, path_at(0.0)[0] + 0.4, 0.0])
    v = 12.0
    vp = 13.0
    xp = 28.0
    Lveh = 4.5
    rec = np.zeros((n, 6))
    for k in range(n):
        t = k * dt
        ap = 0.0 if t < 10.0 else (-2.5 if vp > 6.0 else 0.0)
        s = xp - x[0] - Lveh
        a = acc_a(s, v, vp) if use_acc else 0.0
        delta = stanley_delta(x, v=v) if use_lka else 0.0
        v = max(v + dt * a, 0.5)
        vp = max(vp + dt * ap, 0.0)
        xp += dt * vp
        x = bicycle_euler(x, v, delta, dt, VEH.L)
        Yp, _ = path_at(x[0])
        rec[k] = [t, x[0], x[1] - Yp, s, v, vp]
    return rec


def metrics(rec: np.ndarray) -> dict:
    return {
        "s_min": float(rec[:, 3].min()),
        "ey_rmse": float(np.sqrt(np.mean(rec[:, 2] ** 2))),
        "ey_max": float(np.max(np.abs(rec[:, 2]))),
    }


def main() -> None:
    full = simulate(True, True)
    no_lka = simulate(True, False)
    no_acc = simulate(False, True)
    for name, rec in [("full", full), ("no_LKA", no_lka), ("no_ACC", no_acc)]:
        m = metrics(rec)
        print(f"{name:8s}  s_min={m['s_min']:.2f} m  eyRMSE={m['ey_rmse']:.3f} m  |ey|max={m['ey_max']:.3f}")

    fig, axes = plt.subplots(3, 1, figsize=(8, 7), sharex=True)
    axes[0].plot(full[:, 0], full[:, 4], "k-", full[:, 0], full[:, 5], "k--")
    axes[0].legend(["ego v", "lead v"])
    axes[0].grid(True)
    axes[0].set_ylabel("m/s")
    axes[1].plot(full[:, 0], full[:, 3], "k-")
    axes[1].grid(True)
    axes[1].set_ylabel("spacing (m)")
    axes[2].plot(full[:, 0], full[:, 2], "k-", label="full")
    axes[2].plot(no_lka[:, 0], no_lka[:, 2], color="0.5", label="no LKA")
    axes[2].grid(True)
    axes[2].legend()
    axes[2].set_ylabel("ey (m)")
    axes[2].set_xlabel("t (s)")
    fig.suptitle("Project A: ACC + LKA")
    fig.tight_layout()
    out = Path(__file__).with_name("acc_lka.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
