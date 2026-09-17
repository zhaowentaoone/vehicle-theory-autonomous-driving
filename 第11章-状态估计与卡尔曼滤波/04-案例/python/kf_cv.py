from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from kalman import kf_predict, kf_update  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(0)
    dt = 0.05
    A = np.array([[1.0, dt], [0.0, 1.0]])
    C = np.array([[1.0, 0.0]])
    Q = np.diag([0.01, 0.8]) * dt
    R = np.array([[4.0]])
    T = 20.0
    n = int(T / dt)
    p_true = 0.0
    v_true = 10.0
    x = np.array([0.0, 8.0])
    P = np.diag([10.0, 10.0])
    ts = np.linspace(0, T, n)
    rec = np.zeros((n, 5))
    for k in range(n):
        if ts[k] >= 8.0:
            v_true = 16.0
        p_true += dt * v_true
        y = p_true + rng.normal(0.0, 2.0)
        x, P = kf_predict(x, P, A, Q)
        x, P, _ = kf_update(x, P, y, C, R)
        rec[k] = [p_true, v_true, y, x[0], x[1]]
    print(f"pos RMSE meas={np.sqrt(np.mean((rec[:,2]-rec[:,0])**2)):.3f}  kf={np.sqrt(np.mean((rec[:,3]-rec[:,0])**2)):.3f}")
    print(f"vel RMSE kf={np.sqrt(np.mean((rec[:,4]-rec[:,1])**2)):.3f}")

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(ts, rec[:, 2], ".", ms=3, color="0.6", label="meas")
    axes[0].plot(ts, rec[:, 0], "k--", label="true p")
    axes[0].plot(ts, rec[:, 3], "k-", label="kf p")
    axes[0].legend()
    axes[0].grid(True)
    axes[0].set_ylabel("position (m)")
    axes[1].plot(ts, rec[:, 1], "k--", label="true v")
    axes[1].plot(ts, rec[:, 4], "k-", label="kf v")
    axes[1].legend()
    axes[1].grid(True)
    axes[1].set_ylabel("velocity (m/s)")
    axes[1].set_xlabel("t (s)")
    fig.suptitle("Constant-velocity Kalman filter")
    fig.tight_layout()
    out = Path(__file__).with_name("kf_cv.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
