"""solution.py 검증: 정의("다른 점들의 볼록 결합이 아닌 점") 대로 모든 점을 따져 본 완전탐색, 가장 먼 쌍은 모든 쌍을 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p, a, b):
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def in_triangle(p, a, b, c):
    if cross(a, b, c) == 0:
        return on_segment(p, a, b) or on_segment(p, b, c) or on_segment(p, a, c)
    signs = [cross(a, b, p), cross(b, c, p), cross(c, a, p)]
    return all(s >= 0 for s in signs) or all(s <= 0 for s in signs)


def brute_force_vertices(points):
    """다른 서로 다른 점 세 개로 이루어진(퇴화 포함) 삼각형 안에 들어가지 않는 점 = 껍질의 꼭짓점."""
    unique = sorted(set(points))
    vertices = set()
    for p in unique:
        others = [q for q in unique if q != p]
        covered = any(in_triangle(p, a, b, c) for a, b, c in itertools.combinations(others, 3)) or any(
            on_segment(p, a, b) for a, b in itertools.combinations(others, 2)
        )
        if not covered:
            vertices.add(p)
    return vertices


def random_points(rng, n, bound):
    return [(rng.randint(-bound, bound), rng.randint(-bound, bound)) for _ in range(n)]


def test_hull_vertices_match_definition_and_form_a_ccw_convex_polygon():
    rng = random.Random(0)
    for _ in range(700):
        points = random_points(rng, rng.randint(1, 9), rng.choice([2, 3, 5]))
        hull = solution.convex_hull(points)
        expected = brute_force_vertices(points)
        assert set(hull) == expected and len(hull) == len(set(hull)), (points, hull)
        if len(hull) >= 3:
            assert hull[0] == min(hull)  # 가장 왼쪽(같으면 아래) 점에서 시작
            n = len(hull)
            assert all(solution.cross(hull[i], hull[(i + 1) % n], hull[(i + 2) % n]) > 0 for i in range(n))  # 반시계, 일직선 없음
            assert all(solution.cross(hull[i], hull[(i + 1) % n], p) >= 0 for i in range(n) for p in points)  # 모든 점이 안쪽


def test_keep_collinear_returns_every_boundary_point_in_order():
    rng = random.Random(1)
    for _ in range(500):
        points = random_points(rng, rng.randint(1, 10), rng.choice([2, 3]))
        strict = solution.convex_hull(points)
        full = solution.convex_hull(points, keep_collinear=True)
        unique = set(points)
        if len(strict) >= 3:
            n = len(strict)
            boundary = {p for p in unique if any(on_segment(p, strict[i], strict[(i + 1) % n]) for i in range(n))}
            assert set(full) == boundary and len(full) == len(boundary), (points, full)
            m = len(full)
            assert all(solution.cross(full[i], full[(i + 1) % m], full[(i + 2) % m]) >= 0 for i in range(m))
            assert solution.polygon_area2(full) == solution.polygon_area2(strict)
            assert set(strict) <= set(full)
        else:
            assert full == sorted(unique) if len(strict) == 2 else full == strict


def test_degenerate_inputs():
    assert solution.convex_hull([]) == []
    assert solution.convex_hull([(3, 4)]) == [(3, 4)]
    assert solution.convex_hull([(3, 4), (3, 4), (3, 4)]) == [(3, 4)]
    assert solution.convex_hull([(0, 0), (2, 2), (1, 1), (3, 3)]) == [(0, 0), (3, 3)]  # 모두 일직선: 양 끝
    assert solution.convex_hull([(0, 0), (2, 2), (1, 1), (3, 3)], keep_collinear=True) == [(0, 0), (1, 1), (2, 2), (3, 3)]
    assert solution.convex_hull([(0, 0), (0, 5), (0, 2)]) == [(0, 0), (0, 5)]
    assert solution.convex_hull([(5, 1), (1, 1)]) == [(1, 1), (5, 1)]


def test_known_shapes():
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    inner = square + [(1, 1), (1, 0), (2, 1), (0, 0), (1, 2)]
    assert solution.convex_hull(inner) == square
    assert solution.convex_hull(inner, keep_collinear=True) == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)]
    assert solution.convex_hull(inner + [(0, 1)], keep_collinear=True) == [
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)
    ]  # 왼쪽 변 위의 점은 반시계 방향으로 마지막에 나온다
    assert solution.polygon_area2(square) == 8
    assert abs(solution.hull_perimeter(square) - 8.0) < 1e-12 and solution.hull_perimeter([(1, 1)]) == 0.0
    triangle = [(0, 0), (4, 0), (0, 3)]
    assert abs(solution.hull_perimeter(triangle) - 12.0) < 1e-12  # 3-4-5 삼각형


def test_rotating_calipers_matches_all_pairs():
    rng = random.Random(2)
    for _ in range(700):
        points = random_points(rng, rng.randint(1, 12), rng.choice([2, 4, 8]))
        distance, p, q = solution.rotating_calipers_diameter(points)
        expected = max(solution.squared_distance(a, b) for a in points for b in points)
        assert distance == expected, points
        assert p in points and q in points and solution.squared_distance(p, q) == distance


def test_large_inputs():
    rng = random.Random(3)
    points = random_points(rng, 100_000, 10**6)
    hull = solution.convex_hull(points)
    assert 3 <= len(hull) < 200  # 균일하게 흩뿌린 점의 껍질은 아주 작다
    assert all(solution.cross(hull[i], hull[(i + 1) % len(hull)], hull[(i + 2) % len(hull)]) > 0 for i in range(len(hull)))
    parabola = [(i, i * i) for i in range(20_000)]
    assert len(solution.convex_hull(parabola)) == 20_000  # 포물선 위의 점은 모두 껍질의 꼭짓점이다
    distance, _, _ = solution.rotating_calipers_diameter(points[:3000])
    assert distance == max(solution.squared_distance(a, b) for a in solution.convex_hull(points[:3000]) for b in solution.convex_hull(points[:3000]))


def test_main(monkeypatch, capsys):
    text = "6\n0 0\n2 0\n2 2\n0 2\n1 1\n1 0\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
