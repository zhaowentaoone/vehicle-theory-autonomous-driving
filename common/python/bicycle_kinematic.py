"""后轴运动学自行车：欧拉一步与精确圆弧一步。"""

from __future__ import annotations

import numpy as np


def wrap_to_pi(angle: float) -> float:
    a = (angle + np.pi) % (2.0 * np.pi) - np.pi
    return a


def bicycle_euler(x: np.ndarray, v: float, delta: float, dt: float, L: float,
                  delta_max: float = np.deg2rad(35.0)) -> np.ndarray:
    X, Y, psi = x
    delta = float(np.clip(delta, -delta_max, delta_max))
    X = X + dt * v * np.cos(psi)
    Y = Y + dt * v * np.sin(psi)
    psi = wrap_to_pi(psi + dt * v / L * np.tan(delta))
    return np.array([X, Y, psi], dtype=float)


def bicycle_exact(x: np.ndarray, v: float, delta: float, dt: float, L: float,
                  delta_max: float = np.deg2rad(35.0), eps: float = 1e-6) -> np.ndarray:
    X, Y, psi = x
    delta = float(np.clip(delta, -delta_max, delta_max))
    if abs(delta) < eps:
        return bicycle_euler(x, v, 0.0, dt, L, delta_max)
    R = L / np.tan(delta)
    dpsi = v * dt / R
    X = X + R * (np.sin(psi + dpsi) - np.sin(psi))
    Y = Y + R * (-np.cos(psi + dpsi) + np.cos(psi))
    psi = wrap_to_pi(psi + dpsi)
    return np.array([X, Y, psi], dtype=float)
