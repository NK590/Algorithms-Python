import sys

from tools.loader import load_solution


def test_same_filename_in_different_folders_does_not_collide(tmp_path):
    for name, value in (("a", 1), ("b", 2)):
        (tmp_path / name).mkdir()
        (tmp_path / name / "solution.py").write_text(f"VALUE = {value}\n")
    a = load_solution(tmp_path / "a" / "test_solution.py")
    b = load_solution(tmp_path / "b" / "test_solution.py")
    assert (a.VALUE, b.VALUE) == (1, 2)


def test_failed_import_is_not_left_in_sys_modules(tmp_path):
    (tmp_path / "solution.py").write_text("raise RuntimeError('boom')\n")
    before = set(sys.modules)
    try:
        load_solution(tmp_path / "test_solution.py")
    except RuntimeError:
        pass
    else:
        raise AssertionError("RuntimeError 가 전파되어야 합니다")
    assert set(sys.modules) == before
