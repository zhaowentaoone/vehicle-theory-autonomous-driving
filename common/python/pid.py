"""离散 PID，条件积分抗饱和。"""

from __future__ import annotations


class PID:
    def __init__(self, kp: float, ki: float, kd: float, umin: float, umax: float):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.umin, self.umax = umin, umax
        self.I = 0.0
        self.e_prev = 0.0

    def reset(self) -> None:
        self.I = 0.0
        self.e_prev = 0.0

    def step(self, e: float, dt: float) -> float:
        self.I += e * dt
        d = (e - self.e_prev) / dt if dt > 0 else 0.0
        u = self.kp * e + self.ki * self.I + self.kd * d
        u_sat = max(self.umin, min(self.umax, u))
        if u != u_sat:
            self.I -= e * dt
        self.e_prev = e
        return u_sat
