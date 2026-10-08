"""solution.py 검증: 경계 상자를 반평면으로 차례로 자르는 순진한 방법(서덜랜드-호지먼 클리핑)과 무작위 반평면·다각형으로 비교"""
import io
import itertools
import random
import time
from fractions import Fraction

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
HalfPlane = solution.HalfPlane
BOUND = 100


def clip(polygon, plane):
    """볼록 다각형을 반평면의 안쪽으로 자른다 (경계 포함)."""
    result = []
    for i, current in enumerate(polygon):
        nxt = polygon[(i + 1) % len(polygon)]
        s_cur, s_nxt = plane.side(current), plane.side(nxt)
        if s_cur >= 0:
            result.append(current)
        if (s_cur > 0 and s_nxt < 0) or (s_cur < 0 and s_nxt > 0):
            t = Fraction(s_cur, 1) / (s_cur - s_nxt)
            result.append((current[0] + t * (nxt[0] - current[0]), current[1] + t * (nxt[1] - current[1])))
    return result


def normalize(polygon):
    """연속된 중복점과 일직선 위의 점을 없애고 가장 작은 점부터 시작하도록 회전."""
    points = []
    for p in polygon:
        p = (Fraction(p[0]), Fraction(p[1]))
        if not points or points[-1] != p:
            points.append(p)
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    changed = True
    while changed and len(points) >= 3:
        changed = False
        for i in range(len(points)):
            a, b, c = points[i - 1], points[i], points[(i + 1) % len(points)]
            if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) == 0:
                points.pop(i)
                changed = True
                break
    if not points:
        return []
    start = points.index(min(points))
    return points[start:] + points[:start]


def reference(planes, bound=BOUND):
    polygon = [(-bound, -bound), (bound, -bound), (bound, bound), (-bound, bound)]
    for plane in planes:
        polygon = clip(polygon, plane)
        if not polygon:
            return []
    polygon = normalize(polygon)
    return polygon if len(polygon) >= 3 and solution.polygon_area(polygon) > 0 else []


def random_plane(rng, spread=5):
    a = (rng.randint(-spread, spread), rng.randint(-spread, spread))
    while True:
        d = (rng.randint(-spread, spread), rng.randint(-spread, spread))
        if d != (0, 0):
            return HalfPlane(a[0], a[1], d[0], d[1])


def test_random_planes_match_clipping():
    rng = random.Random(0)
    for _ in range(1500):
        planes = [random_plane(rng) for _ in range(rng.randint(1, 7))]
        got = normalize(solution.half_plane_intersection(planes, BOUND))
        assert got == reference(planes), [(p.px, p.py, p.dx, p.dy) for p in planes]


def test_nonempty_results_satisfy_every_plane_and_are_convex_counter_clockwise():
    rng = random.Random(1)
    nonempty = 0
    for _ in range(600):
        planes = [random_plane(rng, 8) for _ in range(rng.randint(3, 12))]
        polygon = solution.half_plane_intersection(planes, BOUND)
        if not polygon:
            continue
        nonempty += 1
        assert solution.polygon_area(polygon) > 0
        for plane in planes:
            assert all(plane.contains(v) for v in polygon)
        n = len(polygon)
        for i in range(n):
            a, b, c = polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n]
            assert (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) > 0  # 왼쪽으로만 꺾인다 (엄격한 볼록)
    assert nonempty > 50  # 비어 있지 않은 경우를 충분히 시험했다


