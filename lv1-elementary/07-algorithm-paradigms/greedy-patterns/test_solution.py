"""solution.py 검증: 모든 순서·모든 병합 방법·모든 부분 선택을 전수 탐색한 결과와 비교"""
import io
import itertools
import random
from functools import lru_cache

from tools.loader import load_solution

solution = load_solution(__file__)


def total_wait(order):
    elapsed = total = 0
    for t in order:
        elapsed += t
        total += elapsed
    return total


def test_min_total_wait_matches_all_orders():
    rng = random.Random(0)
    for _ in range(200):
        times = [rng.randint(1, 9) for _ in range(rng.randint(0, 6))]
        expected = min((total_wait(p) for p in itertools.permutations(times)), default=0)
        assert solution.min_total_wait(times) == expected, times
    assert solution.min_total_wait([3, 1, 4, 3, 2]) == 32


@lru_cache(maxsize=None)
def best_merge(sizes):
    if len(sizes) <= 1:
        return 0
    best = None
    for i, j in itertools.combinations(range(len(sizes)), 2):
        rest = [s for k, s in enumerate(sizes) if k not in (i, j)]
        merged = sizes[i] + sizes[j]
        cost = merged + best_merge(tuple(sorted(rest + [merged])))
        best = cost if best is None else min(best, cost)
    return best


def test_merge_cost_matches_all_merge_orders():
    rng = random.Random(1)
    for _ in range(150):
        sizes = [rng.randint(1, 12) for _ in range(rng.randint(0, 6))]
        assert solution.merge_cost(sizes) == best_merge(tuple(sorted(sizes))), sizes
    assert solution.merge_cost([10, 20, 40]) == 100
    assert solution.merge_cost([7]) == 0 and solution.merge_cost([]) == 0


def reach_by_dp(jumps):
    reachable = [False] * len(jumps)
    if jumps:
        reachable[0] = True
    for i, jump in enumerate(jumps):
        if reachable[i]:
            for nxt in range(i + 1, min(len(jumps), i + jump + 1)):
                reachable[nxt] = True
    return bool(jumps) and reachable[-1]


def test_can_reach_end_matches_reachability_table():
    rng = random.Random(2)
    for _ in range(500):
        jumps = [rng.randint(0, 3) for _ in range(rng.randint(1, 9))]
        assert solution.can_reach_end(jumps) == reach_by_dp(jumps), jumps
    assert solution.can_reach_end([2, 3, 1, 1, 4]) is True
    assert solution.can_reach_end([3, 2, 1, 0, 4]) is False  # 모두 0 번 칸 앞에서 막힌다


def test_min_rooms_matches_maximum_overlap():
    rng = random.Random(3)
    for _ in range(300):
        intervals = []
        for _ in range(rng.randint(0, 9)):
            start = rng.randint(0, 10)
            intervals.append((start, start + rng.randint(1, 5)))
        overlap = max((sum(1 for s, e in intervals if s <= t < e) for t in range(0, 20)), default=0)
        assert solution.min_rooms(intervals) == overlap, intervals
    assert solution.min_rooms([(0, 30), (5, 10), (15, 20)]) == 2
    assert solution.min_rooms([(1, 2), (2, 3), (3, 4)]) == 1  # 끝과 시작이 같으면 같은 방


def test_biggest_after_removing_matches_all_selections():
    rng = random.Random(4)
    for _ in range(300):
        digits = "".join(str(rng.randint(1, 9)) for _ in range(rng.randint(1, 8)))
        k = rng.randint(0, len(digits) - 1)
        expected = max("".join(c) for c in itertools.combinations(digits, len(digits) - k))
        assert solution.biggest_after_removing(digits, k) == expected, (digits, k)
    assert solution.biggest_after_removing("1924", 2) == "94"
    assert solution.biggest_after_removing("1231234", 3) == "3234"
    assert solution.biggest_after_removing("4177252841", 4) == "775841"
    assert solution.biggest_after_removing("54321", 2) == "543"  # 지울 횟수가 남으면 뒤에서 자른다


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n3 1 4 3 2\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "32"
