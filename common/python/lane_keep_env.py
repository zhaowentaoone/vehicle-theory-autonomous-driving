"""最小车道保持环境：观测 [ey, epsi, v]，动作 delta（rad）。"""

from __future__ import annotations

import numpy as np

from bicycle_kinematic import bicycle_euler, wrap_to_pi
from vehicle_params import VEH


class LaneKeepEnv:
    def __init__(self, dt: float = 0.05, v: float = 12.0, max_steps: int = 200):
        self.dt = dt
        self.v = v
        self.max_steps = max_steps
        self.delta_max = np.deg2rad(35.0)
        self.x = np.zeros(3)
        self.t_step = 0
        self.rng = np.random.default_rng(0)

    def _path(self, X: float) -> tuple[float, float]:
        Y = 0.6 * np.sin(2 * np.pi * X / 70.0)
        dY = 0.6 * (2 * np.pi / 70.0) * np.cos(2 * np.pi * X / 70.0)
        return Y, np.arctan(dY)

    def _obs_err(self) -> tuple[float, float]:
        Yp, psip = self._path(self.x[0])
        ey = self.x[1] - Yp
        epsi = wrap_to_pi(self.x[2] - psip)
        return ey, epsi

    def reset(self, seed: int | None = None) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        ey0 = self.rng.uniform(-0.5, 0.5)
        epsi0 = self.rng.uniform(-0.1, 0.1)
        Yp, psip = self._path(0.0)
        self.x = np.array([0.0, Yp + ey0, wrap_to_pi(psip + epsi0)])
        self.t_step = 0
        ey, epsi = self._obs_err()
        return np.array([ey, epsi, self.v], dtype=float)

    def step(self, delta: float) -> tuple[np.ndarray, float, bool, dict]:
        delta = float(np.clip(delta, -self.delta_max, self.delta_max))
        self.x = bicycle_euler(self.x, self.v, delta, self.dt, VEH.L)
        self.t_step += 1
        ey, epsi = self._obs_err()
        r = -ey**2 - 0.5 * epsi**2 - 0.05 * delta**2 + 0.05
        done = abs(ey) > 2.5 or self.t_step >= self.max_steps
        if abs(ey) > 2.5:
            r -= 10.0
        obs = np.array([ey, epsi, self.v], dtype=float)
        return obs, float(r), done, {"ey": ey, "epsi": epsi}
