# 算法　A* 与 IDM

## A* 伪代码

```
open = min-heap of (f, node)
g[start]=0; f[start]=h(start)
while open:
    current = pop min f
    if current == goal: reconstruct
    for nb in neighbors(current):
        tentative = g[current] + cost(current, nb)
        if tentative < g[nb]:
            came_from[nb]=current
            g[nb]=tentative
            f[nb]=tentative + h(nb)
            push nb
```

复杂度：最坏 $O(|E|\log|V|)$。实时性：30×30 毫无压力；城市 0.2 m 栅格可能要分层或 Hybrid。

## IDM 伪代码

```
dv = v - vp
s_star = s0 + max(0, v*T + v*dv/(2*sqrt(amax*b)))
a = amax * (1 - (v/v0)**delta - (s_star/max(s,eps))**2)
a = clip(a, -4, amax)
```

## 对比

| 方法 | 用途 | 车辆约束 |
|------|------|----------|
| A* | 全局几何 | 无 |
| Hybrid A* | 泊车/窄路 | 有（运动学） |
| RRT | 高维探索 | 可有 |
| Lattice | 结构化道路 | 有 |
| IDM | 纵向速度 | 点质量 |
