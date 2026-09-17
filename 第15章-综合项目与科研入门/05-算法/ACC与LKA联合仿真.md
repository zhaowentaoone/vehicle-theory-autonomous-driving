# 项目实施要点

## 联合仿真循环

```
loop t:
    测间距 s, 相对速度, 自车 v
    a = ACC(s, v, vp)          # 第07章
    测 ey, epsi
    delta = Stanley(...)       # 第08章
    v += dt * a
    bicycle_euler(x, v, delta)
```

前车：$v_p(t)$ 分段，$X_p$ 积分。间距用纵向弧长差近似 $s=X_p-X-L_{\mathrm{veh}}$。缓弯时该近似可接受；急弯应沿路径弧长。

## 报告检查单

- [ ] 参数全部来自 `vehicle_params` 或文中表格
- [ ] 随机种子固定
- [ ] 对照实验三组
- [ ] 失败案例（例如 $h=0.4\,\mathrm{s}$）至少一张图
- [ ] 局限：运动学植物、无侧风、无执行器延迟
