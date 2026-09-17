"""第00章：Python 环境自检。"""

from __future__ import annotations

import sys


def main() -> None:
    print(f"Python {sys.version.split()[0]}")

    import numpy as np
    import scipy
    import matplotlib

    print(f"numpy {np.__version__} OK")
    print(f"scipy {scipy.__version__} OK")
    print(f"matplotlib {matplotlib.__version__} OK")

    for name in ("casadi", "gymnasium"):
        try:
            mod = __import__(name)
            ver = getattr(mod, "__version__", "unknown")
            print(f"{name} {ver} OK (optional)")
        except ImportError:
            print(f"{name} not installed (optional until later chapters)")

    import matplotlib.pyplot as plt

    t = np.linspace(0.0, 1.0, 50)
    y = 2.0 * t + 0.5
    fig, ax = plt.subplots()
    ax.plot(t, y, "k-")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("y")
    ax.set_title("Ch00 env check: a straight line")
    ax.grid(True)
    fig.tight_layout()
    out = __file__.replace("check_env.py", "env_check.png")
    fig.savefig(out, dpi=120)
    print(f"saved {out}")
    plt.show()


if __name__ == "__main__":
    main()
