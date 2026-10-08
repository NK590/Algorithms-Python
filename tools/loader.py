"""테스트에서 같은 폴더의 solution.py 를 불러오는 도우미

모든 개념 폴더가 `solution.py` / `test_solution.py` 라는 같은 이름을 쓰기 때문에,
그냥 `import solution` 을 하면 폴더끼리 모듈 이름이 충돌한다.
경로마다 고유한 모듈 이름으로 불러와서 이를 피한다.

    # <개념 폴더>/test_solution.py
    from tools.loader import load_solution

    solution = load_solution(__file__)

    def test_something():
        assert solution.some_function(...) == ...
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType


def load_solution(test_file: str | Path, filename: str = "solution.py") -> ModuleType:
    path = Path(test_file).resolve().with_name(filename)
    name = "solution__" + re.sub(r"\W", "_", str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"{path} 를 불러올 수 없습니다")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[name]
        raise
    return module
