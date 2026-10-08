"""solution.py 검증: 정수 격자의 모든 점/칸을 직접 확인하는 방법과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_max_overlap_matches_pointwise_count_for_half_open_intervals():
    rng = random.Random(0)
    for _ in range(800):
        intervals = []
        for _ in range(rng.randint(0, 8)):
            start = rng.randint(0, 15)
            intervals.append((start, start + rng.randint(1, 8)))
        expected = max((sum(1 for s, e in intervals if s <= t < e) for t in range(0, 30)), default=0)
        assert solution.max_overlap(intervals) == expected, intervals
    assert solution.max_overlap([(0, 30), (5, 10), (15, 20)]) == 2
    assert solution.max_overlap([(1, 2), (2, 3), (3, 4)]) == 1  # 끝과 시작이 맞닿아도 겹치지 않는다


def merge_by_doubling(intervals):
    """닫힌 정수 구간을 2 배 좌표의 점 집합으로 바꿔 합집합을 만든 뒤, 이어진 점들의 묶음으로 다시 구간을 만든다 (정수 사이의 틈도 구별된다)"""
    points = set()
    for l, r in intervals:
        points |= set(range(2 * l, 2 * r + 1))
    result, run = [], []
    for p in sorted(points):
        if run and p != run[-1] + 1:
            result.append((run[0] // 2, run[-1] // 2))
            run = []
        run.append(p)
    if run:
        result.append((run[0] // 2, run[-1] // 2))
    return result


def test_merge_intervals_matches_point_set_union():
    rng = random.Random(1)
    for _ in range(800):
        intervals = []
        for _ in range(rng.randint(0, 8)):
            l = rng.randint(0, 20)
            intervals.append((l, l + rng.randint(0, 6)))
        assert solution.merge_intervals(intervals) == merge_by_doubling(intervals), intervals
    assert solution.merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == [(1, 6), (8, 10), (15, 18)]
    assert solution.merge_intervals([(1, 4), (4, 5)]) == [(1, 5)]  # 끝점이 맞닿으면 합친다
    assert solution.merge_intervals([(1, 4), (5, 8)]) == [(1, 4), (5, 8)]  # 사이에 틈이 있다


def test_covered_length():
    rng = random.Random(2)
    for _ in range(500):
        segments = []
        for _ in range(rng.randint(0, 8)):
            l = rng.randint(0, 20)
            segments.append((l, l + rng.randint(0, 6)))
        # 단위 구간 [i, i+1] 이 하나라도 덮이는지 센다
        covered = {i for l, r in segments for i in range(l, r)}
        assert solution.covered_length(segments) == len(covered), segments
    assert solution.covered_length([(1, 3), (2, 5), (3, 5), (6, 7)]) == 5


def skyline_by_unit_cells(buildings):
    """정수 x 마다 [x, x+1) 칸의 높이를 직접 구하고, 높이가 바뀌는 지점을 모은다"""
    if not buildings:
        return []
    low = min(l for l, _, _ in buildings)
    high = max(r for _, r, _ in buildings)
    heights = {x: max((h for l, r, h in buildings if l <= x < r), default=0) for x in range(low, high + 1)}
    result, previous = [], 0
    for x in range(low, high + 1):
        if heights[x] != previous:
            result.append((x, heights[x]))
            previous = heights[x]
    return result


def test_skyline_matches_unit_cell_heights():
    rng = random.Random(3)
    for _ in range(800):
        buildings = []
        for _ in range(rng.randint(0, 6)):
            l = rng.randint(0, 12)
            buildings.append((l, l + rng.randint(1, 6), rng.randint(1, 8)))
        assert solution.skyline(buildings) == skyline_by_unit_cells(buildings), buildings
    assert solution.skyline([(2, 9, 10), (3, 7, 15), (5, 12, 12), (15, 20, 10), (19, 24, 8)]) == [
        (2, 10), (3, 15), (7, 12), (12, 0), (15, 10), (20, 8), (24, 0)
    ]
    assert solution.skyline([]) == [] and solution.skyline([(0, 2, 3), (2, 4, 3)]) == [(0, 3), (4, 0)]  # 같은 높이가 이어지면 하나로


def test_rectangle_union_area_matches_cell_count():
    rng = random.Random(4)
    for _ in range(500):
        rects = []
        for _ in range(rng.randint(0, 6)):
            x1, y1 = rng.randint(0, 8), rng.randint(0, 8)
            rects.append((x1, y1, x1 + rng.randint(1, 6), y1 + rng.randint(1, 6)))
        cells = {(x, y) for x1, y1, x2, y2 in rects for x in range(x1, x2) for y in range(y1, y2)}
        assert solution.rectangle_union_area(rects) == len(cells), rects
    assert solution.rectangle_union_area([(0, 0, 2, 2), (1, 1, 3, 3)]) == 7
    assert solution.rectangle_union_area([(0, 0, 4, 4), (1, 1, 2, 2)]) == 16  # 안에 포함
    assert solution.rectangle_union_area([]) == 0


def test_large_input():
    rng = random.Random(5)
    segments = []
    for _ in range(100_000):
        l = rng.randint(0, 10**9)
        segments.append((l, l + rng.randint(0, 1000)))
    merged = solution.merge_intervals(segments)
    assert all(a[1] < b[0] for a, b in zip(merged, merged[1:]))  # 서로소이고 정렬됨
    assert solution.max_overlap([(s, e + 1) for s, e in segments]) >= 1


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n1 3\n3 5\n4 6\n7 8\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "6"
    monkeypatch.setattr("sys.stdin", io.StringIO("2\n5 1\n2 4\n"))  # 끝점 순서가 뒤바뀐 입력
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
