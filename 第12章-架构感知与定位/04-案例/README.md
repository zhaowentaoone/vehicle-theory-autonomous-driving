# 第 12 章案例

1. `lane_fit.py`：合成车道响应 → 峰值检测 → 一次多项式。  
2. `gnss_imu_ekf.py`：自行车真值 + 噪声 GNSS + 带偏置的 yaw rate，EKF 融合。

**做对的标志**：拟合斜率误差小于 0.05；EKF 位置 RMSE 明显小于生 GNSS RMSE。
