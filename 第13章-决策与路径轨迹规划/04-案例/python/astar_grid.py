from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "common" / "python"))
from astar import astar  # noqa: E402


def main() -> None:
    grid = np.zeros((30, 30), dtype=int)
    grid[5:25, 12:16] = 1
    grid[18:22, 16:24] = 1
    start, goal = (2, 2), (27, 27)
    path, expanded = astar(grid, start, goal)
    print(f"path length={len(path) if path else None}, expanded={expanded}")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(grid, cmap="Greys", origin="lower")
    if path:
        ys, xs = zip(*path)
        ax.plot(xs, ys, "k-o", ms=3)
    ax.plot(start[1], start[0], "gs", ms=10)
    ax.plot(goal[1], goal[0], "rs", ms=10)
    ax.set_title("A* on occupancy grid")
    fig.tight_layout()
    out = Path(__file__).with_name("astar_grid.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
