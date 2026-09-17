"""八邻域 A*。"""

from __future__ import annotations

import heapq
import numpy as np


def astar(grid: np.ndarray, start: tuple[int, int], goal: tuple[int, int]):
    h, w = grid.shape
    nbrs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def heur(i, j):
        return np.hypot(i - goal[0], j - goal[1])

    def valid(i, j):
        return 0 <= i < h and 0 <= j < w and grid[i, j] == 0

    g = {start: 0.0}
    came: dict[tuple[int, int], tuple[int, int]] = {}
    openh = [(heur(*start), start)]
    closed: set[tuple[int, int]] = set()
    expanded = 0
    while openh:
        _, cur = heapq.heappop(openh)
        if cur in closed:
            continue
        closed.add(cur)
        expanded += 1
        if cur == goal:
            path = [cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)
            path.reverse()
            return path, expanded
        for di, dj in nbrs:
            nb = (cur[0] + di, cur[1] + dj)
            if not valid(*nb):
                continue
            step = np.hypot(di, dj)
            tg = g[cur] + step
            if tg < g.get(nb, np.inf):
                g[nb] = tg
                came[nb] = cur
                heapq.heappush(openh, (tg + heur(*nb), nb))
    return None, expanded
