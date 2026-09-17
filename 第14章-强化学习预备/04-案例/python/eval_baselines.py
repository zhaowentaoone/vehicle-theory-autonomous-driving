from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from lane_keep_env import LaneKeepEnv  # noqa: E402


def rollout(env: LaneKeepEnv, policy, seed: int):
    obs = env.reset(seed=seed)
    G = 0.0
    eys = []
    for _ in range(env.max_steps):
        act = policy(obs)
        obs, r, done, info = env.step(act)
        G += r
        eys.append(info["ey"])
        if done:
            break
    return G, len(eys), float(np.sqrt(np.mean(np.square(eys))))


def pid_policy(obs):
    ey, epsi, _ = obs
    return -0.8 * ey - 1.6 * epsi


def random_policy(obs, rng):
    return rng.uniform(-np.deg2rad(20), np.deg2rad(20))


def main() -> None:
    env = LaneKeepEnv()
    rng = np.random.default_rng(0)
    n_ep = 8
    rows = []
    for name, pol in [
        ("random", lambda o: random_policy(o, rng)),
        ("PID", pid_policy),
    ]:
        Gs, steps, rmses = [], [], []
        for ep in range(n_ep):
            G, n, rmse = rollout(env, pol, seed=10 + ep)
            Gs.append(G)
            steps.append(n)
            rmses.append(rmse)
        print(f"{name:6s}  return={np.mean(Gs):7.2f}  steps={np.mean(steps):6.1f}  eyRMSE={np.mean(rmses):.3f}")
        rows.append((name, Gs, rmses))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([0, 1], [np.mean(rows[0][1]), np.mean(rows[1][1])], color=["0.6", "0.2"])
    ax.set_xticks([0, 1], ["random", "PID"])
    ax.set_ylabel("mean return")
    ax.set_title("Lane-keeping baselines (higher is better)")
    ax.grid(True, axis="y")
    fig.tight_layout()
    out = Path(__file__).with_name("eval_baselines.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
