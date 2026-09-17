"""Intelligent Driver Model 加速度。"""

from __future__ import annotations

import numpy as np


def idm_accel(v: float, vp: float, s: float, v0: float = 25.0, T: float = 1.4,
              amax: float = 1.4, b: float = 2.0, s0: float = 4.0, delta: float = 4.0) -> float:
    dv = v - vp
    s_star = s0 + max(0.0, v * T + v * dv / (2.0 * np.sqrt(amax * b)))
    a = amax * (1.0 - (v / max(v0, 0.1)) ** delta - (s_star / max(s, 0.2)) ** 2)
    return float(np.clip(a, -6.0, amax))
