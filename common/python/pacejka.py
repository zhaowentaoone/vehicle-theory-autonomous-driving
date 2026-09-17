"""Pacejka magic formula (pure slip)."""

from __future__ import annotations

import numpy as np


def pacejka(kappa: np.ndarray, B: float, C: float, D: float, E: float) -> np.ndarray:
    x = B * np.asarray(kappa, dtype=float)
    return D * np.sin(C * np.arctan(x - E * (x - np.arctan(x))))
