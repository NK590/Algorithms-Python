"""solution.py 검증: O(k n²) 기준 구현, 모든 분할을 나열하는 완전 탐색과 무작위 입력으로 비교"""
import io
import itertools
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_force(n, k, cost):
    best = None
    for cuts in itertools.combinations(range(1, n), k - 1):  # 묶음의 경계 위치
        points = (0,) + cuts + (n,)
        total = sum(cost(points[g], points[g + 1]) for g in range(k))
        if best is None or total < best:
            best = total
    return best


def test_matches_brute_force_over_all_partitions():
    rng = random.Random(0)
    for _ in range(400):
        n = rng.randint(1, 9)
        k = rng.randint(1, n)
        values = [rng.randint(0, 9) for _ in range(n)]
        for cost in (solution.cost_size_times_sum(values), solution.cost_square_of_sum(values)):
            assert solution.partition_cost(n, k, cost) == brute_force(n, k, cost), (values, k)
            assert solution.naive_partition_cost(n, k, cost) == brute_force(n, k, cost), (values, k)


def test_matches_the_quadratic_dp_on_larger_inputs():
    rng = random.Random(1)
    for _ in range(60):
        n = rng.randint(10, 60)
        k = rng.randint(1, min(n, 12))
        values = [rng.randint(0, 100) for _ in range(n)]
        for cost in (solution.cost_size_times_sum(values), solution.cost_square_of_sum(values)):
            assert solution.partition_cost(n, k, cost) == solution.naive_partition_cost(n, k, cost), (values, k)


def test_known_values_and_the_two_extremes():
    values = [1, 2, 3, 4, 5, 6]
    cost = solution.cost_size_times_sum(values)
    assert solution.partition_cost(6, 1, cost) == 6 * 21  # 전체를 한 구역
    assert solution.partition_cost(6, 6, cost) == sum(values)  # 각자 한 구역: 1·v 의 합
    assert solution.partition_cost(1, 1, cost) == 1
    # 2 개로 나누기: 가장 좋은 경계를 완전 탐색으로
    assert solution.partition_cost(6, 2, cost) == min(cost(0, c) + cost(c, 6) for c in range(1, 6))


def test_next_layer_returns_monotone_optimal_choices():
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(3, 40)
        values = [rng.randint(0, 50) for _ in range(n)]
        cost = solution.cost_size_times_sum(values)
        previous = [solution.INF] + [cost(0, i) for i in range(1, n + 1)]
        current, best_j = solution.next_layer(previous, n, cost, 1)
        for i in range(2, n + 1):
            expected = min(previous[j] + cost(j, i) for j in range(1, i))
            assert current[i] == expected, (values, i)
            assert previous[best_j[i]] + cost(best_j[i], i) == expected
        # 단조성: i 가 커져도 (가장 작은 최적 j 기준) 최적 j 는 줄어들지 않는다.  동점이면 구현의 선택이 달라질 수 있어 가장 작은 최적 j 로 비교
        smallest = [min(j for j in range(1, i) if previous[j] + cost(j, i) == current[i]) for i in range(2, n + 1)]
        assert smallest == sorted(smallest), (values, smallest)
        assert current[0] == current[1] == solution.INF  # low = 1 이면 i = 1 은 계산하지 않는다


def test_cost_functions_compute_the_documented_values():
    values = [3, 1, 4, 1, 5, 9]
    size_times_sum = solution.cost_size_times_sum(values)
    assert size_times_sum(0, 3) == 3 * (3 + 1 + 4) and size_times_sum(2, 5) == 3 * (4 + 1 + 5) and size_times_sum(4, 4) == 0
    square_of_sum = solution.cost_square_of_sum(values)
    assert square_of_sum(0, 3) == 8**2 and square_of_sum(2, 5) == 10**2 and square_of_sum(1, 2) == 1


def test_a_per_group_penalty_makes_extra_groups_costly_so_exactly_k_groups_matter():
    def penalised(j, i):  # 묶음 하나마다 고정 비용 50 + 길이의 제곱 (묶음이 늘면 손해라 "정확히 k 개" 가 중요하다)
        return 0 if i == j else (i - j) ** 2 + 50

    rng = random.Random(10)
    for _ in range(100):
        n = rng.randint(2, 9)
        k = rng.randint(1, n)
        expected = brute_force(n, k, penalised)
        assert solution.partition_cost(n, k, penalised) == expected, (n, k)
        assert solution.naive_partition_cost(n, k, penalised) == expected, (n, k)
    assert solution.partition_cost(5, 5, penalised) == 5 * 51


def test_cost_functions_satisfy_the_monge_condition_but_a_bad_cost_does_not():
    rng = random.Random(3)
    for _ in range(40):
        values = [rng.randint(0, 20) for _ in range(rng.randint(1, 7))]
        n = len(values)
        assert solution.is_monge(n, solution.cost_size_times_sum(values))
        assert solution.is_monge(n, solution.cost_square_of_sum(values))
    # 구간이 길수록 비용이 줄어드는 (사각 부등식을 깨는) 비용
    assert not solution.is_monge(4, lambda j, i: -((i - j) ** 2))
    assert solution.is_monge(0, lambda j, i: 0)


def test_invalid_k_is_rejected():
    cost = solution.cost_size_times_sum([1, 2, 3])
    for k in (0, 4, -1):
        with pytest.raises(ValueError, match="k ≤ n"):
            solution.partition_cost(3, k, cost)
        with pytest.raises(ValueError, match="k ≤ n"):
            solution.naive_partition_cost(3, k, cost)


def test_large_input_is_fast_and_correct_against_few_groups():
    rng = random.Random(4)
    n, k = 3000, 30
    values = [rng.randint(0, 10**4) for _ in range(n)]
    cost = solution.cost_size_times_sum(values)
    started = time.perf_counter()
    fast = solution.partition_cost(n, k, cost)
    assert time.perf_counter() - started < 15
    # 그룹이 2 개일 때는 완전 탐색과 비교할 수 있다
    assert solution.partition_cost(n, 2, cost) == min(cost(0, c) + cost(c, n) for c in range(1, n))
    assert fast <= solution.partition_cost(n, 2, cost)  # 구역을 더 쪼개면 비용은 늘지 않는다 (값이 음이 아님)


def test_main_reads_the_prison_input(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6 3\n1 2 3 4 5 6\n"))
    solution.main()
    values = [1, 2, 3, 4, 5, 6]
    expected = brute_force(6, 3, solution.cost_size_times_sum(values))
    assert capsys.readouterr().out == f"{expected}\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("3 5\n4 5 6\n"))  # G > L 이면 L 개의 구역으로
    solution.main()
    assert capsys.readouterr().out == "15\n"