def test_simple_shapes():
    square = [HalfPlane(0, 0, 1, 0), HalfPlane(4, 0, 0, 1), HalfPlane(4, 4, -1, 0), HalfPlane(0, 4, 0, -1)]
    polygon = solution.half_plane_intersection(square)
    assert normalize(polygon) == [(0, 0), (4, 0), (4, 4), (0, 4)] and solution.polygon_area(polygon) == 16
    assert solution.half_plane_intersection(list(reversed(square))) and normalize(solution.half_plane_intersection(list(reversed(square)))) == normalize(polygon)  # 입력 순서와 무관
    triangle = [HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(0, -1, 0), HalfPlane.from_inequality(1, 1, 4)]  # x ≥ 0, y ≥ 0, x + y ≤ 4
    assert normalize(solution.half_plane_intersection(triangle)) == [(0, 0), (4, 0), (0, 4)] and solution.polygon_area(solution.half_plane_intersection(triangle)) == 8
    assert solution.half_plane_intersection([]) != [] and solution.polygon_area(solution.half_plane_intersection([], 10)) == 400  # 아무 제약이 없으면 경계 상자 전체


def test_degenerate_and_empty_cases():
    below = HalfPlane.from_inequality(0, 1, 0)  # y ≤ 0
    above = HalfPlane.from_inequality(0, -1, 0)  # y ≥ 0
    assert solution.half_plane_intersection([below, above]) == []  # 선분 (넓이 0)
    assert solution.half_plane_intersection([HalfPlane.from_inequality(0, 1, 0), HalfPlane.from_inequality(0, -1, -1)]) == []  # y ≤ 0 이고 y ≥ 1: 빈 집합
    point = [HalfPlane.from_inequality(1, 0, 0), HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(0, 1, 0), HalfPlane.from_inequality(0, -1, 0)]
    assert solution.half_plane_intersection(point) == []  # 한 점
    redundant = [HalfPlane(0, 0, 1, 0), HalfPlane(0, 0, 3, 0), HalfPlane(0, -5, 1, 0), HalfPlane(4, 0, 0, 1), HalfPlane(4, 4, -1, 0), HalfPlane(0, 4, 0, -1)]
    assert solution.polygon_area(solution.half_plane_intersection(redundant)) == 16  # 같은 방향의 겹치는 반평면, 바깥쪽 제약은 무시된다
    with pytest.raises(ValueError):
        HalfPlane(0, 0, 0, 0)
    with pytest.raises(ValueError):
        HalfPlane.from_inequality(0, 0, 1)


def test_concurrent_lines_do_not_create_extra_vertices():
    # 세 직선이 한 점에서 만나면 가운데 직선은 변을 이루지 않는다
    planes = [HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(0, -1, 0), HalfPlane.from_inequality(1, 1, 2), HalfPlane.from_inequality(1, 0, 2), HalfPlane.from_inequality(0, 1, 2)]
    polygon = solution.half_plane_intersection(planes)
    assert normalize(polygon) == [(0, 0), (2, 0), (0, 2)] and len(polygon) == 3


def test_lines_through_a_common_point_leave_no_duplicate_vertex():
    # 바닥 변(각도 0°)과 두 대각선(45°, 315°) 이 한 점 (0, -10) 에서 만난다: 바닥 변은 그 점에서 한 점만 닿는 군더더기라 꼭짓점이 중복되면 안 된다
    planes = [HalfPlane(0, -10, 1, 1), HalfPlane(0, -10, 1, -1)]
    polygon = solution.half_plane_intersection(planes, 10)
    assert len(polygon) == 5 and sorted(polygon) == sorted([(0, -10), (10, 0), (10, 10), (-10, 10), (-10, 0)])
    assert solution.polygon_area(polygon) == 300
    # 같은 모양을 입력 순서와 상자 크기를 바꿔 다시: 위쪽 변(180°) 이 두 대각선 (135°, 225°) 의 교점에 닿는다
    planes = [HalfPlane(0, 10, -1, -1), HalfPlane(0, 10, -1, 1)]
    polygon = solution.half_plane_intersection(list(reversed(planes)), 10)
    assert len(polygon) == 5 and (0, 10) in polygon and solution.polygon_area(polygon) == 300
    # 네 직선이 원점을 지난다 (사분면을 가르는 십자 + 대각선): 영역은 쐐기 하나이고 원점은 꼭짓점 하나
    cross = [HalfPlane(0, 0, 1, 0), HalfPlane(0, 0, 0, 1), HalfPlane(0, 0, 1, 1), HalfPlane(0, 0, -1, 1)]  # y ≥ 0, x ≤ 0, y ≤ -x: 원점이 꼭짓점인 쐐기 (y ≥ x 는 군더더기)
    polygon = solution.half_plane_intersection(cross, 10)
    assert polygon and polygon.count((0, 0)) == 1


