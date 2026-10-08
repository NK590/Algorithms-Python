"""solution.py 검증: 부분집합 전수 조사, 물건 복제 후 전수 조사, 재귀 열거와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_01(items, capacity):
    best = 0
    for mask in range(1 << len(items)):
        picked = [items[i] for i in range(len(items)) if mask >> i & 1]
        if sum(w for w, _ in picked) <= capacity:
            best = max(best, sum(v for _, v in picked))
    return best


def random_items(rng, max_n=9, max_w=8, max_v=20):
    return [(rng.randint(1, max_w), rng.randint(0, max_v)) for _ in range(rng.randint(0, max_n))]


def test_01_matches_brute_force_in_all_three_forms():
    rng = random.Random(0)
    for _ in range(500):
        items = random_items(rng)
        capacity = rng.randint(0, 20)
        expected = brute_01(items, capacity)
        assert solution.knapsack_01(items, capacity) == expected, (items, capacity)
        assert solution.knapsack_table(items, capacity)[len(items)][capacity] == expected
        best, chosen = solution.knapsack_01_items(items, capacity)
        assert best == expected
        assert sum(items[i][1] for i in chosen) == expected and sum(items[i][0] for i in chosen) <= capacity
        assert len(set(chosen)) == len(chosen)


def test_readme_example():
    items = [(6, 13), (4, 8), (3, 6), (5, 12)]
    assert solution.knapsack_01(items, 7) == 14
    best, chosen = solution.knapsack_01_items(items, 7)
    assert (best, chosen) == (14, [1, 2])
    assert solution.knapsack_unbounded([(3, 6), (4, 8)], 7) == 14
    assert solution.knapsack_01(items, 0) == 0 and solution.knapsack_01([], 5) == 0


def test_greedy_by_ratio_fails_for_01():
    # 무게당 가치가 가장 큰 (6, 7) 을 먼저 담으면 (5, 5)+(5, 5) 보다 못하다
    items = [(6, 7), (5, 5), (5, 5)]
    assert solution.knapsack_01(items, 10) == 10


def brute_unbounded(items, capacity):
    best = 0
    ranges = [range(capacity // w + 1) for w, _ in items]
    for counts in itertools.product(*ranges):
        if sum(c * w for c, (w, _) in zip(counts, items)) <= capacity:
            best = max(best, sum(c * v for c, (_, v) in zip(counts, items)))
    return best


def test_unbounded_matches_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        items = random_items(rng, max_n=4, max_w=6)
        capacity = rng.randint(0, 14)
        assert solution.knapsack_unbounded(items, capacity) == brute_unbounded(items, capacity), (items, capacity)


def test_bounded_matches_copies_in_01():
    rng = random.Random(2)
    for _ in range(300):
        items = [(rng.randint(1, 6), rng.randint(0, 15), rng.randint(0, 5)) for _ in range(rng.randint(0, 4))]
        capacity = rng.randint(0, 20)
        copies = [(w, v) for w, v, c in items for _ in range(c)]
        assert solution.knapsack_bounded(items, capacity) == brute_01(copies, capacity), (items, capacity)


def min_coins_by_bfs(coins, amount):
    dist = {0: 0}
    frontier = [0]
    while frontier:
        nxt = []
        for s in frontier:
            for c in coins:
                if s + c <= amount and s + c not in dist:
                    dist[s + c] = dist[s] + 1
                    nxt.append(s + c)
        frontier = nxt
    return dist.get(amount, -1)


def combinations_by_recursion(coins, amount, start=0):
    if amount == 0:
        return 1
    return sum(combinations_by_recursion(coins, amount - coins[i], i) for i in range(start, len(coins)) if coins[i] <= amount)


def orderings_by_recursion(coins, amount):
    if amount == 0:
        return 1
    return sum(orderings_by_recursion(coins, amount - c) for c in coins if c <= amount)


def test_coin_problems_match_independent_methods():
    rng = random.Random(3)
    for _ in range(300):
        coins = sorted(rng.sample(range(1, 8), rng.randint(1, 4)))
        amount = rng.randint(0, 14)
        assert solution.min_coins(coins, amount) == min_coins_by_bfs(coins, amount), (coins, amount)
        assert solution.count_coin_ways(coins, amount) == combinations_by_recursion(coins, amount), (coins, amount)
        assert solution.count_coin_orderings(coins, amount) == orderings_by_recursion(coins, amount), (coins, amount)
    assert solution.count_coin_ways([1, 2, 5], 5) == 4  # 1+1+1+1+1, 1+1+1+2, 1+2+2, 5
    assert solution.count_coin_orderings([1, 2], 3) == 3  # 1+1+1, 1+2, 2+1 (순서가 다르면 다른 경우)
    assert solution.count_coin_ways([1, 2], 3) == 2
    assert solution.min_coins([2], 3) == -1 and solution.min_coins([5], 0) == 0


def test_subset_sum_and_partition_match_enumeration():
    rng = random.Random(4)
    for _ in range(500):
        numbers = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
        target = rng.randint(0, 30)
        expected = any(sum(c) == target for r in range(len(numbers) + 1) for c in itertools.combinations(numbers, r))
        assert solution.subset_sum(numbers, target) == expected, (numbers, target)
        total = sum(numbers)
        half = total % 2 == 0 and any(sum(c) == total // 2 for r in range(len(numbers) + 1) for c in itertools.combinations(numbers, r))
        assert solution.can_partition_equal(numbers) == half
    assert solution.subset_sum([3, 5], -1) is False and solution.subset_sum([], 0) is True


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4 7\n6 13\n4 8\n3 6\n5 12\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "14"
