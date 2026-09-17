"""路径生成与几何跟踪器。"""

from __future__ import annotations

import numpy as np

from bicycle_kinematic import wrap_to_pi


def make_path(ds: float = 0.5) -> np.ndarray:
    """直线 60 m + 1/4 圆弧 R=40 m。返回 (N, 3) = X,Y,psi."""
    R = 40.0
    xs = np.arange(0.0, 60.0, ds)
    ys = np.zeros_like(xs)
    psis = np.zeros_like(xs)
    n_arc = int(0.5 * np.pi * R / ds)
    ang = np.linspace(0.0, 0.5 * np.pi, n_arc, endpoint=False)
    xa = 60.0 + R * np.sin(ang)
    ya = R * (1.0 - np.cos(ang))
    pa = ang
    ys2 = np.arange(ya[-1] + ds, ya[-1] + 120.0, ds)
    xs2 = np.full_like(ys2, xa[-1])
    ps2 = np.full_like(ys2, 0.5 * np.pi)
    X = np.concatenate([xs, xa, xs2])
    Y = np.concatenate([ys, ya, ys2])
    P = np.concatenate([psis, pa, ps2])
    return np.stack([X, Y, P], axis=1)


def nearest_index(p: np.ndarray, path: np.ndarray, start: int = 0, window: int = 80) -> int:
    i0 = max(start, 0)
    i1 = min(len(path), i0 + window)
    d = np.hypot(path[i0:i1, 0] - p[0], path[i0:i1, 1] - p[1])
    return i0 + int(np.argmin(d))


def signed_ey(p: np.ndarray, path_xy: np.ndarray, psi_path: float) -> float:
    dx = p[0] - path_xy[0]
    dy = p[1] - path_xy[1]
    n = np.array([-np.sin(psi_path), np.cos(psi_path)])
    return float(dx * n[0] + dy * n[1])


def pure_pursuit(x: np.ndarray, path: np.ndarray, L: float, ld: float, idx: int) -> tuple[float, int]:
    idx = nearest_index(x[:2], path, idx)
    # 沿下标向前约 ld
    acc = 0.0
    j = idx
    while j < len(path) - 1 and acc < ld:
        acc += np.hypot(path[j + 1, 0] - path[j, 0], path[j + 1, 1] - path[j, 1])
        j += 1
    look = path[j, :2]
    dx = look[0] - x[0]
    dy = look[1] - x[1]
    c, s = np.cos(x[2]), np.sin(x[2])
    eta = c * dx + s * dy
    zeta = -s * dx + c * dy
    alpha = np.arctan2(zeta, eta)
    delta = np.arctan2(2.0 * L * np.sin(alpha), ld)
    return float(np.clip(delta, -np.deg2rad(35), np.deg2rad(35))), idx


def stanley(x: np.ndarray, path: np.ndarray, L: float, k: float, v: float, idx: int) -> tuple[float, int]:
    lf_approx = L * 1.2 / 2.8
    pf = x[:2] + np.array([np.cos(x[2]), np.sin(x[2])]) * lf_approx
    idx = nearest_index(pf, path, idx)
    psi_p = path[idx, 2]
    ey = signed_ey(pf, path[idx, :2], psi_p)
    epsi = wrap_to_pi(psi_p - x[2])
    delta = epsi - np.arctan(k * ey / (v + 0.1))
    return float(np.clip(delta, -np.deg2rad(35), np.deg2rad(35))), idx
