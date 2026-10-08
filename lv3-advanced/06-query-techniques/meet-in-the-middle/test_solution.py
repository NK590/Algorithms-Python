"""solution.py 검증: itertools 로 모든 부분집합을 만드는 순진한 방법, 작은 값에서는 DP 와 비교"""
import io
import itertools
import random
import time

from tools.loader import load_solution

solution = load_solution(__file__)


def all_subsets(values):
    for mask in range(1 << len(values)):
        yield [values[i] for i in range(len(values)) if mask >> i & 1]


def test_subset_sums_lists_every_subset_including_the_empty_one():
    rng = random.Random(0)
    for _ in range(200):
        values = [rng.randint(-5, 9) for _ in range(rng.randint(0, 9))]
        assert sorted(solution.subset_sums(values)) == sorted(sum(s) for s in all_subsets(values)), values
    assert solution.subset_sums([]) == [0]
    assert sorted(solution.subset_sums([1, 2, 4])) == [0, 1, 2, 3, 4, 5, 6, 7]


def test_count_subsets_at_most_matches_brute_force_with_negatives_and_odd_lengths():
    rng = random.Random(1)
    for _ in range(600):
        values = [rng.randint(-6, 12) for _ in range(rng.randint(0, 11))]
        limit = rng.randint(-15, 40)
        expected = sum(1 for s in all_subsets(values) if sum(s) <= limit)
        assert solution.count_subsets_at_most(values, limit) == expected, (values, limit)
    assert solution.count_subsets_at_most([], 0) == 1 and solution.count_subsets_at_most([], -1) == 0
    assert solution.count_subsets_at_most([5], 4) == 1 and solution.count_subsets_at_most([5], 5) == 2


def test_count_subsets_with_sum_matches_brute_force():
    rng = random.Random(2)
    for _ in range(600):
        values = [rng.randint(-4, 8) for _ in range(rng.randint(0, 11))]
        target = rng.randint(-8, 25)
        expected = sum(1 for s in all_subsets(values) if sum(s) == target)
        assert solution.count_subsets_with_sum(values, target) == expected, (values, target)
    assert solution.count_subsets_with_sum([1, -1], 0) == 2  # 빈 집합과 {1, -1}
    assert solution.count_subsets_with_sum([0, 0, 0], 0) == 8


def test_closest_subset_sum_matches_brute_force_and_breaks_ties_downward():
    rng = random.Random(3)
    for _ in range(600):
        values = [rng.randint(-9, 20) for _ in range(rng.randint(0, 11))]
        target = rng.randint(-30, 60)
        sums = [sum(s) for s in all_subsets(values)]
        expected = min(sums, key=lambda s: (abs(s - target), s))
        assert solution.closest_subset_sum(values, target) == expected, (values, target)
    assert solution.closest_subset_sum([2, 4], 3) == 2  # 2 와 4 가 같은 거리 -> 작은 쪽
    assert solution.closest_subset_sum([], 100) == 0
    assert solution.closest_subset_sum([7], -100) == 0


def test_knapsack_meet_matches_brute_force():
    rng = random.Random(4)
    for _ in range(500):
        items = [(rng.randint(0, 12), rng.randint(0, 20)) for _ in range(rng.randint(0, 11))]
        capacity = rng.randint(0, 40)
        expected = max(sum(v for _, v in s) for s in all_subsets(items) if sum(w for w, _ in s) <= capacity)
        assert solution.knapsack_meet(items, capacity) == expected, (items, capacity)
    assert solution.knapsack_meet([], 5) == 0
    assert solution.knapsack_meet([(10, 100)], 9) == 0 and solution.knapsack_meet([(10, 100)], 10) == 100
    assert solution.knapsack_meet([(0, 7), (3, 5)], 0) == 7  # 무게 0 인 물건은 항상 담는다


def test_four_sum_zero_count_matches_four_nested_loops():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(0, 6)
        lists = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(4)]
        expected = sum(1 for t in itertools.product(*lists) if sum(t) == 0)
        assert solution.four_sum_zero_count(*lists) == expected, lists
    assert solution.four_sum_zero_count([1], [1], [-1], [-1]) == 1
    assert solution.four_sum_zero_count([], [1], [2], [3]) == 0


def test_large_n_agrees_with_an_independent_dp():
    rng = random.Random(6)
    n = 36  # 2^36 은 훑을 수 없지만 절반씩이면 2^18
    weights = [rng.randint(0, 40) for _ in range(n)]
    limit = 500
    zeros = weights.count(0)  # 무게 0 인 원소는 넣든 빼든 합이 같으므로 부분집합 수가 2 배씩
    positive = [w for w in weights if w > 0]
    ways = [0] * (limit + 1)
    ways[0] = 1
    for w in positive:
        for s in range(limit, w - 1, -1):
            ways[s] += ways[s - w]
    started = time.perf_counter()
    assert solution.count_subsets_at_most(weights, limit) == sum(ways) * 2**zeros
    assert solution.count_subsets_with_sum(weights, 300) == ways[300] * 2**zeros
    assert time.perf_counter() - started < 10


def test_large_knapsack_agrees_with_dp():
    rng = random.Random(7)
    items = [(rng.randint(1, 60), rng.randint(1, 1000)) for _ in range(34)]
    capacity = 700
    dp = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    started = time.perf_counter()
    assert solution.knapsack_meet(items, capacity) == dp[capacity]
    assert time.perf_counter() - started < 10


def test_huge_weights_that_a_dp_table_could_not_hold():
    values = [10**9 + i for i in range(30)]
    assert solution.count_subsets_at_most(values, 10**9) == 2  # 빈 집합, {10^9}
    assert solution.count_subsets_with_sum(values, 2 * 10**9 + 1) == 1  # {10^9, 10^9 + 1}
    assert solution.closest_subset_sum(values, 3 * 10**9 + 3) == 3 * 10**9 + 3  # {0, 1, 2} 번째의 합


def test_main_counts_subsets_with_total_at_most_c(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 10\n1 2 3\n"))
    solution.main()
    assert capsys.readouterr().out == "8\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("2 1\n5 4\n"))
    solution.main()
    assert capsys.readouterr().out == "1\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("3 6\n1 2 3\n"))  # 합이 정확히 C 인 부분집합도 센다
    solution.main()
    assert capsys.readouterr().out == "8\n"
