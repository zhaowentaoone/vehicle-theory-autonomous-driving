"""平面刚体坐标变换，与 05-算法文档一致。"""

from __future__ import annotations

import numpy as np


def rot2(psi: float) -> np.ndarray:
    c, s = np.cos(psi), np.sin(psi)
    return np.array([[c, -s], [s, c]], dtype=float)


def body_to_inertial(origin, psi: float, p_body) -> np.ndarray:
    origin = np.asarray(origin, dtype=float).reshape(2)
    p_body = np.asarray(p_body, dtype=float).reshape(2)
    return origin + rot2(psi) @ p_body


def inertial_to_body(origin, psi: float, p_inertial) -> np.ndarray:
    origin = np.asarray(origin, dtype=float).reshape(2)
    p_inertial = np.asarray(p_inertial, dtype=float).reshape(2)
    return rot2(psi).T @ (p_inertial - origin)
