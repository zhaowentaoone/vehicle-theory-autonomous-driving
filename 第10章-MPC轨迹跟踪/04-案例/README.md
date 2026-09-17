# 第 10 章案例　带约束的运动学线性 MPC

与第 09 章同一条正弦路、同一初始横向偏差。$\delta$ 限制在 $\pm 8^\circ$，并限制每步变化。

**做对的标志**：仍能拉回路径；起步转角被顶在限幅上一段时间（打印 `sat_frac`）；比无约束 LQR 拉回更慢，但不应发散。

Python 优先 CasADi；若未安装则 SciPy SLSQP。MATLAB 用 `quadprog`，若无优化工具箱则无约束最小二乘 + clip。
