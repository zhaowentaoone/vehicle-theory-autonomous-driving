"""线性二自由度横向模型。状态 [vy, r]，输入 delta。"""

from __future__ import annotations

import numpy as np

from vehicle_params import VehicleParams, VEH


def lateral_AB(vx: float, veh: VehicleParams = VEH) -> tuple[np.ndarray, np.ndarray]:
    vx = max(float(vx), 1.0)
    m, Iz, lf, lr = veh.m, veh.Iz, veh.lf, veh.lr
    Cf, Cr = veh.Cf, veh.Cr
    A = np.array(
        [
            [-(Cf + Cr) / (m * vx), -vx - (Cf * lf - Cr * lr) / (m * vx)],
            [-(Cf * lf - Cr * lr) / (Iz * vx), -(Cf * lf**2 + Cr * lr**2) / (Iz * vx)],
        ]
    )
    B = np.array([[Cf / m], [Cf * lf / Iz]])
    return A, B


def kus(veh: VehicleParams = VEH) -> float:
    return veh.m / veh.L * (veh.lr / veh.Cf - veh.lf / veh.Cr)
