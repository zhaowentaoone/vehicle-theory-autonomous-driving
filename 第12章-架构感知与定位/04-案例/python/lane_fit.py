from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    rng = np.random.default_rng(1)
    x = np.linspace(5.0, 40.0, 36)
    true_c1, true_c0 = 0.04, -0.3
    y_true = true_c1 * x + true_c0
    y_det = y_true + rng.normal(0.0, 0.15, size=x.shape)
    A = np.stack([x, np.ones_like(x)], axis=1)
    c1, c0 = np.linalg.lstsq(A, y_det, rcond=None)[0]
    print(f"true  c1={true_c1:.4f}, c0={true_c0:.4f}")
    print(f"fitted c1={c1:.4f}, c0={c0:.4f}")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y_true, "k--", label="true lane")
    ax.plot(x, y_det, "k.", label="detections")
    ax.plot(x, c1 * x + c0, "k-", label="fit")
    ax.set_xlabel("ahead x (m)")
    ax.set_ylabel("lateral y (m)")
    ax.grid(True)
    ax.legend()
    ax.set_title("Synthetic lane detection + polyfit")
    fig.tight_layout()
    out = Path(__file__).with_name("lane_fit.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
