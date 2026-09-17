# 公共代码库

各章案例通过把本目录加入 `sys.path` / `addpath` 复用，避免复制粘贴导致参数不一致。

## Python（`common/python`）

| 文件 | 用途 | 首次出现 |
|------|------|----------|
| `vehicle_params.py` | 教学车参数 | 全书 |
| `bicycle_kinematic.py` | 运动学自行车欧拉/圆弧积分 | 02 |
| `pacejka.py` | 魔术公式 | 03 |
| `lateral_2dof.py` | 二自由度 $A,B$ | 05 |
| `pid.py` | 离散 PID | 07 |
| `geom_track.py` | 路径、PP、Stanley | 08 |
| `dlqr.py` | 迭代 Riccati | 09 |
| `linear_mpc.py` | 凝聚 QP-MPC | 10 |
| `kalman.py` | KF 预测更新 | 11 |
| `astar.py` `idm.py` | 规划 | 13 |
| `lane_keep_env.py` | RL 环境 | 14 |

## MATLAB（`common/matlab`）

对应 `.m`：`vehicle_params` `bicycle_euler` `bicycle_exact` `pacejka` `lateral_AB` `pid_step` `dlqr_iter` `mpc_step` `kf_predict` `kf_update` `astar_grid` `idm_accel`。
