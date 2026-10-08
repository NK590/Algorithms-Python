"""solution.py 검증: 개수 제한이 있는 느린 DP·구간 선택 전수 탐색, 합성한 볼록 함수와 비교하고 단조성·볼록성 같은 성질을 확인"""
import io
import itertools
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def synthetic_evaluators(slopes, start):
    """F(0) = start, F(c+1) - F(c) = slopes[c] 인 함수의 완화 문제 평가기 (동점이면 개수가 많은 쪽)."""
    values = [start]
    for s in slopes:
        values.append(values[-1] + s)

    def evaluate_min(lam):
        best = min(range(len(values)), key=lambda c: (values[c] + lam * c, -c))
        return values[best] + lam * best, best

    def evaluate_max(lam):
        best = max(range(len(values)), key=lambda c: (values[c] - lam * c, c))
        return values[best] - lam * best, best

    return values, evaluate_min, evaluate_max


def test_aliens_trick_recovers_every_value_of_a_synthetic_convex_or_concave_function():
    rng = random.Random(0)
    for _ in range(300):
        m = rng.randint(1, 10)
        slopes = sorted(rng.randint(-12, 12) for _ in range(m))  # 오름차순 기울기: 볼록
        values, evaluate_min, _ = synthetic_evaluators(slopes, rng.randint(-5, 5))
        for k in range(m + 1):
            assert solution.aliens_trick(evaluate_min, k, -40, 40, maximize=False) == values[k], (slopes, k)
        concave = sorted((rng.randint(-12, 12) for _ in range(m)), reverse=True)  # 내림차순 기울기: 오목
        values, _, evaluate_max = synthetic_evaluators(concave, rng.randint(-5, 5))
        for k in range(m + 1):
            assert solution.aliens_trick(evaluate_max, k, -40, 40, maximize=True) == values[k], (concave, k)


def test_aliens_trick_errors_and_tie_breaking_matters():
    values, evaluate_min, _ = synthetic_evaluators([1, 1, 1], 0)  # 기울기가 전부 같으면 모든 개수가 동점
    assert solution.aliens_trick(evaluate_min, 2, -5, 5, maximize=False) == 2
    with pytest.raises(ValueError, match="k 개"):
        solution.aliens_trick(evaluate_min, 4, -5, 5, maximize=False)  # 최대 3 개
    with pytest.raises(ValueError, match="low"):
        solution.aliens_trick(evaluate_min, 1, 5, -5, maximize=False)

    def evaluate_prefers_fewer(lam):  # 동점에서 개수가 적은 쪽을 돌려주면 중간 개수 k 에서 틀린 답이 나온다
        best = min(range(len(values)), key=lambda c: (values[c] + lam * c, c))
        return values[best] + lam * best, best

    assert solution.aliens_trick(evaluate_prefers_fewer, 2, -5, 5, maximize=False) == 1 != values[2]  # F(2) = 2 여야 한다


def brute_non_adjacent(a, k):
    best = None
    for mask in range(1 << len(a)):
        selected = [bool(mask >> i & 1) for i in range(len(a))]
        runs = sum(1 for i in range(len(a)) if selected[i] and (i == 0 or not selected[i - 1]))
        if runs == k:
            total = sum(x for x, s in zip(a, selected) if s)
            if best is None or total > best:
                best = total
    return best


def test_k_subarrays_match_enumeration_and_the_slow_dp():
    rng = random.Random(1)
    for _ in range(250):
        n = rng.randint(1, 9)
        a = [rng.randint(-9, 9) for _ in range(n)]
        assert solution.max_sum_k_subarrays(a, 0) == 0
        for k in range(1, (n + 1) // 2 + 1):
            expected = brute_non_adjacent(a, k)
            assert solution.max_sum_k_subarrays(a, k) == expected == solution.max_sum_k_subarrays_dp(a, k), (a, k)
        for k in range(1, n + 1):  # 인접 허용: 느린 DP 와만 비교
            assert solution.max_sum_k_subarrays(a, k, allow_adjacent=True) == solution.max_sum_k_subarrays_dp(a, k, True), (a, k)
    for _ in range(100):
        n = rng.randint(10, 30)
        a = [rng.randint(-50, 50) for _ in range(n)]
        for k in range(1, (n + 1) // 2 + 1):
            assert solution.max_sum_k_subarrays(a, k) == solution.max_sum_k_subarrays_dp(a, k)


def test_best_total_is_concave_in_k_and_infeasible_k_is_rejected():
    rng = random.Random(2)
    for _ in range(100):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(3, 20))]
        for allow_adjacent in (False, True):
            limit = len(a) if allow_adjacent else (len(a) + 1) // 2
            f = [solution.max_sum_k_subarrays_dp(a, k, allow_adjacent) for k in range(1, limit + 1)]
            assert solution.convexity_violations([-x for x in f]) == [], (a, allow_adjacent)  # -F 가 볼록 = F 가 오목
    with pytest.raises(ValueError):
        solution.max_sum_k_subarrays([1, 2, 3], 3)  # 인접하지 않으면 최대 2 개
    with pytest.raises(ValueError):
        solution.max_sum_k_subarrays([1, 2, 3], -1)
    assert solution.max_sum_k_subarrays([1, 2, 3], 3, allow_adjacent=True) == 6
    assert solution.max_sum_k_subarrays([], 0) == 0 and solution.max_sum_k_subarrays([-5], 1) == -5
    with pytest.raises(ValueError):
        solution.max_sum_k_subarrays_dp([1, 2], 3)


