"""solution.py 검증: 닫힌 식, 모든 경우를 나열하는 완전 탐색, 연쇄를 연립방정식으로 푼 독립적인 계산과 비교"""
import io
import itertools
import random
import time
from fractions import Fraction

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)

MOD = 998244353


def test_solve_linear_recovers_a_known_solution():
    rng = random.Random(0)
    for _ in range(100):
        n = rng.randint(1, 6)
        a = [[Fraction(rng.randint(-5, 5), rng.randint(1, 4)) for _ in range(n)] for _ in range(n)]
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n)]
        b = [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)]
        try:
            solved = solution.solve_linear(a, b)
        except ValueError:
            # 무작위 행렬이 우연히 특이할 수 있다: 그때는 정말 행렬식이 0 이어야 한다
            assert determinant(a) == 0
            continue
        assert solved == x
    with pytest.raises(ValueError, match="하나로"):
        solution.solve_linear([[1, 2], [2, 4]], [1, 2])
    assert solution.solve_linear([[2]], [3]) == [Fraction(3, 2)]
    assert solution.solve_linear([[0, 1], [1, 0]], [5, 7]) == [7, 5]  # 첫 열의 기준이 0 이라 행을 바꿔야 한다


def determinant(matrix):
    n = len(matrix)
    rows = [[Fraction(v) for v in row] for row in matrix]
    det = Fraction(1)
    for c in range(n):
        pivot = next((r for r in range(c, n) if rows[r][c] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != c:
            rows[c], rows[pivot] = rows[pivot], rows[c]
            det = -det
        det *= rows[c][c]
        for r in range(c + 1, n):
            f = rows[r][c] / rows[c][c]
            rows[r] = [x - f * y for x, y in zip(rows[r], rows[c])]
    return det


def rolls_by_chain(target, sides):
    """같은 기댓값을 마르코프 연쇄 + 연립방정식으로 (다른 방법으로) 계산."""
    transitions = {}
    for s in range(target):
        merged = {}
        for k in range(1, sides + 1):  # 목표를 넘으면 모두 target 한 상태로 모은다
            merged[min(s + k, target)] = merged.get(min(s + k, target), 0) + Fraction(1, sides)
        transitions[s] = merged
    transitions[target] = {}
    steps, _ = solution.absorbing_chain(transitions, [target])
    return steps[0]


def test_expected_rolls_match_the_chain_and_small_cases():
    for sides in range(1, 7):
        for target in range(1, 15):
            assert solution.expected_rolls_to_reach(target, sides) == rolls_by_chain(target, sides), (target, sides)
    assert solution.expected_rolls_to_reach(1, 6) == 1
    assert solution.expected_rolls_to_reach(2, 6) == Fraction(7, 6)
    assert solution.expected_rolls_to_reach(5, 1) == 5  # 면이 하나면 매번 1 씩
    assert solution.expected_rolls_to_reach(0, 6) == 0 and solution.expected_rolls_to_reach(-3, 6) == 0
    assert solution.expected_rolls_to_reach(2, 2) == Fraction(3, 2)  # 동전 던지듯: 1 이 나오면 한 번 더
    with pytest.raises(ValueError, match="면"):
        solution.expected_rolls_to_reach(3, 0)


def test_expected_rolls_mod_matches_the_fraction_version():
    for sides in (1, 2, 3, 6, 10):
        for target in list(range(0, 60)) + [150]:
            fraction = solution.expected_rolls_to_reach(target, sides)
            assert solution.expected_rolls_mod(target, sides) == solution.fraction_mod(fraction), (target, sides)
            assert solution.expected_rolls_mod(target, sides, 1_000_000_007) == solution.fraction_mod(fraction, 1_000_000_007)
    with pytest.raises(ValueError, match="면"):
        solution.expected_rolls_mod(5, 0)
    with pytest.raises(ValueError, match="면"):
        solution.expected_rolls_mod(5, MOD)  # 면의 수가 mod 의 배수면 역원이 없다


def test_fraction_mod():
    assert solution.fraction_mod(Fraction(1, 2)) == (MOD + 1) // 2
    assert solution.fraction_mod(Fraction(7)) == 7
    assert solution.fraction_mod(Fraction(-1, 3)) * 3 % MOD == MOD - 1
    with pytest.raises(ValueError, match="분모"):
        solution.fraction_mod(Fraction(1, MOD))


def test_modular_version_agrees_for_a_long_target_and_runs_fast_for_a_huge_one():
    fraction = solution.expected_rolls_to_reach(1500, 6)  # 분모가 6^1500 에 가까운 정확한 분수
    assert solution.expected_rolls_mod(1500, 6) == solution.fraction_mod(fraction)
    started = time.perf_counter()
    value = solution.expected_rolls_mod(10**6, 6)
    assert time.perf_counter() - started < 10
    assert 0 <= value < MOD


def test_coupon_collector_matches_n_times_harmonic_number_and_the_chain():
    for n in range(0, 12):
        harmonic = sum(Fraction(1, k) for k in range(1, n + 1))
        assert solution.coupon_collector(n) == n * harmonic, n
    assert solution.coupon_collector(1) == 1 and solution.coupon_collector(2) == 3 and solution.coupon_collector(3) == Fraction(11, 2)
    # 연쇄로 독립적으로 계산: 상태 k = 모은 종류의 수
    for n in range(1, 7):
        transitions = {k: {k: Fraction(k, n), k + 1: Fraction(n - k, n)} for k in range(n)}
        transitions[n] = {}
        steps, _ = solution.absorbing_chain(transitions, [n])
        assert steps[0] == solution.coupon_collector(n), n
    with pytest.raises(ValueError, match="n 은"):
        solution.coupon_collector(-1)


def test_sum_distribution_matches_enumerating_every_roll():
    for dice in range(0, 5):
        for sides in range(1, 6):
            distribution = solution.sum_distribution(dice, sides)
            counts = {}
            for roll in itertools.product(range(1, sides + 1), repeat=dice):
                counts[sum(roll)] = counts.get(sum(roll), 0) + 1
            assert len(distribution) == dice * sides + 1
            assert distribution == [Fraction(counts.get(s, 0), sides**dice) for s in range(dice * sides + 1)], (dice, sides)
            assert sum(distribution) == 1
            mean = sum(s * p for s, p in enumerate(distribution))
            assert mean == Fraction(dice * (sides + 1), 2)
    assert solution.sum_distribution(2, 6)[7] == Fraction(1, 6)
    assert solution.probability_sum_at_least(2, 6, 11) == Fraction(3, 36)
    assert solution.probability_sum_at_least(2, 6, 0) == 1 and solution.probability_sum_at_least(2, 6, -5) == 1
    assert solution.probability_sum_at_least(2, 6, 13) == 0
    with pytest.raises(ValueError, match="주사위"):
        solution.sum_distribution(-1, 6)
    with pytest.raises(ValueError, match="주사위"):
        solution.sum_distribution(2, 0)


def closed_form_ruin(start, goal, p):
    if p == Fraction(1, 2):
        return Fraction(start, goal)
    r = (1 - p) / p
    return (1 - r**start) / (1 - r**goal)


def test_gamblers_ruin_matches_the_closed_form():
    for goal in range(1, 9):
        for start in range(0, goal + 1):
            for p in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(3, 5)):
                assert solution.gamblers_ruin(start, goal, p) == closed_form_ruin(start, goal, p), (start, goal, p)
    with pytest.raises(ValueError, match="start"):
        solution.gamblers_ruin(5, 3, Fraction(1, 2))
    with pytest.raises(ValueError, match="start"):
        solution.gamblers_ruin(0, 0, Fraction(1, 2))


def test_symmetric_random_walk_expected_steps_and_probabilities_sum_to_one():
    n = 7
    transitions = {0: {}, n: {}}
    for i in range(1, n):
        transitions[i] = {i - 1: Fraction(1, 2), i + 1: Fraction(1, 2)}
    steps, absorption = solution.absorbing_chain(transitions, [0, n])
    for i in range(1, n):
        assert steps[i] == i * (n - i)  # 대칭 보행의 평균 흡수 시간
        assert sum(absorption[i].values()) == 1
        assert absorption[i][n] == Fraction(i, n)


def test_linearity_of_expectation_matches_enumerating_permutations():
    for n in range(0, 7):
        perms = list(itertools.permutations(range(n)))
        if n == 0:
            perms = [()]
        inversions = sum(sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j]) for p in perms)
        fixed = sum(sum(1 for i in range(n) if p[i] == i) for p in perms)
        assert solution.expected_inversions(n) == Fraction(inversions, len(perms)), n
        assert solution.expected_fixed_points(n) == Fraction(fixed, len(perms)), n


def test_main_prints_fraction_and_modular_value(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2 6\n"))
    solution.main()
    assert capsys.readouterr().out == f"7/6\n{solution.fraction_mod(Fraction(7, 6))}\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("4 1\n"))
    solution.main()
    assert capsys.readouterr().out == "4/1\n4\n"
