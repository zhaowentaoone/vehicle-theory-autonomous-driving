from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from pacejka import pacejka  # noqa: E402

# Match linear stiffness ~ 80000 N/rad: B*C*D = 80000
B, C, D, E = 8.0, 1.25, 8000.0, 0.4


def main() -> None:
    alpha_deg = np.linspace(-15.0, 15.0, 400)
    alpha = np.deg2rad(alpha_deg)
    Fy = pacejka(alpha, B, C, D, E)
    slope = B * C * D
    Fy_lin = slope * alpha

    sigma = np.linspace(-0.2, 0.2, 400)
    Fx = pacejka(sigma, B, C, D, E)

    i_peak = int(np.argmax(Fy))
    print(f"BCD (cornering stiffness) = {slope:.0f} N/rad")
    print(f"peak Fy = {Fy[i_peak]:.0f} N at alpha = {alpha_deg[i_peak]:.2f} deg")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].plot(alpha_deg, Fy, "k-", label="Pacejka")
    axes[0].plot(alpha_deg, Fy_lin, "k--", label="linear BCD*alpha")
    axes[0].set_xlabel("alpha (deg)")
    axes[0].set_ylabel("Fy (N)")
    axes[0].set_title("Pure cornering")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_ylim(-9000, 9000)

    axes[1].plot(sigma, Fx, "k-")
    axes[1].set_xlabel("longitudinal slip sigma")
    axes[1].set_ylabel("Fx (N)")
    axes[1].set_title("Pure longitudinal")
    axes[1].grid(True)
    fig.tight_layout()
    out = Path(__file__).with_name("pacejka_curves.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
