# 算法　Pure Pursuit 与 Stanley

## Pure Pursuit 伪代码

```
i = nearest_index(rear_axle, path)
look = interpolate_ahead(path, i, ld)
vec = world_to_body(look, rear_axle, psi)  # (eta, zeta)
alpha = atan2(zeta, eta)
delta = atan2(2 * L * sin(alpha), ld)
delta = clip(delta)
```

## Stanley 伪代码

```
pf = front_axle_position()
i = nearest_index(pf, path)
ey = signed_lateral_error(pf, path[i], psi_path)  # left positive
epsi = wrap_to_pi(psi_path - psi)
delta = epsi - atan(k * ey / (v + eps))
delta = clip(delta)
```

## 调参

| 参数 | 起点 | 备注 |
|------|------|------|
| $l_d$ | $2+0.3v$ （m, v 为 m/s） | 道路越弯越要减小 |
| $k$ Stanley | $1\sim 3\,\mathrm{s}^{-1}$ | 与 $e_y$ 单位 m 匹配 |
| 路径点间距 | $0.5\sim 1\,\mathrm{m}$ | 太稀则切向跳 |

## 实时性

最近邻若每次线性扫 $N$ 点：$O(N)$。闭环 100 Hz、$N=2000$ 仍可接受；更长路用「只在上次下标附近搜」$O(1)$。
