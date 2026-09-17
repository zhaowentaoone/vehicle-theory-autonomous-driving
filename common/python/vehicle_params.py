"""教学用紧凑型轿车参数。全书案例默认引用本文件。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleParams:
    m: float = 1500.0  # kg
    Iz: float = 2250.0  # kg*m^2
    lf: float = 1.2  # m
    lr: float = 1.6  # m
    Cf: float = 80000.0  # N/rad 前轴侧偏刚度
    Cr: float = 80000.0  # N/rad 后轴侧偏刚度
    Re: float = 0.30  # m 有效滚动半径
    Cd: float = 0.30  # 空气阻力系数
    Af: float = 2.2  # m^2 迎风面积
    rho: float = 1.225  # kg/m^3
    fr: float = 0.015  # 滚动阻力系数
    g: float = 9.81  # m/s^2

    @property
    def L(self) -> float:
        return self.lf + self.lr


VEH = VehicleParams()
