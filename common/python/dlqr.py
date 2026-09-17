"""离散 LQR：迭代代数 Riccati。"""

from __future__ import annotations

import numpy as np


def dlqr(A: np.ndarray, B: np.ndarray, Q: np.ndarray, R: np.ndarray, niter: int = 400) -> np.ndarray:
    P = Q.copy().astype(float)
    A, B = np.asarray(A, float), np.asarray(B, float)
    if B.ndim == 1:
        B = B.reshape(-1, 1)
    R = np.atleast_2d(np.asarray(R, float))
    for _ in range(niter):
        S = R + B.T @ P @ B
        K = np.linalg.solve(S, B.T @ P @ A)
        Pnew = A.T @ P @ A - A.T @ P @ B @ K + Q
        if np.linalg.norm(Pnew - P, ord="fro") < 1e-10:
            P = Pnew
            break
        P = 0.5 * (Pnew + Pnew.T)
    K = np.linalg.solve(R + B.T @ P @ B, B.T @ P @ A)
    return K
