# 第 02 章案例　开环运动学仿真

## 目的

固定 $v,\delta$，积分自行车模型，观察圆轨迹，并与理论半径 $R=L/\tan\delta$ 比较。

## 运行

```bash
python "第02章-车辆运动学与自行车模型/04-案例/python/kinematic_circle.py"
```

MATLAB：`04-案例/matlab/kinematic_circle.m`。

默认：$v=8\,\mathrm{m/s}$，$\delta=15^\circ$，$T=12\,\mathrm{s}$，$\Delta t=0.01\,\mathrm{s}$。

## 做对的标志

- $X$–$Y$ 图是圆（`axis equal`）。
- 打印的「仿真半径」与理论 $L/\tan\delta$ 相对误差小于 5%（欧拉 + 有限时间，圆心用几何拟合或用 $R=v/\dot\psi$）。
- 横摆角随时间近似线性增长（常 $\dot\psi$）。
- 把 $\delta$ 改为 0，轨迹为沿 $X$ 的直线。
