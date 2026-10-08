"""solution.py 검증: math 와 반복문 기준 구현과 비교 + 재귀 깊이 제한"""
import io
import math

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_factorial_matches_math():
    for n in range(0, 30):
        assert solution.factorial(n) == math.factorial(n)


def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_fibonacci_matches_iterative():
    for n in range(0, 20):
        assert solution.fibonacci(n) == fib_iterative(n)
    for n in range(0, 200):
        assert solution.fibonacci_memo(n) == fib_iterative(n)


def test_naive_fibonacci_call_count_is_exponential():
    # 호출 횟수는 2·F(n+1) − 1 이다. n 이 하나 늘 때마다 약 1.6 배씩 늘어난다.
    for n in range(0, 20):
        assert solution.fibonacci_call_count(n) == 2 * fib_iterative(n + 1) - 1
    assert solution.fibonacci_call_count(25) > 200_000


def test_sum_of_digits_matches_str():
    for n in list(range(0, 2000)) + [10 ** 18 + 999]:
        assert solution.sum_of_digits(n) == sum(map(int, str(n)))


def test_reverse_string():
    for s in ("", "a", "abc", "hello world"):
        assert solution.reverse_string(s) == s[::-1]


def test_sum_to_recursive_hits_the_recursion_limit():
    assert solution.sum_to_recursive(100) == 5050
    assert solution.sum_to_iterative(100_000) == 100_000 * 100_001 // 2
    with pytest.raises(RecursionError):
        solution.sum_to_recursive(50_000)  # 기본 재귀 깊이 제한(1000)을 넘는다


def test_cantor_string():
    assert solution.cantor_string(0) == "-"
    assert solution.cantor_string(1) == "- -"
    assert solution.cantor_string(2) == "- -   - -"
    for n in range(0, 8):
        assert len(solution.cantor_string(n)) == 3 ** n


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "120"
