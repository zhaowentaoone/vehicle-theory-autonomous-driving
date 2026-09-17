"""把课程根目录的 common/python 加入 sys.path，便于各章脚本 import vehicle_params。"""

from pathlib import Path
import sys


def add_common_to_path() -> Path:
    here = Path(__file__).resolve()
    common_python = here.parent
    if str(common_python) not in sys.path:
        sys.path.insert(0, str(common_python))
    return common_python