def test_unbounded_regions_are_cut_by_the_box():
    assert solution.polygon_area(solution.half_plane_intersection([HalfPlane.from_inequality(0, 1, 0)], 10)) == 20 * 10  # y ≤ 0 인 반평면
    wedge = [HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(0, -1, 0)]
    assert solution.polygon_area(solution.half_plane_intersection(wedge, 10)) == 100  # 제1사분면


def test_from_inequality_matches_the_inequality():
    rng = random.Random(2)
    for _ in range(300):
        a, b = rng.randint(-6, 6), rng.randint(-6, 6)
        if a == 0 and b == 0:
            continue
        c = rng.randint(-20, 20)
        plane = HalfPlane.from_inequality(a, b, c)
        for _ in range(10):
            x, y = Fraction(rng.randint(-30, 30), rng.randint(1, 4)), Fraction(rng.randint(-30, 30), rng.randint(1, 4))
            assert plane.contains((x, y)) == (a * x + b * y <= c)


def test_polygon_kernel():
    # 별 모양(화살촉) 다각형: 볼록 꼭짓점들과 오목 꼭짓점 하나 → 핵은 오목 꼭짓점 근처의 작은 영역
    arrow = [(0, 0), (4, 2), (0, 4), (1, 2)]  # 반시계
    kernel = solution.polygon_kernel(arrow)
    assert kernel
    for edge_start, edge_end in zip(arrow, arrow[1:] + arrow[:1]):
        plane = HalfPlane.from_points(edge_start, edge_end)
        assert all(plane.contains(v) for v in kernel)
    convex = [(0, 0), (4, 0), (4, 4), (0, 4)]
    assert normalize(solution.polygon_kernel(convex)) == convex  # 볼록 다각형의 핵은 자기 자신
    # 핵 안의 점에서는 모든 꼭짓점이 보인다: 핵의 넓이가 양수이면 오목 꼭짓점 (1, 2) 이 핵의 꼭짓점이다
    assert (Fraction(1), Fraction(2)) in kernel
    not_star = [(0, 0), (6, 0), (6, 6), (5, 6), (5, 1), (1, 1), (1, 6), (0, 6)]  # 'U' 자 모양: 핵이 없다
    assert solution.polygon_kernel(not_star) == []


def test_convex_polygon_intersection_matches_clipping():
    rng = random.Random(3)

    def random_convex(rng):
        while True:
            points = [(rng.randint(-8, 8), rng.randint(-8, 8)) for _ in range(rng.randint(3, 7))]
            hull = []
            for p in sorted(set(points)):
                while len(hull) >= 2 and (hull[-1][0] - hull[-2][0]) * (p[1] - hull[-1][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-1][0]) <= 0:
                    hull.pop()
                hull.append(p)
            lower = hull
            hull = []
            for p in reversed(sorted(set(points))):
                while len(hull) >= 2 and (hull[-1][0] - hull[-2][0]) * (p[1] - hull[-1][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-1][0]) <= 0:
                    hull.pop()
                hull.append(p)
            polygon = lower[:-1] + hull[:-1]
            if len(polygon) >= 3:
                return polygon

    for _ in range(300):
        first, second = random_convex(rng), random_convex(rng)
        planes = [HalfPlane.from_points(poly[i], poly[(i + 1) % len(poly)]) for poly in (first, second) for i in range(len(poly))]
        assert normalize(solution.convex_polygon_intersection(first, second, BOUND)) == reference(planes), (first, second)


