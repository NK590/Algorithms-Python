"""solution.py 검증: 외적의 성질, 독립적인 계산(분수·각도), 알려진 도형의 값과 비교"""
import io
import math
import random
from fractions import Fraction

from tools.loader import load_solution

solution = load_solution(__file__)


def random_point(rng, bound=6):
    return rng.randint(-bound, bound), rng.randint(-bound, bound)


def test_ccw_signs_for_known_triples():
    assert solution.ccw((0, 0), (1, 0), (1, 1)) == 1  # 오른쪽으로 갔다가 위로: 반시계
    assert solution.ccw((0, 0), (1, 1), (1, 0)) == -1
    assert solution.ccw((0, 0), (1, 1), (2, 2)) == 0
    assert solution.ccw((1, 1), (5, 5), (7, 3)) == -1
    assert solution.ccw((5, 5), (5, 5), (3, 1)) == 0  # 같은 점이 있으면 0


def test_cross_properties():
    rng = random.Random(0)
    for _ in range(2000):
        a, b, c = random_point(rng), random_point(rng), random_point(rng)
        value = solution.cross(a, b, c)
        assert solution.cross(b, c, a) == value == solution.cross(c, a, b)  # 순환해도 같다
        assert solution.cross(a, c, b) == -value  # 두 점을 바꾸면 부호가 바뀐다
        shift = random_point(rng)
        moved = [(x + shift[0], y + shift[1]) for x, y in (a, b, c)]
        assert solution.cross(*moved) == value  # 평행 이동에 불변
        assert solution.cross((2 * a[0], 2 * a[1]), (2 * b[0], 2 * b[1]), (2 * c[0], 2 * c[1])) == 4 * value
        assert solution.ccw(a, b, c) == (value > 0) - (value < 0)
        assert solution.triangle_area2(a, b, c) == abs(value)


def test_ccw_matches_the_angle_between_vectors():
    rng = random.Random(1)
    for _ in range(2000):
        a, b, c = random_point(rng), random_point(rng), random_point(rng)
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (c[0] - a[0], c[1] - a[1])
        if v1 == (0, 0) or v2 == (0, 0):
            continue
        # 정수 좌표의 방향을 기약화해 같은 방향이 정확히 같은 실수 각도를 갖게 한다
        def normalized(v):
            g = math.gcd(abs(v[0]), abs(v[1]))
            return math.atan2(v[1] // g, v[0] // g)

        turn = (normalized(v2) - normalized(v1)) % (2 * math.pi)
        expected = 0 if turn == 0 or turn == math.pi else (1 if turn < math.pi else -1)
        assert solution.ccw(a, b, c) == expected, (a, b, c)


def test_polygon_area_shoelace():
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert solution.polygon_area2(square) == 8 and solution.polygon_area2(square[::-1]) == -8
    l_shape = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 3), (0, 3)]
    assert solution.polygon_area2(l_shape) == 2 * 6  # 4 + 2
    assert solution.polygon_area2([(0, 0), (4, 0), (0, 3)]) == 12
    assert solution.polygon_area2([(0, 0), (1, 1)]) == 0 and solution.polygon_area2([]) == 0


