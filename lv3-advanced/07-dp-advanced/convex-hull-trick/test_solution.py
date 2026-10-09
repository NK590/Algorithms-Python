"""solution.py 검증: 모든 직선을 직접 훑는 순진한 방법, O(n²) DP, 땅을 묶는 모든 방법을 나열하는 완전 탐색과 비교"""
import io
import itertools
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def brute_min(lines, x):
    return min(m * x + b for m, b in lines)


def test_monotone_cht_min_matches_scanning_all_lines():
    rng = random.Random(0)
    for _ in range(600):
        count = rng.randint(1, 12)
        slopes = sorted((rng.randint(-8, 8) for _ in range(count)), reverse=True)  # 같은 기울기가 섞인다
        lines = [(m, rng.randint(-30, 30)) for m in slopes]
        hull = solution.MonotoneCHT()
        for m, b in lines:
            hull.add(m, b)
        assert len(hull) <= len(lines)
        for x in range(-12, 13):
            assert hull.query(x) == brute_min(lines, x), (lines, x)


def test_monotone_cht_max_matches_scanning_all_lines():
    rng = random.Random(1)
    for _ in range(400):
        count = rng.randint(1, 10)
        slopes = sorted(rng.randint(-8, 8) for _ in range(count))  # 최대: 오름차순
        lines = [(m, rng.randint(-30, 30)) for m in slopes]
        hull = solution.MonotoneCHT(maximize=True)
        for m, b in lines:
            hull.add(m, b)
        for x in range(-10, 11):
            assert hull.query(x) == max(m * x + b for m, b in lines), (lines, x)


def test_query_monotone_agrees_with_scanning_while_lines_are_added_between_queries():
    rng = random.Random(2)
    for _ in range(600):
        count = rng.randint(2, 15)
        slopes = sorted((rng.randint(-6, 6) for _ in range(count)), reverse=True)
        lines = [(m, rng.randint(-20, 20)) for m in slopes]
        xs = sorted(rng.randint(-15, 15) for _ in range(count))  # 질의 x 는 줄어들지 않는다
        hull, hull_binary = solution.MonotoneCHT(), solution.MonotoneCHT()
        for k, ((m, b), x) in enumerate(zip(lines, xs), start=1):  # 직선 하나 추가하고 질의 하나, 번갈아
            hull.add(m, b)
            hull_binary.add(m, b)
            assert hull.query_monotone(x) == brute_min(lines[:k], x), (lines, xs, k)
            assert hull_binary.query(x) == brute_min(lines[:k], x), (lines, xs, k)


def test_query_monotone_in_maximize_mode():
    rng = random.Random(11)
    for _ in range(300):
        count = rng.randint(2, 12)
        slopes = sorted(rng.randint(-6, 6) for _ in range(count))  # 최대: 기울기 오름차순
        lines = [(m, rng.randint(-20, 20)) for m in slopes]
        xs = sorted(rng.randint(-15, 15) for _ in range(count))
        hull = solution.MonotoneCHT(maximize=True)
        for k, ((m, b), x) in enumerate(zip(lines, xs), start=1):
            hull.add(m, b)
            assert hull.query_monotone(x) == max(m2 * x + b2 for m2, b2 in lines[:k]), (lines, xs, k)


def test_equal_slopes_keep_the_smaller_intercept_and_order_is_enforced():
    hull = solution.MonotoneCHT()
    hull.add(2, 10)
    hull.add(2, 5)
    hull.add(2, 7)  # 쓸모없다
    assert len(hull) == 1 and hull.query(0) == 5
    with pytest.raises(ValueError, match="정렬된 순서"):
        hull.add(3, 0)
    top = solution.MonotoneCHT(maximize=True)
    top.add(1, 0)
    with pytest.raises(ValueError, match="정렬된 순서"):
        top.add(0, 0)
    with pytest.raises(ValueError, match="직선이 없습니다"):
        solution.MonotoneCHT().query(0)
    with pytest.raises(ValueError, match="직선이 없습니다"):
        solution.MonotoneCHT().query_monotone(0)


def test_useless_middle_line_is_dropped_even_when_three_lines_meet_at_one_point():
    hull = solution.MonotoneCHT()
    for line in [(3, 0), (2, 10), (1, 0)]:  # 가운데 직선 y = 2x + 10 은 두 직선의 아래 껍질에 못 든다
        hull.add(*line)
    assert len(hull) == 2
    concurrent = [(2, 0), (1, 1), (0, 2)]  # 세 직선이 모두 (1, 2) 를 지난다: 가운데는 최소가 되는 x 가 없다
    hull = solution.MonotoneCHT()
    for line in concurrent:
        hull.add(*line)
    assert len(hull) == 2
    assert [hull.query(x) for x in range(-3, 6)] == [brute_min(concurrent, x) for x in range(-3, 6)]
    separate = [(2, 0), (1, 1), (0, 4)]  # 교점이 서로 다르면 세 직선이 모두 필요하다
    hull = solution.MonotoneCHT()
    for line in separate:
        hull.add(*line)
    assert len(hull) == 3
    assert [hull.query(x) for x in range(-3, 6)] == [brute_min(separate, x) for x in range(-3, 6)]


