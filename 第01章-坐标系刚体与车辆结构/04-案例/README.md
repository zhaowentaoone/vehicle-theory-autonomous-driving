# 第 01 章案例　车体矩形变换到惯性系

## 目的

把质心、车体四角、前轴/后轴中心从车体系变到地面并绘图，建立对 $R(\psi)$ 的直觉。

## 运行

```bash
python "第01章-坐标系刚体与车辆结构/04-案例/python/body_to_inertial.py"
```

MATLAB：运行 `04-案例/matlab/body_to_inertial.m`（脚本会 `addpath` 到 `common/matlab`）。

## 做对的标志

- 图中矩形长边约 $L\approx 2.8\,\mathrm{m}$ 量级（前后轴之外还有悬，脚本用简化车长 4.5 m）。
- 改变 `psi_deg` 时矩形旋转，边长不变。
- 质心为原点附近的点；前轴中心在车头方向、后轴中心在车尾方向。
- Python 与 MATLAB 两张图几何一致。
