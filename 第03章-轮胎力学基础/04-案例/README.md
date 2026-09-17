# 第 03 章案例　魔术公式曲线

## 目的

绘制纯侧偏 $F_y(\alpha)$ 与纯纵滑 $F_x(\sigma)$，并画原点线性切线。

## 运行

```bash
python "第03章-轮胎力学基础/04-案例/python/pacejka_curves.py"
```

MATLAB：`pacejka_curves.m`。

## 做对的标志

- 曲线过原点、奇函数（左右对称反号）。
- 约 $8^\circ$–$12^\circ$ 附近出现峰值（取决于 $B,C,D,E$）。
- 虚线切线在 $\pm 3^\circ$ 内与曲线几乎重合，大角度高于曲线（线性高估）。
