"""반평면 교집합(Half-Plane Intersection) — 반평면 n 개의 교집합(볼록 다각형)을 각도 정렬 + 덱으로 O(n log n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 반평면: 방향이 있는 직선 (점 p, 방향 d) 의 **왼쪽**(경계 포함) {q : cross(d, q - p) ≥ 0}. 부등식 a·x + b·y ≤ c 는 from_inequality 로 바꾼다.
- 알고리즘: 방향의 각도 순으로 정렬 → 같은 방향은 더 안쪽(제약이 센) 것만 남김 → 덱에 하나씩 넣으면서
  ① 새 반평면이 덱 뒤쪽 두 직선의 교점을 (엄격하게) 밖으로 밀어내면 뒤에서 pop, ② 앞쪽 두 직선의 교점도 같은 방식으로 앞에서 pop → 새 직선을 뒤에 넣는다.
  마지막에 앞뒤를 서로 한 번 더 정리하면 덱에 남은 직선들이 교집합 볼록 다각형의 변을 이룬다 (각 직선이 이웃과 만나는 점이 꼭짓점).
- 교점은 분수(Fraction) 로 정확하게 계산한다. 각도 정렬도 외적으로 비교하는 정확한 방법이라 오차가 없다.
- 교집합이 비어 있거나 넓이가 0 (한 점 또는 선분) 이면 빈 리스트 (경계에 걸친 꼭짓점도 엄격하게 pop 하므로 넓이 0 인 결과는 정반대 방향의 평행선이 이웃하거나 3 개 미만의 직선만 남아 걸러진다). 유계가 아닌 교집합은 한 변이 ±bound 인 큰 정사각형으로 잘려 나온다 (bound 는 실제 꼭짓점의 좌표보다 충분히 크게).
- 응용: polygon_area, polygon_kernel(별 모양 다각형의 핵), linear_program_2d(변수 두 개의 선형 계획), convex_polygon_intersection(두 볼록 다각형의 교집합).
- 직접 실행하면 `N` 과 N 개의 선분(`x1 y1 x2 y2`)을 받아, 각 선분의 **왼쪽**을 허용하는 반평면 N 개의 교집합 넓이를 출력합니다 (정수 좌표이면 넓이의 2 배는 분수일 수 있어 `정수/분모` 형태로 출력).
"""
import sys
from fractions import Fraction
from functools import cmp_to_key
from typing import Optional, Sequence

Point = tuple


class HalfPlane:
    __slots__ = ("px", "py", "dx", "dy")

    def __init__(self, px, py, dx, dy):
        if dx == 0 and dy == 0:
            raise ValueError("방향 벡터가 영벡터입니다")
        self.px, self.py, self.dx, self.dy = px, py, dx, dy

    @classmethod
    def from_points(cls, a: Point, b: Point) -> "HalfPlane":
        """a → b 로 향하는 직선의 왼쪽."""
        return cls(a[0], a[1], b[0] - a[0], b[1] - a[1])

    @classmethod
    def from_inequality(cls, a, b, c) -> "HalfPlane":
        """a·x + b·y ≤ c. 안쪽 법선은 -(a, b) 이고 방향 d 의 왼쪽 법선은 (-dy, dx) 이므로 (-dy, dx) = -(a, b), 즉 d = (-b, a)."""
        if a == 0 and b == 0:
            raise ValueError("a 와 b 가 모두 0 입니다")
        px, py = (Fraction(c, a), 0) if a != 0 else (0, Fraction(c, b))
        return cls(px, py, -b, a)

    def side(self, point: Point):
        """> 0 이면 안쪽, 0 이면 경계 위, < 0 이면 바깥."""
        return self.dx * (point[1] - self.py) - self.dy * (point[0] - self.px)

    def contains(self, point: Point) -> bool:
        return self.side(point) >= 0


def _cross(ax, ay, bx, by):
    return ax * by - ay * bx


def _angle_compare(p: HalfPlane, q: HalfPlane) -> int:
    """방향 벡터의 각도(0 이상 2π 미만) 비교. 외적만 쓰는 정확한 비교."""
    half_p = 0 if (p.dy > 0 or (p.dy == 0 and p.dx > 0)) else 1
    half_q = 0 if (q.dy > 0 or (q.dy == 0 and q.dx > 0)) else 1
    if half_p != half_q:
        return -1 if half_p < half_q else 1
    c = _cross(p.dx, p.dy, q.dx, q.dy)
    return -1 if c > 0 else (1 if c < 0 else 0)


def _intersection(p: HalfPlane, q: HalfPlane) -> Point:
    denominator = _cross(q.dx, q.dy, p.dx, p.dy)
    t = Fraction(_cross(q.dx, q.dy, q.px - p.px, q.py - p.py), 1) / denominator
    return (p.px + t * p.dx, p.py + t * p.dy)


