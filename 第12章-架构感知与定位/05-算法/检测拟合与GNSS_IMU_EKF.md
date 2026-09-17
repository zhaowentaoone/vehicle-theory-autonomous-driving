# 算法　1D 车道峰值检测 + 线性拟合；GNSS/IMU EKF

## 车道拟合伪代码

```
for each image-row sample x:
    y_hat = argmax_y response(x, y)
pts.append((x, y_hat))
c1, c0 = least_squares(y = c1*x + c0)
```

教学用，不是真实图像。真实系统还要鸟瞰变换、多车道、置信度。

## EKF 预测

$x=[X,Y,\psi]$，$u=[v,r]$：

$$
X^{+}=X+v\Delta t\cos\psi,\ \ Y^{+}=Y+v\Delta t\sin\psi,\ \ \psi^{+}=\psi+r\Delta t
$$

Jacobian：

$$
A=\begin{bmatrix}1&0&-v\Delta t\sin\psi\\0&1&v\Delta t\cos\psi\\0&0&1\end{bmatrix}
$$

测量 $h=[X,Y]$，$C=[[1,0,0],[0,1,0]]$。

## 调参

GNSS $R=\mathrm{diag}(\sigma^2,\sigma^2)$，$\sigma$ 按实际 1–5 m。IMU 过程噪声在 $\psi$ 上：若 IMU 很准，$Q_{\psi\psi}$ 小。
