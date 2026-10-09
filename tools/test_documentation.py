"""Python 예제의 구문과 명시적으로 실행 가능하다고 표시한 예제의 결과를 검증한다."""
import ast
from pathlib import Path
import re
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_RE = re.compile(r"<!-- RUNNABLE -->\s*```python\n(.*?)\n```", flags=re.S)
PYTHON_BLOCK_RE = re.compile(r"^```python[^\n]*\n(.*?)^```", flags=re.M | re.S)


def documentation_paths():
    return [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")),
            *sorted(ROOT.glob("lv*/*/*/README.md"))]


def examples():
    for path in documentation_paths():
        text = path.read_text(encoding="utf-8")
        matches = EXAMPLE_RE.findall(text)
        assert len(matches) == text.count("<!-- RUNNABLE -->"), f"잘못된 실행 예제 마커: {path}"
        for index, code in enumerate(matches, 1):
            yield pytest.param(code, id=f"{path.relative_to(ROOT)}:{index}")


def python_blocks():
    for path in documentation_paths():
        for index, code in enumerate(PYTHON_BLOCK_RE.findall(path.read_text(encoding="utf-8")), 1):
            yield pytest.param(code, id=f"{path.relative_to(ROOT)}:{index}")


@pytest.mark.parametrize("code", list(python_blocks()))
def test_python_documentation_blocks_have_valid_syntax(code):
    ast.parse(code)


@pytest.mark.parametrize("code", list(examples()))
def test_documented_example_runs_with_its_assertions(code):
    assert re.search(r"^\s*assert\s", code, flags=re.M), "실행 예제에는 기대 결과 검사가 필요합니다"
    completed = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True,
                               text=True, timeout=30)
    assert completed.returncode == 0, completed.stdout + completed.stderr
