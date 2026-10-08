"""solution.py 검증: 가능한 모든 답을 하나씩 판정하는 선형 탐색(브루트포스)과 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_first_and_last_true_on_monotone_predicates():
    rng = random.Random(0)
    for _ in range(500):
        lo = rng.randint(-5, 5)
        hi = lo + rng.randint(-1, 15)
        threshold = rng.randint(lo - 2, hi + 2)
        expected_first = next((x for x in range(lo, hi + 1) if x >= threshold), hi + 1)
        assert solution.first_true(lo, hi, lambda x: x >= threshold) == expected_first
        expected_last = next((x for x in range(hi, lo - 1, -1) if x <= threshold), lo - 1)
        assert solution.last_true(lo, hi, lambda x: x <= threshold) == expected_last


def test_cable_length_matches_linear_scan():
    rng = random.Random(1)
    for _ in range(400):
        cables = [rng.randint(1, 30) for _ in range(rng.randint(1, 6))]
        need = rng.randint(1, 12)
        expected = max((L for L in range(1, max(cables) + 1) if sum(c // L for c in cables) >= need), default=0)
        assert solution.max_cable_length(cables, need) == expected, (cables, need)
    assert solution.max_cable_length([802, 743, 457, 539], 11) == 200
    assert solution.max_cable_length([], 3) == 0 and solution.max_cable_length([1], 5) == 0


def test_cutter_height_matches_linear_scan():
    rng = random.Random(2)
    for _ in range(400):
        trees = [rng.randint(1, 25) for _ in range(rng.randint(1, 6))]
        need = rng.randint(0, sum(trees) + 3)
        got = solution.max_cutter_height(trees, need)
        if sum(trees) < need:
            assert got == -1
        else:
            expected = max(h for h in range(0, max(trees) + 1) if sum(t - h for t in trees if t > h) >= need)
            assert got == expected, (trees, need)
    assert solution.max_cutter_height([20, 15, 10, 17], 7) == 15
    assert solution.max_cutter_height([], 1) == -1 and solution.max_cutter_height([5, 5], 11) == -1  # 나무가 모자라면 -1


def test_max_min_distance_matches_all_subsets():
    rng = random.Random(3)
    for _ in range(300):
        positions = rng.sample(range(0, 40), rng.randint(2, 8))
        count = rng.randint(2, len(positions))
        pts = sorted(positions)
        expected = max(min(b - a for a, b in zip(c, c[1:])) for c in itertools.combinations(pts, count))
        assert solution.max_min_distance(positions, count) == expected, (positions, count)
    assert solution.max_min_distance([1, 2, 8, 4, 9], 3) == 3
    assert solution.max_min_distance([1, 5], 1) == 0 and solution.max_min_distance([1, 5], 3) == 0


def test_split_array_matches_all_partitions():
    rng = random.Random(4)
    for _ in range(300):
        numbers = [rng.randint(0, 9) for _ in range(rng.randint(1, 8))]
        parts = rng.randint(1, len(numbers))
        best = None
        for cuts in itertools.combinations(range(1, len(numbers)), parts - 1):
            bounds = [0, *cuts, len(numbers)]
            worst = max(sum(numbers[a:b]) for a, b in zip(bounds, bounds[1:]))
            best = worst if best is None else min(best, worst)
        assert solution.split_array_min_largest_sum(numbers, parts) == best, (numbers, parts)
    assert solution.split_array_min_largest_sum([7, 2, 5, 10, 8], 2) == 18
    assert solution.split_array_min_largest_sum([], 3) == 0


def test_min_time_matches_linear_scan():
    rng = random.Random(5)
    for _ in range(300):
        speeds = [rng.randint(1, 9) for _ in range(rng.randint(1, 5))]
        jobs = rng.randint(0, 20)
        expected = next((t for t in range(0, 200) if sum(t // s for s in speeds) >= jobs), None)
        assert solution.min_time_to_finish(speeds, jobs) == (0 if jobs <= 0 else expected), (speeds, jobs)
    assert solution.min_time_to_finish([7, 10], 6) == 28


def test_huge_answers_take_logarithmic_steps():
    # 답의 범위가 10^18 이어도 판정 함수는 60 번 정도만 호출된다
    calls = []

    def ok(x):
        calls.append(x)
        return x * x <= 10**30

    assert solution.last_true(1, 10**18, ok) == 10**15
    assert len(calls) <= 64


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4 11\n802\n743\n457\n539\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "200"
