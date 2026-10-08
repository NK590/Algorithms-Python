"""solution.py 검증: 정의(자기보다 작은 서로 다른 값의 개수)와 비교 + 대소 관계 보존 + 겹침은 모든 점을 직접 확인"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_compress_matches_definition():
    rng = random.Random(0)
    for _ in range(800):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 15))]
        expected = [len({w for w in values if w < v}) for v in values]
        assert solution.compress(values) == expected, values
    assert solution.compress([2, 4, -10, 4, -9]) == [2, 3, 0, 3, 1]
    assert solution.compress([1000, 999, 1000, 999, 1000, 999]) == [1, 0, 1, 0, 1, 0]
    assert solution.compress([]) == []


def test_order_is_preserved_and_range_is_dense():
    rng = random.Random(1)
    for _ in range(500):
        values = [rng.randint(-10**9, 10**9) for _ in range(rng.randint(1, 20))]
        compressed = solution.compress(values)
        for i in range(len(values)):
            for j in range(len(values)):
                assert (values[i] < values[j]) == (compressed[i] < compressed[j])
                assert (values[i] == values[j]) == (compressed[i] == compressed[j])
        assert set(compressed) == set(range(len(set(values))))  # 0 부터 빈틈없이


def test_maps_round_trip():
    rng = random.Random(2)
    for _ in range(300):
        values = [rng.randint(-100, 100) for _ in range(rng.randint(0, 15))]
        ordered, index = solution.coordinate_maps(values)
        assert ordered == sorted(set(values))
        assert [index[v] for v in values] == solution.compress(values)
        assert solution.decompress(solution.compress(values), ordered) == values


def test_ordinal_ranks_are_a_permutation_and_stable():
    rng = random.Random(3)
    for _ in range(500):
        values = [rng.randint(0, 5) for _ in range(rng.randint(0, 15))]
        ranks = solution.ordinal_ranks(values)
        assert sorted(ranks) == list(range(len(values)))
        for i in range(len(values)):
            for j in range(len(values)):
                if values[i] < values[j] or (values[i] == values[j] and i < j):
                    assert ranks[i] < ranks[j]
    assert solution.ordinal_ranks([30, 10, 20, 10]) == [3, 0, 2, 1]


def test_compress_points_keeps_relative_positions():
    rng = random.Random(4)
    for _ in range(300):
        points = [(rng.randint(-10**6, 10**6), rng.randint(-10**6, 10**6)) for _ in range(rng.randint(0, 10))]
        compressed = solution.compress_points(points)
        for (x1, y1), (c1, d1) in zip(points, compressed):
            for (x2, y2), (c2, d2) in zip(points, compressed):
                assert (x1 < x2) == (c1 < c2) and (y1 < y2) == (d1 < d2)
    assert solution.compress_points([(100, 5), (7, 5), (100, -3)]) == [(1, 1), (0, 1), (1, 0)]


def test_max_overlap_count_matches_pointwise_count():
    rng = random.Random(5)
    for _ in range(800):
        intervals = []
        for _ in range(rng.randint(0, 8)):
            l = rng.randint(0, 20)
            intervals.append((l, l + rng.randint(0, 10)))
        expected = max((sum(1 for l, r in intervals if l <= p <= r) for p in range(0, 40)), default=0)
        assert solution.max_overlap_count(intervals) == expected, intervals


def test_max_overlap_with_huge_coordinates():
    intervals = [(10**17, 10**17 + 5), (10**17 + 3, 10**17 + 9), (10**17 + 5, 10**17 + 6), (1, 2)]
    assert solution.max_overlap_count(intervals) == 3  # 10^17 + 5 에서 셋이 겹친다
    assert solution.max_overlap_count([(1, 1), (2, 2)]) == 1  # 닫힌 구간이라도 끝과 다음 시작이 이어지지 않는다
    assert solution.max_overlap_count([(1, 3), (3, 5)]) == 2  # 점 3 에서 겹친다


def test_large_input_is_fast():
    rng = random.Random(6)
    values = [rng.randint(-10**9, 10**9) for _ in range(200_000)]
    compressed = solution.compress(values)
    assert max(compressed) < len(set(values)) and len(compressed) == len(values)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5\n2 4 -10 4 -9\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "2 3 0 3 1"
