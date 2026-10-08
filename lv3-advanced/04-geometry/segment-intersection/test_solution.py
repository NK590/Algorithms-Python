"""solution.py 검증: 방향 판정과는 다른 방식(매개변수 방정식을 분수로 정확하게 푸는 방법)으로 만든 기준 구현과 비교"""
import io
import random
from fractions import Fraction

from tools.loader import load_solution

solution = load_solution(__file__)


def sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def cross2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def on_segment_param(p, c, d):
    s = sub(d, c)
    w = sub(p, c)
    return cross2(w, s) == 0 and 0 <= dot(w, s) <= dot(s, s)


def reference_intersect(a, b, c, d):
    """a + t·r = c + u·s (0 ≤ t, u ≤ 1) 의 해가 있는가. 퇴화(점)와 평행한 경우를 따로 다룬다."""
    r, s = sub(b, a), sub(d, c)
    if r == (0, 0) and s == (0, 0):
        return a == c
    if r == (0, 0):
        return on_segment_param(a, c, d)
    if s == (0, 0):
        return on_segment_param(c, a, b)
    denominator = cross2(r, s)
    if denominator != 0:
        t = Fraction(cross2(sub(c, a), s), denominator)
        u = Fraction(cross2(sub(c, a), r), denominator)
        return 0 <= t <= 1 and 0 <= u <= 1
    if cross2(sub(c, a), r) != 0:
        return False  # 평행하지만 다른 직선
    tc = Fraction(dot(sub(c, a), r), dot(r, r))
    td = Fraction(dot(sub(d, a), r), dot(r, r))
    return min(tc, td) <= 1 and max(tc, td) >= 0


def random_point(rng, bound):
    return rng.randint(-bound, bound), rng.randint(-bound, bound)


def test_intersect_matches_reference_on_small_grid_including_degenerate_cases():
    rng = random.Random(0)
    hits = misses = 0
    for _ in range(20000):
        a, b, c, d = (random_point(rng, 3) for _ in range(4))
        expected = reference_intersect(a, b, c, d)
        assert solution.segments_intersect(a, b, c, d) == expected, (a, b, c, d)
        assert solution.segments_intersect(c, d, a, b) == expected  # 순서 바꿔도 같다
        assert solution.segments_intersect(b, a, d, c) == expected  # 끝점 방향을 바꿔도 같다
        hits += expected
        misses += not expected
    assert hits > 3000 and misses > 3000


def test_exhaustive_check_on_a_tiny_grid():
    points = [(x, y) for x in range(3) for y in range(2)]
    for a in points:
        for b in points:
            for c in points:
                for d in points:
                    assert solution.segments_intersect(a, b, c, d) == reference_intersect(a, b, c, d), (a, b, c, d)


def test_known_cases():
    assert solution.segments_intersect((0, 0), (2, 2), (0, 2), (2, 0))  # X 자
    assert solution.segments_intersect((0, 0), (2, 0), (2, 0), (3, 5))  # 끝점끼리 닿음
    assert solution.segments_intersect((0, 0), (4, 0), (2, 0), (2, 3))  # T 자: 한 끝점이 다른 선분 위
    assert solution.segments_intersect((0, 0), (4, 0), (2, 0), (6, 0))  # 일직선 위에서 겹침
    assert solution.segments_intersect((0, 0), (4, 0), (4, 0), (6, 0))  # 일직선 위에서 끝점만 닿음
    assert not solution.segments_intersect((0, 0), (4, 0), (5, 0), (6, 0))  # 일직선이지만 떨어져 있음
    assert not solution.segments_intersect((0, 0), (4, 0), (0, 1), (4, 1))  # 평행
    assert not solution.segments_intersect((0, 0), (1, 1), (2, 0), (3, 5))  # 직선은 만나지만 선분은 안 만남
    assert solution.segments_intersect((1, 1), (1, 1), (0, 0), (2, 2))  # 점이 선분 위
    assert not solution.segments_intersect((1, 2), (1, 2), (0, 0), (2, 2))


def test_properly_intersect_excludes_touching():
    assert solution.segments_properly_intersect((0, 0), (2, 2), (0, 2), (2, 0))
    assert not solution.segments_properly_intersect((0, 0), (2, 0), (2, 0), (3, 5))
    assert not solution.segments_properly_intersect((0, 0), (4, 0), (2, 0), (2, 3))
    assert not solution.segments_properly_intersect((0, 0), (4, 0), (2, 0), (6, 0))


