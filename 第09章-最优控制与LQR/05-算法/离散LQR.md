# 算法　离散 LQR（迭代 Riccati）

## 伪代码

```
P = Q
for iter in 1..N:
    K = solve(R + B.T @ P @ B, B.T @ P @ A)
    Pnew = A.T @ P @ A - A.T @ P @ B @ K + Q
    if ||Pnew-P|| < tol: break
    P = Pnew
u = -K @ x
```

## 复杂度

状态维 $n=2$ 时可忽略。$n=10$ 的 Riccati 仍在毫秒内。实时只需算 $u=-Kx$，Riccati 可离线或低频率调度。

## 调参

先令 $R=1$（对 $\delta$ 以 rad²），再调 $q_y$。$e_y$ 以米、$e_\psi$ 以弧度，量纲不同：可先把 $e_\psi$ 看成「5 m 外 0.1 rad ≈ 0.5 m」，故 $q_\psi$ 常取比 $q_y$ 大几倍到一个数量级。

## 对比

相对 Pure Pursuit：无需调预瞄距离，但对线性化更敏感。相对 MPC：不能显式限幅（只能事后 clip），也不能处理前方变曲率的预瞄规划（除非加前馈）。
