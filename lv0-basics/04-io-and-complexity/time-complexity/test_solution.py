"""solution.py 검증: 반복 횟수를 직접 센 값과 공식 비교 + 복잡도별 최대 입력 크기"""
import io
import math

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_loop_counts_match_formulas():
    for n in range(0, 200):
        assert solution.count_single_loop(n) == n
        assert solution.count_nested_loops(n) == n * n
        assert solution.count_triangle_loops(n) == n * (n - 1) // 2
        assert solution.count_halving(n) == (n.bit_length() - 1 if n >= 1 else 0)
        assert solution.count_sqrt_loop(n) == math.isqrt(n)


def test_triangle_loop_is_still_quadratic():
    # n 이 10배 커지면 n² 은 100배, n(n-1)/2 도 약 100배 늘어난다
    ratio = solution.count_triangle_loops(1000) / solution.count_triangle_loops(100)
    assert 95 < ratio < 105


def test_max_n_exact_values():
    assert solution.max_n("n") == 10 ** 8
    assert solution.max_n("n^2") == 10 ** 4
    assert solution.max_n("n^3") == 464  # 464³ = 99,897,344 이고 465³ = 100,544,625
    assert solution.max_n("2^n") == 26  # 2²⁶ ≈ 6.7천만, 2²⁷ ≈ 1.3억
    assert solution.max_n("n!") == 11  # 11! ≈ 4천만, 12! ≈ 4.8억


@pytest.mark.parametrize("name", list(solution.COST))
@pytest.mark.parametrize("budget", [10, 1000, 10 ** 6, 10 ** 8, 10 ** 9])
def test_max_n_is_the_boundary(name, budget):
    cost = solution.COST[name]
    n = solution.max_n(name, budget)
    assert cost(n) <= budget < cost(n + 1)


def test_n_log_n_is_between_linear_and_quadratic():
    assert solution.max_n("n^2") < solution.max_n("n log n") < solution.max_n("n")


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("n^2\n\nn^3\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["10000", "464"]
