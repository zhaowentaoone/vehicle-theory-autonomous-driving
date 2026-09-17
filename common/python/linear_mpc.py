"""凝聚线性 MPC：箱约束 + 输入速率约束。"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


def build_pred(A: np.ndarray, B: np.ndarray, N: int):
    n = A.shape[0]
    m = B.shape[1]
    Phi = np.zeros((n * N, n))
    Gamma = np.zeros((n * N, m * N))
    Ap = np.eye(n)
    for i in range(N):
        Ap = Ap @ A
        Phi[i * n : (i + 1) * n, :] = Ap
        Acol = np.eye(n)
        for j in range(i, -1, -1):
            Gamma[i * n : (i + 1) * n, j * m : (j + 1) * m] = Acol @ B
            Acol = Acol @ A
    return Phi, Gamma


def mpc_step(
    x: np.ndarray,
    A: np.ndarray,
    B: np.ndarray,
    Q: np.ndarray,
    R: float,
    N: int,
    umin: float,
    umax: float,
    dumax: float,
    u_prev: float,
) -> np.ndarray:
    Phi, Gamma = build_pred(A, B, N)
    Qb = np.kron(np.eye(N), Q)
    Rb = R * np.eye(N)
    H = Gamma.T @ Qb @ Gamma + Rb
    H = 0.5 * (H + H.T)
    f = Gamma.T @ Qb @ Phi @ x.reshape(-1)

    def cost(U):
        return 0.5 * U @ H @ U + f @ U

    def jac(U):
        return H @ U + f

    cons = []

    def add_rate(i: int, prev_is_u0: bool) -> None:
        cons.append({"type": "ineq", "fun": lambda U, i=i: dumax - (U[i] - (u_prev if i == 0 else U[i - 1]))})
        cons.append({"type": "ineq", "fun": lambda U, i=i: dumax - ((u_prev if i == 0 else U[i - 1]) - U[i])})

    for i in range(N):
        add_rate(i, i == 0)
    bounds = [(umin, umax)] * N
    U0 = np.clip(np.full(N, u_prev), umin, umax)
    res = minimize(cost, U0, jac=jac, bounds=bounds, constraints=cons, method="SLSQP", options={"maxiter": 80, "ftol": 1e-8})
    if not res.success:
        U = np.clip(U0, umin, umax)
    else:
        U = np.clip(res.x, umin, umax)
    return U