def test_li_chao_tree_matches_scanning_all_lines_in_any_order():
    rng = random.Random(3)
    for _ in range(300):
        lo = rng.randint(-20, 0)
        hi = lo + rng.randint(0, 40)
        tree = solution.LiChaoTree(lo, hi)
        assert tree.query(lo) is None
        lines = []
        for _ in range(rng.randint(1, 12)):
            line = (rng.randint(-9, 9), rng.randint(-60, 60))
            lines.append(line)
            tree.add_line(*line)
            for x in range(lo, hi + 1):
                assert tree.query(x) == brute_min(lines, x), (lo, hi, lines, x)


def test_li_chao_tree_large_domain_and_errors():
    rng = random.Random(4)
    tree = solution.LiChaoTree(-10**9, 10**9)
    lines = [(rng.randint(-10**9, 10**9), rng.randint(-10**18, 10**18)) for _ in range(300)]
    for line in lines:
        tree.add_line(*line)
    for x in [-10**9, -1, 0, 1, 10**9] + [rng.randint(-10**9, 10**9) for _ in range(300)]:
        assert tree.query(x) == brute_min(lines, x)
    with pytest.raises(ValueError, match="정의역"):
        tree.query(10**9 + 1)
    with pytest.raises(ValueError, match="lo ≤ hi"):
        solution.LiChaoTree(1, 0)
    single = solution.LiChaoTree(5, 5)
    single.add_line(2, 1)
    single.add_line(1, 5)
    assert single.query(5) == 10  # min(11, 10)


def land_purchase_brute(lands):
    n = len(lands)
    best = None

    def assign(index, groups):
        nonlocal best
        if index == n:
            total = sum(max(w for w, _ in g) * max(h for _, h in g) for g in groups)
            if best is None or total < best:
                best = total
            return
        for g in groups:  # 기존 묶음에 넣거나
            g.append(lands[index])
            assign(index + 1, groups)
            g.pop()
        groups.append([lands[index]])  # 새 묶음을 만든다
        assign(index + 1, groups)
        groups.pop()

    assign(0, [])
    return best


def test_land_purchase_matches_all_set_partitions():
    rng = random.Random(5)
    for _ in range(300):
        lands = [(rng.randint(1, 12), rng.randint(1, 12)) for _ in range(rng.randint(1, 7))]
        assert solution.land_purchase_cost(lands) == land_purchase_brute(lands), lands
    assert solution.land_purchase_cost([]) == 0
    assert solution.land_purchase_cost([(4, 5)]) == 20
    # 한 땅이 다른 땅에 덮이면 공짜
    assert solution.land_purchase_cost([(4, 5), (3, 2), (4, 5)]) == 20
    # 네 직사각형을 묶어 구매하는 검산 예제
    assert solution.land_purchase_cost([(100, 1), (15, 15), (20, 5), (1, 100)]) == 500


def test_land_purchase_matches_the_quadratic_dp_on_larger_inputs():
    rng = random.Random(6)
    for _ in range(40):
        lands = [(rng.randint(1, 10**4), rng.randint(1, 10**4)) for _ in range(rng.randint(1, 200))]
        kept = []
        tallest = 0
        for w, h in sorted(lands, key=lambda land: (-land[0], -land[1])):
            if h > tallest:
                kept.append((w, h))
                tallest = h
        kept.reverse()
        m = len(kept)
        dp = [0] + [None] * m
        for i in range(1, m + 1):
            dp[i] = min(dp[j] + kept[j][1] * kept[i - 1][0] for j in range(i))
        assert solution.land_purchase_cost(lands) == dp[m]


def test_min_cost_batches_matches_the_quadratic_dp():
    rng = random.Random(7)
    for _ in range(400):
        values = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]
        c = rng.randint(0, 30)
        n = len(values)
        prefix = [0]
        for v in values:
            prefix.append(prefix[-1] + v)
        dp = [0] + [None] * n
        for i in range(1, n + 1):
            dp[i] = min(dp[j] + (prefix[i] - prefix[j]) ** 2 + c for j in range(i))
        assert solution.min_cost_batches(values, c) == dp[n], (values, c)
    assert solution.min_cost_batches([], 5) == 0
    assert solution.min_cost_batches([3], 5) == 14
    with pytest.raises(ValueError, match="음이 아니어야"):
        solution.min_cost_batches([1, -2, 3], 1)


def test_large_input_is_linear_time():
    rng = random.Random(8)
    lands = [(rng.randint(1, 10**9), rng.randint(1, 10**9)) for _ in range(200000)]
    started = time.perf_counter()
    solution.land_purchase_cost(lands)
    values = [rng.randint(0, 100) for _ in range(200000)]
    solution.min_cost_batches(values, 1000)
    assert time.perf_counter() - started < 15


def test_main_reads_lands(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n100 1\n15 15\n20 5\n1 100\n"))
    solution.main()
    assert capsys.readouterr().out == "500\n"
