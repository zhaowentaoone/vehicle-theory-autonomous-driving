# 第 00 章案例　环境自检

## 你要做什么

确认 Python 与 MATLAB 都能找到依赖，并能画出一张最简单的图。不涉及车辆模型。

## 如何运行

### Python

在课程根目录已 `pip install -r requirements.txt` 的前提下：

```bash
python "第00章-导论与知识地图/04-案例/python/check_env.py"
```

或进入该文件夹后 `python check_env.py`。

### MATLAB

打开 `04-案例/matlab/check_env.m`，点击运行。需要能使用 `plot`。

## 怎样算做对

- Python 打印 `numpy / scipy / matplotlib OK`，并弹出（或保存）一条直线图。
- MATLAB 打印 `MATLAB graphics OK`，并出现同一条直线。
- 若第 10、14 章依赖尚未装，Python 脚本会提示 `casadi` / `gymnasium` 为可选，不判失败。