def test_convexity_violations_helper():
    assert solution.convexity_violations([9, 5, 3, 2, 2]) == []
    assert solution.convexity_violations([9, 5, 4, 1, 0]) == [2]  # 5, 4, 1: 5 + 1 < 2·4
    assert solution.convexity_violations([1, 2]) == [] and solution.convexity_violations([]) == []


def square_cost(a):
    prefix = [0]
    for x in a:
        prefix.append(prefix[-1] + x)
    return lambda l, r: (prefix[r] - prefix[l]) ** 2


def test_generic_partition_matches_the_slow_dp():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 10)
        a = [rng.randint(0, 9) for _ in range(n)]
        base = square_cost(a)
        fixed = rng.randint(0, 20)
        for name, cost in (("squares", base), ("squares+fixed", lambda l, r, base=base, fixed=fixed: base(l, r) + fixed), ("length²", lambda l, r: (r - l) ** 2)):
            for k in range(1, n + 1):
                assert solution.partition_min_cost(n, cost, k) == solution.partition_min_cost_dp(n, cost, k), (name, a, k)
    with pytest.raises(ValueError, match="1 ≤ k"):
        solution.partition_min_cost(3, lambda l, r: 1, 4)
    with pytest.raises(ValueError, match="1 ≤ k"):
        solution.partition_min_cost(3, lambda l, r: 1, 0)


def test_sum_of_squares_partition_with_the_hull_matches_the_slow_dp():
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(1, 14)
        a = [rng.choice([0, 0, 1, 2, 5, 9, 20]) for _ in range(n)]  # 0 이 섞이면 접두사 합이 같은 직선(기울기 같음)이 생긴다
        cost = square_cost(a)
        for k in range(1, n + 1):
            assert solution.partition_sum_of_squares(a, k) == solution.partition_min_cost_dp(n, cost, k), (a, k)
    with pytest.raises(ValueError, match="음이 아닌"):
        solution.partition_sum_of_squares([1, -2, 3], 2)
    with pytest.raises(ValueError):
        solution.partition_sum_of_squares([1, 2], 3)


def test_large_inputs_are_fast():
    rng = random.Random(5)
    a = [rng.randint(-10**6, 10**6) for _ in range(10000)]
    started = time.perf_counter()
    k = 1800
    before, here, after = (solution.max_sum_k_subarrays(a, c) for c in (k - 1, k, k + 1))
    assert time.perf_counter() - started < 60
    assert before + after <= 2 * here  # 오목성 (이웃한 세 값에서 확인): 느린 DP 없이 큰 입력의 결과를 검증
    b = [rng.randint(0, 1000) for _ in range(30000)]
    started = time.perf_counter()
    values = [solution.partition_sum_of_squares(b, c) for c in (99, 100, 101)]
    assert time.perf_counter() - started < 60
    assert values[0] + values[2] >= 2 * values[1]  # 구간 수에 대해 볼록
    assert values[0] > values[1] > values[2]  # 구간이 많을수록 제곱합이 줄어든다


def test_main_interval_division_format(monkeypatch, capsys):
    text = "6 2\n1\n-2\n3\n4\n-5\n6\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == str(brute_non_adjacent([1, -2, 3, 4, -5, 6], 2)) + "\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("3 2\n2 2 2\n"))  # 인접이 허용되면 6, 허용되지 않으면 2 + 2 = 4: main 은 인접하지 않은 구간
    solution.main()
    assert capsys.readouterr().out == "4\n"
