"""线性卡尔曼一步：预测+更新。"""

from __future__ import annotations

import numpy as np


def kf_predict(x, P, A, Q, B=None, u=None):
    x = A @ x if u is None else A @ x + B @ u
    P = A @ P @ A.T + Q
    P = 0.5 * (P + P.T)
    return x, P


def kf_update(x, P, y, C, R):
    y = np.atleast_1d(np.asarray(y, float))
    S = C @ P @ C.T + R
    K = np.linalg.solve(S.T, (P @ C.T).T).T
    x = x + K @ (y - C @ x)
    I = np.eye(P.shape[0])
    P = (I - K @ C) @ P
    P = 0.5 * (P + P.T)
    return x, P, K