def star_shaped_polygon(rng, n):
    """원점을 둘러싸는 서로 다른 각도의 점들을 각도순으로 이은 단순 다각형(변이 교차하지 않음)."""
    while True:
        points = list({(rng.randint(-8, 8), rng.randint(-8, 8)) for _ in range(n)} - {(0, 0)})
        keys = {math.atan2(y // math.gcd(abs(x), abs(y)), x // math.gcd(abs(x), abs(y))) for x, y in points}
        if len(points) >= 3 and len(keys) == len(points):  # 각도가 모두 달라야 단순 다각형
            ordered = sorted(points, key=lambda p: math.atan2(p[1], p[0]))
            if solution.polygon_area2(ordered) > 0:
                return ordered


def test_area_equals_fan_triangulation_for_simple_polygons():
    rng = random.Random(2)
    for _ in range(300):
        polygon = star_shaped_polygon(rng, rng.randint(3, 9))
        origin_fan = sum(solution.cross((0, 0), polygon[i], polygon[(i + 1) % len(polygon)]) for i in range(len(polygon)))
        assert solution.polygon_area2(polygon) == origin_fan  # 원점에서 쏜 삼각형들의 합
        shifted = [(x + 5, y - 3) for x, y in polygon]
        assert solution.polygon_area2(shifted) == solution.polygon_area2(polygon)


def test_is_convex_polygon_matches_every_edge_has_all_points_on_one_side():
    rng = random.Random(3)
    convex_seen = concave_seen = 0
    for _ in range(600):
        polygon = star_shaped_polygon(rng, rng.randint(3, 8))
        n = len(polygon)
        expected = all(
            all(solution.cross(polygon[i], polygon[(i + 1) % n], p) >= 0 for p in polygon) for i in range(n)
        )
        strictly = all(
            all(solution.cross(polygon[i], polygon[(i + 1) % n], p) > 0 for j, p in enumerate(polygon) if j not in (i, (i + 1) % n))
            for i in range(n)
        )
        assert solution.is_convex_polygon(polygon, allow_collinear=True) == expected, polygon
        assert solution.is_convex_polygon(polygon) == strictly, polygon
        convex_seen += expected
        concave_seen += not expected
    assert convex_seen > 20 and concave_seen > 20
    assert not solution.is_convex_polygon([(0, 0), (1, 1)])
    assert not solution.is_convex_polygon([(0, 0), (1, 1), (2, 2)], allow_collinear=True)  # 넓이가 없는 퇴화


def test_on_segment_matches_parametric_definition():
    rng = random.Random(9)
    for _ in range(4000):
        a, b, p = random_point(rng, 4), random_point(rng, 4), random_point(rng, 4)
        direction = (b[0] - a[0], b[1] - a[1])
        offset = (p[0] - a[0], p[1] - a[1])
        if direction == (0, 0):
            expected = p == a
        else:
            collinear = direction[0] * offset[1] - direction[1] * offset[0] == 0
            along = direction[0] * offset[0] + direction[1] * offset[1]
            expected = collinear and 0 <= along <= direction[0] ** 2 + direction[1] ** 2
        assert solution.on_segment(p, a, b) == expected, (a, b, p)


def test_point_in_triangle_matches_barycentric_coordinates():
    rng = random.Random(4)
    for _ in range(3000):
        a, b, c, p = (random_point(rng, 4) for _ in range(4))
        area = solution.cross(a, b, c)
        if area == 0:
            expected = solution.on_segment(p, a, b) or solution.on_segment(p, b, c) or solution.on_segment(p, a, c)
        else:
            u = Fraction(solution.cross(p, b, c), area)
            v = Fraction(solution.cross(a, p, c), area)
            w = Fraction(solution.cross(a, b, p), area)
            expected = u >= 0 and v >= 0 and w >= 0
        assert solution.point_in_triangle(p, a, b, c) == expected, (a, b, c, p)


def winding_inside(p, polygon):
    """각도를 모두 더한 값이 ±2π 이면 안 (경계에서 멀리 떨어진 점에서만 신뢰)."""
    total = 0.0
    n = len(polygon)
    for i in range(n):
        a, b = polygon[i], polygon[(i + 1) % n]
        total += math.atan2(solution.cross(p, a, b), (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]))
    return abs(total) > math.pi


def test_point_in_polygon_matches_winding_number_and_detects_boundary():
    rng = random.Random(5)
    seen = {"inside": 0, "outside": 0, "boundary": 0}
    for _ in range(300):
        polygon = star_shaped_polygon(rng, rng.randint(3, 9))
        n = len(polygon)
        for _ in range(30):
            p = random_point(rng, 9)
            result = solution.point_in_polygon(p, polygon)
            seen[result] += 1
            on_boundary = any(solution.on_segment(p, polygon[i], polygon[(i + 1) % n]) for i in range(n))
            assert (result == "boundary") == on_boundary, (polygon, p)
            if not on_boundary:
                assert (result == "inside") == winding_inside(p, polygon), (polygon, p)
    assert all(count > 100 for count in seen.values())
    # 오목한 다각형 (ㄴ 모양): 오목하게 파인 곳은 바깥
    l_shape = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 3), (0, 3)]
    assert solution.point_in_polygon((2, 2), l_shape) == "outside" and solution.point_in_polygon((0, 2), l_shape) == "boundary"
    assert solution.point_in_polygon((2, 0), l_shape) == "boundary" and solution.point_in_polygon((0, 1), l_shape) == "boundary"
    assert solution.point_in_polygon((1, 1), l_shape) == "boundary" and solution.point_in_polygon((3, 0), l_shape) == "boundary"
    assert solution.point_in_polygon((3, 2), l_shape) == "outside" and solution.point_in_polygon((0, -1), l_shape) == "outside"


def test_sort_by_angle_matches_atan2_order():
    rng = random.Random(6)
    for _ in range(500):
        origin = random_point(rng, 3)
        points = [random_point(rng, 6) for _ in range(rng.randint(0, 12))]

        def key(p):
            dx, dy = p[0] - origin[0], p[1] - origin[1]
            if (dx, dy) == (0, 0):
                return (-1.0, 0)
            g = math.gcd(abs(dx), abs(dy))
            angle = math.atan2(dy // g, dx // g) % (2 * math.pi)
            return (angle, dx * dx + dy * dy)

        assert [key(p) for p in solution.sort_by_angle(points, origin)] == sorted(key(p) for p in points), (origin, points)
    assert solution.sort_by_angle([(0, -1), (-1, 0), (0, 1), (1, 0)]) == [(1, 0), (0, 1), (-1, 0), (0, -1)]


def test_main(monkeypatch, capsys):
    for text, expected in [("1 1\n5 5\n7 3\n", "-1"), ("0 0\n1 0\n1 1\n", "1"), ("0 0\n1 1\n3 3\n", "0")]:
        monkeypatch.setattr("sys.stdin", io.StringIO(text))
        solution.main()
        assert capsys.readouterr().out.strip() == expected
