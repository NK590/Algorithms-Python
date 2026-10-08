"""선분 교차 — 두 선분이 만나는지 판정하고, 만나는 점(또는 겹치는 구간)을 정확하게 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 판정: 선분 ab 와 cd 에 대해 ccw(a, b, c) 와 ccw(a, b, d) 가 서로 다른 쪽이고(또는 0) ccw(c, d, a) 와 ccw(c, d, b) 도 서로 다른 쪽이면 교차한다.
  네 점이 모두 일직선이면 위 식이 항상 0 이라 "두 선분의 x 범위와 y 범위가 겹치는가" 를 따로 확인한다. 끝점이 닿거나 한 끝점이 다른 선분 위에 있는 경우도 교차로 본다.
- 교점: 두 직선의 교점을 분수(Fraction)로 정확하게 계산합니다 (좌표가 정수라도 교점은 정수가 아닐 수 있음).
  평행하게 겹치면 겹치는 구간의 양 끝점을 돌려줍니다.
- segment_groups: 서로 닿는 선분끼리 합집합 찾기(Union-Find)로 묶어 그룹의 수와 가장 큰 그룹의 크기를 구합니다 (O(n²)).
- 점은 (x, y) 정수 튜플. 길이가 0 인 선분(점)도 올바르게 처리합니다.
- 직접 실행하면 두 선분 `x1 y1 x2 y2` 두 줄을 받아 교차하면 1, 아니면 0 을 출력합니다.
"""
import sys
from fractions import Fraction

Point = tuple[int, int]
Segment = tuple[Point, Point]


def cross(o: Point, a: Point, b: Point) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """닫힌 선분 ab 와 cd 가 한 점이라도 공유하는가 (끝점이 닿는 경우, 겹치는 경우 포함)."""
    d1 = sign(cross(a, b, c))
    d2 = sign(cross(a, b, d))
    d3 = sign(cross(c, d, a))
    d4 = sign(cross(c, d, b))
    if d1 == d2 == d3 == d4 == 0:  # 네 점이 일직선: 투영한 구간이 겹치는가
        return (
            max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
            and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))
        )
    return d1 * d2 <= 0 and d3 * d4 <= 0


def segments_properly_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """서로의 안쪽 점에서 엇갈려 만나는가 (끝점이 닿거나 겹치는 경우는 제외)."""
    return (
        sign(cross(a, b, c)) * sign(cross(a, b, d)) < 0
        and sign(cross(c, d, a)) * sign(cross(c, d, b)) < 0
    )


def intersection(a: Point, b: Point, c: Point, d: Point):
    """교점 계산. 만나지 않으면 None, 한 점에서 만나면 ("point", (x, y)) (좌표는 Fraction), 겹치는 구간이 있으면 ("segment", (p, q)) (p <= q, 사전순)."""
    if not segments_intersect(a, b, c, d):
        return None
    r = (b[0] - a[0], b[1] - a[1])
    s = (d[0] - c[0], d[1] - c[1])
    denominator = r[0] * s[1] - r[1] * s[0]  # r × s
    if denominator != 0:  # 평행하지 않다: a + t·r = c + u·s 를 풀면 t = (c - a) × s / (r × s)
        t = Fraction((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0], denominator)
        return "point", (a[0] + t * r[0], a[1] + t * r[1])
    # 평행하고 만난다 → 일직선 위. 겹치는 구간은 사전순으로 가장 큰 시작점과 가장 작은 끝점
    first = sorted([a, b])
    second = sorted([c, d])
    low = max(first[0], second[0])
    high = min(first[1], second[1])
    if low == high:
        return "point", (Fraction(low[0]), Fraction(low[1]))
    return "segment", (low, high)


def segment_groups(segments: list[Segment]) -> tuple[int, int]:
    """서로 닿는 선분(간접적으로 닿아도 같은 그룹)의 (그룹 수, 가장 큰 그룹의 선분 수). O(n²)."""
    n = len(segments)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(i + 1, n):
            if segments_intersect(*segments[i], *segments[j]):
                parent[find(i)] = find(j)
    sizes: dict[int, int] = {}
    for i in range(n):
        root = find(i)
        sizes[root] = sizes.get(root, 0) + 1
    return len(sizes), max(sizes.values(), default=0)


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    a, b, c, d = (data[0], data[1]), (data[2], data[3]), (data[4], data[5]), (data[6], data[7])
    print(1 if segments_intersect(a, b, c, d) else 0)


if __name__ == "__main__":
    main()
