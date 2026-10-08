"""solution.py 검증: StringIO 로 입력을 흉내 내서 확인"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_read_ints_handles_any_whitespace():
    assert solution.read_ints(io.StringIO("1 2\n3\t4  \n\n-5\n")) == [1, 2, 3, 4, -5]
    assert solution.read_ints(io.StringIO("")) == []


def test_read_pairs_until_eof():
    assert solution.read_pairs_until_eof(io.StringIO("1 2\n3 4\n\n5 6")) == [(1, 2), (3, 4), (5, 6)]
    assert solution.read_pairs_until_eof(io.StringIO("")) == []


def test_sum_each_test():
    assert solution.sum_each_test(io.StringIO("3\n1 2\n10 -4\n0 0\n")) == [3, 6, 0]


def test_format_lines():
    assert solution.format_lines([1, 2, 3]) == "1\n2\n3"
    assert solution.format_lines([]) == ""


def test_large_input_roundtrip():
    rng = random.Random(0)
    pairs = [(rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9)) for _ in range(50_000)]
    text = f"{len(pairs)}\n" + "\n".join(f"{a} {b}" for a, b in pairs) + "\n"
    results = solution.sum_each_test(io.StringIO(text))
    assert results == [a + b for a, b in pairs]
    assert solution.read_ints(io.StringIO(text))[1:] == [x for pair in pairs for x in pair]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2\n1 2\n3 4\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["3", "7"]
