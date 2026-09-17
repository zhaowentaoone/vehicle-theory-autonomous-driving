# 算法　离散 PID 与恒时距 ACC

## PID 伪代码

```
I = 0, e_prev = 0
loop:
    e = ref - meas
    I = I + e * dt
    d = (e - e_prev) / dt
    u = Kp*e + Ki*I + Kd*d
    u_sat = clip(u, umin, umax)
    if u != u_sat: I -= e * dt   # 简单条件积分
    e_prev = e
    apply u_sat
```

## ACC 伪代码

```
s_des = s0 + h * v
a = Ks * (s - s_des) + Kv * (vp - v)
a = clip(a, amin, amax)
```

## 调参表

| 参数 | 起点 | 过大时 |
|------|------|--------|
| $K_p$（巡航） | 0.4–1.0 | 抖、执行器饱和 |
| $K_i$ | 0.1–0.3 | 超调、windup |
| $h$ | 1.0–1.8 s | 太大：老被加塞；太小：危险 |
| $K_s$ | 0.1–0.4 | 跟车突然 |
| $K_v$ | 0.5–1.2 | 对雷达噪声敏感 |

## 对比

PID 巡航简单、无模型。ACC 这套仍是线性反馈，没有显式「永不碰撞」约束。MPC 跟车可把 $s\ge s_{\min}$ 写成不等式。
