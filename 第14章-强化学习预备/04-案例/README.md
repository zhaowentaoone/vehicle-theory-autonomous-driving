# 第 14 章案例　车道保持环境：随机 vs PID

不训练神经网络。跑若干 episode，打印平均回报、平均步数、横向 RMSE。

**做对的标志**：PID 几乎跑满 `max_steps`；随机策略很快 `|ey|>2.5` 终止；PID 的 RMSE 远小于随机。

Python：`lane_keep_env.py` + `eval_baselines.py`。若安装了 Gymnasium，环境仍可独立运行。  
MATLAB：`eval_baselines.m`。