def test_intersection_point_is_exact_and_lies_on_both_segments():
    rng = random.Random(1)
    kinds = {"point": 0, "segment": 0, None: 0}
    cases = [tuple(random_point(rng, 4) for _ in range(4)) for _ in range(10000)]
    for _ in range(4000):  # 한 직선 위에 놓인 선분들 (겹치는 구간이 나오는 경우를 충분히 만든다)
        dx, dy = rng.choice([(1, 0), (0, 1), (1, 1), (2, -1)])
        bx, by = random_point(rng, 3)
        cases.append(tuple((bx + k * dx, by + k * dy) for k in (rng.randint(-4, 4) for _ in range(4))))
    for a, b, c, d in cases:
        result = solution.intersection(a, b, c, d)
        expected = reference_intersect(a, b, c, d)
        assert (result is not None) == expected, (a, b, c, d)
        if result is None:
            kinds[None] += 1
            continue
        kind, value = result
        kinds[kind] += 1
        points = [value] if kind == "point" else list(value)
        for x, y in points:
            for p, q in ((a, b), (c, d)):
                w = (x - p[0], y - p[1])
                s = sub(q, p)
                if s == (0, 0):
                    assert (x, y) == p
                else:
                    assert cross2(w, s) == 0 and 0 <= dot(w, s) <= dot(s, s), (a, b, c, d, result)
        if kind == "segment":
            assert value[0] < value[1]
    assert kinds["point"] > 1000 and kinds["segment"] > 300 and kinds[None] > 1000


def test_intersection_examples():
    assert solution.intersection((0, 0), (2, 2), (0, 2), (2, 0)) == ("point", (Fraction(1), Fraction(1)))
    assert solution.intersection((0, 0), (3, 0), (1, 5), (2, -5)) == ("point", (Fraction(3, 2), Fraction(0)))
    assert solution.intersection((0, 0), (1, 3), (0, 1), (3, 0)) == ("point", (Fraction(3, 10), Fraction(9, 10)))  # 정수가 아닌 교점
    assert solution.intersection((0, 0), (4, 0), (2, 0), (6, 0)) == ("segment", ((2, 0), (4, 0)))
    assert solution.intersection((4, 0), (0, 0), (6, 0), (2, 0)) == ("segment", ((2, 0), (4, 0)))  # 방향이 달라도 같다
    assert solution.intersection((0, 0), (4, 0), (4, 0), (6, 0)) == ("point", (Fraction(4), Fraction(0)))
    assert solution.intersection((0, 0), (4, 0), (5, 0), (6, 0)) is None
    assert solution.intersection((1, 1), (1, 1), (0, 0), (2, 2)) == ("point", (Fraction(1), Fraction(1)))


def test_segment_groups_match_brute_force_components():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(0, 9)
        segments = [(random_point(rng, 5), random_point(rng, 5)) for _ in range(n)]
        # 기준: 반복해서 합치는 단순한 방법
        groups = [{i} for i in range(n)]
        merged = True
        while merged:
            merged = False
            for x in range(len(groups)):
                for y in range(x + 1, len(groups)):
                    if any(reference_intersect(*segments[i], *segments[j]) for i in groups[x] for j in groups[y]):
                        groups[x] |= groups[y]
                        del groups[y]
                        merged = True
                        break
                if merged:
                    break
        expected = (len(groups), max((len(g) for g in groups), default=0))
        assert solution.segment_groups(segments) == expected, segments
    assert solution.segment_groups([]) == (0, 0)
    assert solution.segment_groups([((0, 0), (1, 1)), ((1, 1), (2, 0)), ((5, 5), (6, 6))]) == (2, 2)


def test_main(monkeypatch, capsys):
    for text, expected in [("1 1 5 5\n1 5 5 1\n", "1"), ("1 1 5 5\n6 6 7 7\n", "0"), ("0 0 4 0\n4 0 8 0\n", "1"), ("0 0 4 0\n2 1 2 -1\n", "1"), ("0 0 4 0\n1 3 1 1\n", "0")]:
        monkeypatch.setattr("sys.stdin", io.StringIO(text))
        solution.main()
        assert capsys.readouterr().out.strip() == expected
