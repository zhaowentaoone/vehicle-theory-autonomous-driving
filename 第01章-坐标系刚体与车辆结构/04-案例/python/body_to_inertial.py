"""车体系矩形、轴心 → 惯性系并绘图。"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from vehicle_params import VEH  # noqa: E402


def rot2(psi: float) -> np.ndarray:
    c, s = np.cos(psi), np.sin(psi)
    return np.array([[c, -s], [s, c]])


def body_to_inertial(origin: np.ndarray, psi: float, pts_body: np.ndarray) -> np.ndarray:
    """pts_body: (2, N) or (N, 2) -> 返回 (N, 2) 惯性坐标。"""
    pts = np.asarray(pts_body, dtype=float)
    if pts.ndim != 2:
        raise ValueError("pts_body must be 2D")
    if pts.shape[0] == 2 and pts.shape[1] != 2:
        pts = pts.T
    R = rot2(psi)
    return origin.reshape(1, 2) + pts @ R.T


def main() -> None:
    origin = np.array([0.0, 0.0])
    psi_deg = 35.0
    psi = np.deg2rad(psi_deg)

    length, width = 4.5, 1.8
    half_l, half_w = length / 2.0, width / 2.0
    corners_body = np.array(
        [
            [half_l, half_w],
            [half_l, -half_w],
            [-half_l, -half_w],
            [-half_l, half_w],
            [half_l, half_w],
        ]
    )
    front_axle = np.array([[VEH.lf, 0.0]])
    rear_axle = np.array([[-VEH.lr, 0.0]])

    corners_i = body_to_inertial(origin, psi, corners_body)
    fa_i = body_to_inertial(origin, psi, front_axle)[0]
    ra_i = body_to_inertial(origin, psi, rear_axle)[0]
    heading = origin + rot2(psi) @ np.array([2.5, 0.0])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(corners_i[:, 0], corners_i[:, 1], "k-", lw=2, label="body")
    ax.plot(origin[0], origin[1], "ko", label="CG")
    ax.plot(fa_i[0], fa_i[1], "r^", ms=10, label="front axle")
    ax.plot(ra_i[0], ra_i[1], "bs", ms=10, label="rear axle")
    ax.annotate(
        "",
        xy=heading,
        xytext=origin,
        arrowprops=dict(arrowstyle="->", color="0.3", lw=1.5),
    )
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title(f"Body rectangle in inertial frame, psi={psi_deg:.0f} deg")
    ax.legend(loc="upper left")
    fig.tight_layout()
    out = Path(__file__).with_name("body_to_inertial.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
