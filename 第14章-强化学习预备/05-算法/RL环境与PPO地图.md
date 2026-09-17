# 算法　把自行车模型包成 RL 环境；PPO 只作地图

## 环境伪代码

```
class LaneKeepEnv:
    reset(seed):
        ey ~ U(-0.5,0.5), epsi ~ U(-0.1,0.1)
        X=0, path = sine or straight
        return obs
    step(delta):
        delta = clip(delta)
        bicycle_euler(...)
        ey, epsi = errors()
        r = -ey**2 - 0.5*epsi**2 - 0.05*delta**2 + 0.05
        done = |ey|>2.5 or t>=T
        return obs, r, done
```

## PPO（阅读用地图，本课不实现完整训练循环）

1. 用当前 $\pi_\theta$ 在环境采样一段轨迹。
2. 算优势 $\hat A_t$（GAE）。
3. 最大化 $\mathbb E[\min(\rho\hat A, \mathrm{clip}(\rho,1-\epsilon,1+\epsilon)\hat A)]$，其中 $\rho=\pi_\theta/\pi_{\mathrm{old}}$。
4. 同时拟合价值网络、加熵奖励探索。

超参起步（以后训练时）：`clip=0.2`，`gamma=0.99`，`lr=3e-4`，batch 数万步。先让 PID 基线存在，再开训。

## 与 MPC 接口

可把 MPC 的 $u$ 当 `action` 的先验：RL 输出残差 $\Delta u$，再 clip。这是安全 RL 的一条工程路。
