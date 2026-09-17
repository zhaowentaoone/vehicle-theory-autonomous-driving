# 算法　线性 MPC（凝聚 QP）

## 构造 $\Phi,\Gamma$

```
Phi = []
Gamma_rows = []
Apow = I
for i in 1..N:
    Apow = Apow @ A          # A^i
    Phi.append(Apow)
    # Gamma row i: [A^{i-1}B, A^{i-2}B, ..., B, 0, ...]
```

代码用循环累乘更不易错，见 `common/python/linear_mpc.py`。

## QP

$X=\Phi x+\Gamma U$，$J=X^\top \bar Q X + U^\top \bar R U$

$H=2(\Gamma^\top \bar Q \Gamma+\bar R)$，$f=2\Gamma^\top \bar Q \Phi x$

箱约束 $U\in[u_{\min},u_{\max}]^N$。速率：$\lvert u_0-u_{\mathrm{prev}}\rvert\le\Delta$，$|u_{i}-u_{i-1}|\le\Delta$。

## 伪代码（回退）

```
u_prev = 0
loop:
    ey, epsi = measure()
    U = solve_qp(x=[ey,epsi], u_prev)
    apply U[0]
    u_prev = U[0]
    plant.step(U[0])
```

## 调参

| 参数 | 起点 | 过大/过小 |
|------|------|-----------|
| $N$ | 10–20（$\Delta t=0.05$ 则预瞄 0.5–1 s） | 太大：耗时；太小：切弯 |
| $q_y$ | 4–20 | 过大在约束下仍要猛打，QP 顶满 |
| $\Delta u_{\max}$ | $10^\circ$/步 视 $\Delta t$ 而定 | 过小：来不及纠偏 |

## 对比

|  | LQR | 几何法 | MPC |
|--|-----|--------|-----|
| 约束 | 事后 clip | 事后 clip | 优化内 |
| 预瞄 | 无穷（模型） | 显式 $l_d$ | 显式 $N\Delta t$ |
| CPU | $O(n^2)$ 矩阵乘 | $O(1)$ | QP，视 $N$ |
| 模型 | 线性 | 几何 | 线性或非线性 |

## 非线性 MPC 伪代码（CasADi 方向）

```
opti = Opti()
X = opti.variable(3, N+1)   # X,Y,psi
U = opti.variable(1, N)
opti.subject_to(X[:,0] == x0)
for k in 0..N-1:
    opti.subject_to(X[:,k+1] == bicycle_euler(X[:,k], v, U[k]))
    opti.subject_to( |U[k]| <= dmax )
cost = sum ey(X[k])^2 + R*U[k]^2
opti.minimize(cost)
opti.solve()
```

本课程案例用线性版保证 MATLAB 对照；把上面换成 CasADi 是第 15 章升级项。