def test_linear_program_2d():
    # 최대화 x + y subject to x ≥ 0, y ≥ 0, x + 2y ≤ 8, 3x + y ≤ 9 → 꼭짓점 (2, 3) 에서 5
    planes = [HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(0, -1, 0), HalfPlane.from_inequality(1, 2, 8), HalfPlane.from_inequality(3, 1, 9)]
    assert solution.linear_program_2d(planes, (1, 1)) == (5, (2, 3))
    assert solution.linear_program_2d(planes, (-1, -1)) == (0, (0, 0))
    assert solution.linear_program_2d(planes + [HalfPlane.from_inequality(1, 0, -1)], (1, 1)) is None  # x ≤ -1 이 더해지면 불가능
    with pytest.raises(ValueError, match="유계"):
        solution.linear_program_2d([HalfPlane.from_inequality(-1, 0, 0)], (1, 0), bound=1000)
    strip = [HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(0, -1, 0), HalfPlane.from_inequality(0, 1, 3)]  # x ≥ 0, 0 ≤ y ≤ 3: x 방향으로만 유계가 아니다
    with pytest.raises(ValueError, match="유계"):
        solution.linear_program_2d(strip, (1, 0), bound=1000)  # 최적점 (1000, 0) 은 좌표 하나만 경계 위
    assert solution.linear_program_2d(strip, (0, 1), bound=1000) == (3, (0, 3))  # 최적 집합이 무한히 뻗은 변 y = 3: 상자 밖 진짜 꼭짓점 (0, 3)
    upright = [HalfPlane.from_inequality(-1, 0, 0), HalfPlane.from_inequality(1, 0, 3), HalfPlane.from_inequality(0, -1, 0)]  # 0 ≤ x ≤ 3, y ≥ 0
    with pytest.raises(ValueError, match="유계"):
        solution.linear_program_2d(upright, (0, 1), bound=1000)  # 최적점 (0, 1000), (3, 1000): y 좌표만 경계 위
    rng = random.Random(4)
    for _ in range(200):  # 모든 꼭짓점의 값 중 최대: 클리핑으로 구한 꼭짓점과 비교
        planes = [random_plane(rng) for _ in range(rng.randint(2, 6))]
        objective = (rng.randint(-5, 5), rng.randint(-5, 5))
        ref = reference(planes, 100)
        try:
            result = solution.linear_program_2d(planes, objective, 100)
        except ValueError:
            assert any(abs(v[0]) == 100 or abs(v[1]) == 100 for v in ref)
            continue
        if not ref:
            assert result is None
        else:
            assert result[0] == max(objective[0] * x + objective[1] * y for x, y in ref)


def test_main_area_format(monkeypatch, capsys):
    text = "4\n0 0 4 0\n4 0 4 4\n4 4 0 4\n0 4 0 0\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    solution.main()
    assert capsys.readouterr().out == "16\n"
    text = "3\n0 0 3 0\n3 0 0 1\n0 1 0 0\n"  # 삼각형 (0,0), (3,0), (0,1): 넓이 3/2
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    solution.main()
    assert capsys.readouterr().out == "3/2\n"


def test_large_input_is_fast():
    rng = random.Random(5)
    n = 3000
    planes = []
    for i in range(n):  # 원점을 안쪽에 두는 무작위 반평면 n 개 (모두 c = 10^6 > 0)
        angle_x, angle_y = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
        if (angle_x, angle_y) != (0, 0):
            planes.append(HalfPlane.from_inequality(angle_x, angle_y, 10**6))
    started = time.perf_counter()
    polygon = solution.half_plane_intersection(planes, 10**9)
    assert time.perf_counter() - started < 30
    assert len(polygon) >= 3 and all(plane.contains(v) for plane in planes for v in polygon[:50])
