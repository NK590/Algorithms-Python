"""solution.py 검증: 브루트포스와 비교하고, 그리디가 틀리는 경우도 일부러 확인한다"""
import io
import itertools
import random
from fractions import Fraction

from tools.loader import load_solution

solution = load_solution(__file__)


def test_max_camping_days_matches_day_by_day_simulation():
    def simulate(l, p, v):
        used = 0
        for day in range(v):  # 주기 p 의 앞 l 일만 쓸 수 있다
            if day % p < l:
                used += 1
        return used

    for p in range(2, 9):
        for l in range(1, p):
            for v in range(1, 60):
                assert solution.max_camping_days(l, p, v) == simulate(l, p, v), (l, p, v)


def test_greedy_coin_change_is_optimal_for_a_canonical_system():
    coins = [1, 5, 10, 50, 100, 500]
    for amount in range(0, 1500):
        assert solution.greedy_coin_change(coins, amount) == solution.min_coins_dp(coins, amount)
    assert solution.greedy_coin_change([1, 5, 10, 50, 100, 500, 1000], 4200) == 6  # 1000 원 4개 + 100 원 2개


def test_greedy_coin_change_fails_for_a_non_canonical_system():
    # 6 원을 4+1+1 (3개) 로 만들지만 3+3 (2개) 가 더 좋다
    assert solution.greedy_coin_change([1, 3, 4], 6) == 3
    assert solution.min_coins_dp([1, 3, 4], 6) == 2
    # 그리디는 아예 못 만든다고 답하지만 3+3 으로 만들 수 있는 경우
    assert solution.greedy_coin_change([3, 4], 6) == -1
    assert solution.min_coins_dp([3, 4], 6) == 2


def test_min_coins_dp_matches_exhaustive_search():
    rng = random.Random(0)
    for _ in range(200):
        coins = sorted(rng.sample(range(1, 9), rng.randint(1, 3)))
        amount = rng.randint(0, 20)
        best = None
        for counts in itertools.product(range(amount + 1), repeat=len(coins)):
            if sum(c * k for c, k in zip(coins, counts)) == amount:
                best = sum(counts) if best is None else min(best, sum(counts))
        assert solution.min_coins_dp(coins, amount) == (-1 if best is None else best), (coins, amount)


def test_fractional_knapsack_example():
    # 가치/무게 = 6, 5, 4. 용량 50: 60 + 100 을 담고, 마지막 물건은 무게 20 만큼(2/3)만 담아 80 → 240
    items = [(60, 10), (100, 20), (120, 30)]
    assert solution.fractional_knapsack(items, 50) == 240
    assert solution.fractional_knapsack([(10, 4)], 2) == 5
    assert solution.fractional_knapsack([(10, 4)], 0) == 0
    assert solution.fractional_knapsack([], 10) == 0


def fractional_by_vertices(items, capacity):
    """선형계획의 최적해는 많아야 하나만 쪼개진다는 사실을 이용한 독립적인 전수 검사"""
    n = len(items)
    best = Fraction(0)
    for mask in range(1 << n):
        full = [i for i in range(n) if mask >> i & 1]
        weight = sum(items[i][1] for i in full)
        if weight > capacity:
            continue
        value = Fraction(sum(items[i][0] for i in full))
        best = max(best, value)
        for j in range(n):
            if mask >> j & 1:
                continue
            fraction = min(Fraction(1), Fraction(capacity - weight, items[j][1]))
            best = max(best, value + fraction * items[j][0])
    return best


def test_fractional_knapsack_matches_exhaustive_vertices():
    rng = random.Random(1)
    for _ in range(300):
        items = [(rng.randint(1, 20), rng.randint(1, 10)) for _ in range(rng.randint(0, 6))]
        capacity = rng.randint(0, 30)
        assert solution.fractional_knapsack(items, capacity) == fractional_by_vertices(items, capacity), (items, capacity)


def compatible(a, b):
    return a[1] <= b[0] or b[1] <= a[0]


def best_selection_size(intervals):
    for size in range(len(intervals), 0, -1):
        for subset in itertools.combinations(range(len(intervals)), size):
            if all(compatible(intervals[i], intervals[j]) for i, j in itertools.combinations(subset, 2)):
                return size
    return 0


def test_activity_selection_matches_exhaustive_search():
    rng = random.Random(2)
    for _ in range(400):
        intervals = []
        for _ in range(rng.randint(0, 8)):
            start = rng.randint(0, 8)
            intervals.append((start, start + rng.randint(0, 4)))  # 길이 0 인 구간도 섞는다
        chosen = solution.activity_selection(intervals)
        assert all(compatible(a, b) for a, b in itertools.combinations(chosen, 2)), (intervals, chosen)
        assert len(chosen) == best_selection_size(intervals), (intervals, chosen)


def test_activity_selection_examples():
    assert solution.activity_selection([(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]) == [(1, 4), (5, 7), (8, 11)]
    # 끝나는 시간이 같을 때 시작이 빠른 것부터 보아야 둘 다 고른다
    assert solution.activity_selection([(3, 3), (1, 3)]) == [(1, 3), (3, 3)]
    # 가장 먼저 시작하는 것을 고르는 그리디는 틀린다: (0, 10) 하나뿐
    assert len(solution.activity_selection([(0, 10), (1, 2), (3, 4)])) == 2


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 8 20\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "14"
