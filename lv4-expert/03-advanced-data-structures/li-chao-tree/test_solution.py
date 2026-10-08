"""solution.py 검증: 모든 직선·선분을 직접 평가하는 순진한 방법과 무작위 삽입·질의·되돌리기·시간 구간으로 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def brute(segments, x, maximize=False):
    values = [m * x + b for m, b, left, right in segments if left <= x <= right]
    if not values:
        return None
    return max(values) if maximize else min(values)


def test_full_domain_lines_match_brute_force_in_both_modes():
    rng = random.Random(0)
    for maximize in (False, True):
        for _ in range(150):
            lo = rng.randint(-20, 5)
            hi = rng.randint(lo, lo + 40)
            tree = solution.LiChaoTree(lo, hi, maximize)
            lines = []
            for _ in range(rng.randint(0, 12)):
                m, b = rng.randint(-6, 6), rng.randint(-50, 50)
                tree.add_line(m, b)
                lines.append((m, b, lo, hi))
                for x in range(lo, hi + 1):
                    assert tree.query(x) == brute(lines, x, maximize), (lo, hi, lines, x)
            if not lines:
                assert tree.query(lo) is None


def test_segments_match_brute_force_in_both_modes():
    rng = random.Random(1)
    for maximize in (False, True):
        for _ in range(300):
            lo = rng.randint(-15, 5)
            hi = rng.randint(lo, lo + 35)
            tree = solution.LiChaoTree(lo, hi, maximize)
            segments = []
            for _ in range(rng.randint(1, 14)):
                m, b = rng.randint(-5, 5), rng.randint(-40, 40)
                left = rng.randint(lo - 5, hi + 5)
                right = rng.randint(left - 1, hi + 5)  # 비어 있는 선분(right < left)도 섞는다
                tree.add_segment(m, b, left, right)
                segments.append((m, b, left, right))
            for x in range(lo, hi + 1):
                assert tree.query(x) == brute(segments, x, maximize), (lo, hi, segments, x)


def test_points_outside_every_segment_have_no_answer():
    tree = solution.LiChaoTree(0, 10)
    tree.add_segment(1, 0, 3, 5)
    assert [tree.query(x) for x in range(11)] == [None, None, None, 3, 4, 5, None, None, None, None, None]
    tree.add_segment(-1, 20, 5, 8)
    assert tree.query(5) == 5 and tree.query(6) == 14 and tree.query(8) == 12 and tree.query(9) is None


def test_segment_must_not_leak_to_the_children_outside_its_range():
    # 선분이 노드 구간 전체를 덮지 않는데 그 노드에 넣으면 구간 밖에서도 답이 나온다: 잎 하나짜리 선분들로 확인
    tree = solution.LiChaoTree(0, 15)
    tree.add_segment(0, 100, 7, 7)
    assert [tree.query(x) for x in range(16)] == [None] * 7 + [100] + [None] * 8


def test_snapshot_and_rollback_restore_every_query():
    rng = random.Random(2)
    for _ in range(100):
        tree = solution.LiChaoTree(-10, 10)
        kept = []
        for _ in range(rng.randint(0, 5)):
            m, b, left = rng.randint(-4, 4), rng.randint(-30, 30), rng.randint(-10, 10)
            right = rng.randint(left, 10)
            tree.add_segment(m, b, left, right)
            kept.append((m, b, left, right))
        mark = tree.snapshot()
        before = [tree.query(x) for x in range(-10, 11)]
        extra = []
        for _ in range(rng.randint(1, 6)):
            m, b, left = rng.randint(-4, 4), rng.randint(-30, 30), rng.randint(-10, 10)
            right = rng.randint(left, 10)
            tree.add_segment(m, b, left, right)
            extra.append((m, b, left, right))
        assert [tree.query(x) for x in range(-10, 11)] == [brute(kept + extra, x) for x in range(-10, 11)]
        tree.rollback(mark)
        assert [tree.query(x) for x in range(-10, 11)] == before == [brute(kept, x) for x in range(-10, 11)]
        tree.add_line(0, -1000)  # 되돌린 뒤에도 정상적으로 삽입된다
        assert tree.query(0) == -1000


def test_min_over_time_matches_brute_force():
    rng = random.Random(3)
    for maximize in (False, True):
        for _ in range(150):
            lines = []
            for _ in range(rng.randint(0, 10)):
                start = rng.randint(0, 12)
                lines.append((rng.randint(-5, 5), rng.randint(-30, 30), start, rng.randint(start, 14)))
            queries = [(rng.randint(0, 14), rng.randint(-8, 8)) for _ in range(rng.randint(0, 12))]
            expected = []
            for t, x in queries:
                values = [m * x + b for m, b, start, end in lines if start <= t < end]
                expected.append((max(values) if maximize else min(values)) if values else None)
            assert solution.min_over_time(-10, 10, lines, queries, maximize) == expected, (lines, queries)


def test_min_over_time_edge_cases():
    assert solution.min_over_time(0, 10, [(1, 0, 0, 5)], []) == []
    assert solution.min_over_time(0, 10, [], [(0, 1)]) == [None]
    # 끝 시각 end 에는 이미 사라진다, 시작 시각 start 에는 이미 있다
    assert solution.min_over_time(0, 10, [(1, 0, 3, 6)], [(2, 4), (3, 4), (5, 4), (6, 4)]) == [None, 4, 4, None]
    assert solution.min_over_time(0, 10, [(1, 0, 3, 3)], [(3, 4)]) == [None]  # 빈 구간
    # 같은 시각의 질의는 서로 영향을 주지 않는다
    assert solution.min_over_time(0, 10, [(1, 0, 0, 9), (0, 2, 4, 9)], [(5, 4), (5, 1), (1, 1)]) == [2, 1, 1]


def test_invalid_input():
    with pytest.raises(ValueError):
        solution.LiChaoTree(3, 2)
    tree = solution.LiChaoTree(0, 5)
    with pytest.raises(ValueError, match="정의역"):
        tree.query(6)


def test_large_coordinates_do_not_need_compression():
    tree = solution.LiChaoTree(-10**9, 10**9)
    tree.add_segment(2, -5 * 10**8, -10**9, 0)
    tree.add_segment(-3, 7 * 10**8, -5 * 10**8, 10**9)
    tree.add_line(0, 10**10)
    assert tree.query(-10**9) == -2 * 10**9 - 5 * 10**8
    assert tree.query(0) == min(-5 * 10**8, 7 * 10**8)
    assert tree.query(10**9) == -3 * 10**9 + 7 * 10**8


def test_main_segment_add_get_min_format(monkeypatch, capsys):
    text = "2 8\n0 10 1 0\n5 8 -1 12\n1 7\n1 8\n0 6 9 0 3\n1 8\n1 11\n1 5\n1 9\n1 10\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    # 선분은 반열린: [0,10) 의 y=x 는 x ≤ 9, [5,8) 의 y=-x+12 는 5 ≤ x ≤ 7, 질의 사이에 추가한 [6,9) 의 y=3 은 6 ≤ x ≤ 8
    # x=7: min(7, 5) = 5, x=8: 8 (두 번째 선분은 x=8 을 덮지 않는다), 추가 뒤 x=8: 3, x=11: 덮는 선분 없음, x=5: min(5, 7) = 5, x=9: 9 (세 번째 선분은 x=9 를 덮지 않는다), x=10: 없음
    assert capsys.readouterr().out == "5\n8\n3\nINFINITY\n5\n9\nINFINITY\n"