def half_plane_intersection(planes: Sequence[HalfPlane], bound: int = 10**9) -> list[Point]:
    """교집합 볼록 다각형의 꼭짓점 (반시계 방향, Fraction 좌표). 비었거나 넓이 0 이면 []."""
    corners = [(-bound, -bound), (bound, -bound), (bound, bound), (-bound, bound)]
    box = [HalfPlane.from_points(corners[i], corners[(i + 1) % 4]) for i in range(4)]
    ordered = sorted(list(planes) + box, key=cmp_to_key(_angle_compare))
    unique: list[HalfPlane] = []
    for plane in ordered:
        if unique and _angle_compare(unique[-1], plane) == 0:
            if unique[-1].side((plane.px, plane.py)) > 0:  # 새 직선이 더 안쪽이면 교체
                unique[-1] = plane
        else:
            unique.append(plane)
    lines: list[HalfPlane] = []  # 덱: lines[head:] 가 유효한 부분
    head = 0
    for plane in unique:
        while len(lines) - head >= 2 and plane.side(_intersection(lines[-2], lines[-1])) <= 0:
            lines.pop()
        while len(lines) - head >= 2 and plane.side(_intersection(lines[head], lines[head + 1])) <= 0:
            head += 1
        if len(lines) - head >= 1 and _cross(lines[-1].dx, lines[-1].dy, plane.dx, plane.dy) == 0:
            return []  # 정반대 방향의 평행선이 이웃이 됐다: 사이가 비었다
        lines.append(plane)
    while len(lines) - head >= 3 and lines[head].side(_intersection(lines[-2], lines[-1])) <= 0:
        lines.pop()
    while len(lines) - head >= 3 and lines[-1].side(_intersection(lines[head], lines[head + 1])) <= 0:
        head += 1
    window = lines[head:]
    if len(window) < 3:
        return []
    return [_intersection(window[i], window[(i + 1) % len(window)]) for i in range(len(window))]


def polygon_area(vertices: Sequence[Point]):
    """꼭짓점이 반시계 방향이면 양수인 넓이 (신발끈 공식)."""
    total = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        total += x1 * y2 - x2 * y1
    return Fraction(total, 2) if isinstance(total, int) else total / 2


def point_in_all(planes: Sequence[HalfPlane], point: Point) -> bool:
    return all(plane.contains(point) for plane in planes)


def polygon_kernel(vertices: Sequence[Point], bound: int = 10**9) -> list[Point]:
    """단순 다각형(반시계 방향 꼭짓점) 의 핵(kernel): 다각형 안의 모든 점이 보이는 점들의 집합 = 모든 변의 안쪽 반평면의 교집합."""
    count = len(vertices)
    return half_plane_intersection([HalfPlane.from_points(vertices[i], vertices[(i + 1) % count]) for i in range(count)], bound)


def convex_polygon_intersection(first: Sequence[Point], second: Sequence[Point], bound: int = 10**9) -> list[Point]:
    """반시계 방향의 두 볼록 다각형의 교집합."""
    planes = []
    for polygon in (first, second):
        count = len(polygon)
        planes.extend(HalfPlane.from_points(polygon[i], polygon[(i + 1) % count]) for i in range(count))
    return half_plane_intersection(planes, bound)


def linear_program_2d(planes: Sequence[HalfPlane], objective: tuple, bound: int = 10**9) -> Optional[tuple]:
    """제약 planes 아래에서 objective = (a, b) 로 a·x + b·y 를 최대화. (최댓값, 점) 또는 실행 가능 영역이 비면 None.
    최적 꼭짓점이 모두 인공 경계 상자(±bound) 위에 있으면 최댓값이 유계가 아니므로 ValueError (최적 집합이 무한히 뻗은 변이면 상자 밖 진짜 꼭짓점을 돌려준다)."""
    polygon = half_plane_intersection(planes, bound)
    if not polygon:
        return None
    best = max(objective[0] * x + objective[1] * y for x, y in polygon)
    for x, y in polygon:
        if objective[0] * x + objective[1] * y == best and abs(x) != bound and abs(y) != bound:
            return best, (x, y)
    raise ValueError("최적해가 유계가 아닙니다 (최댓값이 bound 에서 나옵니다)")


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    planes = []
    for i in range(n):
        x1, y1, x2, y2 = (int(v) for v in data[1 + 4 * i : 5 + 4 * i])
        planes.append(HalfPlane.from_points((x1, y1), (x2, y2)))
    area = polygon_area(half_plane_intersection(planes))
    print(f"{area.numerator}/{area.denominator}" if isinstance(area, Fraction) and area.denominator != 1 else int(area))


if __name__ == "__main__":
    main()
