"""CCW(Counter-ClockWise)와 외적 — 세 점이 왼쪽으로 도는지, 오른쪽으로 도는지, 일직선인지를 정수 연산만으로 판정하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 점 o 에서 a, b 로 가는 벡터의 외적 cross(o, a, b) = (a - o) × (b - o) = (ax - ox)(by - oy) - (ay - oy)(bx - ox).
  양수 ⟺ o -> a -> b 가 반시계(왼쪽으로 꺾임), 음수 ⟺ 시계(오른쪽), 0 ⟺ 한 직선 위. 절댓값은 세 점이 이루는 삼각형 넓이의 2 배.
- 좌표가 정수이면 외적도 정수라서 부동소수점 오차가 없습니다. 기하 문제의 대부분은 "외적의 부호" 하나로 풀립니다.
- 응용: 다각형 넓이(신발끈 공식), 볼록 다각형 판정, 점이 삼각형·다각형 안에 있는가, 한 점 둘레의 각도순 정렬.
- 점은 (x, y) 정수 튜플. 직접 실행하면 세 점 P1, P2, P3 을 받아 P1 -> P2 -> P3 이 반시계면 1, 시계면 -1, 일직선이면 0 을 출력합니다.
"""
import sys
from functools import cmp_to_key

Point = tuple[int, int]


def cross(o: Point, a: Point, b: Point) -> int:
    """(a - o) × (b - o). 양수면 o -> a -> b 가 반시계 방향."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def ccw(a: Point, b: Point, c: Point) -> int:
    """a -> b -> c 가 반시계(왼쪽으로 꺾임)면 1, 시계(오른쪽)면 -1, 일직선이면 0."""
    value = cross(a, b, c)
    return (value > 0) - (value < 0)


def triangle_area2(a: Point, b: Point, c: Point) -> int:
    """삼각형 넓이의 2 배 (정수로 유지하려고 2 배로 다룬다)."""
    return abs(cross(a, b, c))


def polygon_area2(points: list[Point]) -> int:
    """다각형 넓이의 2 배, 부호 있음: 점들이 반시계로 주어지면 양수, 시계면 음수. 신발끈 공식 Σ (xᵢ·yᵢ₊₁ - xᵢ₊₁·yᵢ)."""
    total = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        total += x1 * y2 - x2 * y1
    return total


def is_convex_polygon(points: list[Point], allow_collinear: bool = False) -> bool:
    """꼭짓점이 순서대로 주어진 다각형이 볼록인가. 모든 연속한 세 점이 같은 방향으로 꺾여야 한다 (allow_collinear 이면 일직선도 허용)."""
    n = len(points)
    direction = 0  # 점이 3 개 미만이거나 넓이가 없으면 방향이 정해지지 않아 False
    for i in range(n):
        turn = ccw(points[i], points[(i + 1) % n], points[(i + 2) % n])
        if turn == 0:
            if not allow_collinear:
                return False
            continue
        if direction == 0:
            direction = turn
        elif turn != direction:
            return False
    return direction != 0


def on_segment(p: Point, a: Point, b: Point) -> bool:
    """p 가 선분 ab 위(끝점 포함)에 있는가."""
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def point_in_triangle(p: Point, a: Point, b: Point, c: Point) -> bool:
    """p 가 삼각형 abc 안 또는 경계 위에 있는가 (abc 가 일직선인 퇴화된 경우는 선분 위인지)."""
    if cross(a, b, c) == 0:
        return on_segment(p, a, b) or on_segment(p, b, c) or on_segment(p, a, c)
    signs = {ccw(a, b, p), ccw(b, c, p), ccw(c, a, p)}
    return not (1 in signs and -1 in signs)  # 세 변에 대해 같은 쪽(또는 변 위)에 있다


def point_in_polygon(p: Point, polygon: list[Point]) -> str:
    """"inside", "boundary", "outside". 다각형은 볼록하지 않아도 된다. p 에서 오른쪽(+x)으로 쏜 반직선이 변과 만나는 횟수의 홀짝으로 판정."""
    inside = False
    n = len(polygon)
    for i in range(n):
        a, b = polygon[i], polygon[(i + 1) % n]
        if on_segment(p, a, b):
            return "boundary"
        if (a[1] > p[1]) != (b[1] > p[1]):  # 변이 p 의 높이를 가로지른다 (한쪽 끝점만 포함해서 꼭짓점을 두 번 세지 않는다)
            # 변과 p 를 지나는 수평선의 교점이 p 보다 오른쪽인가 ⟺ p 가 변의 (위로 향하는 방향 기준) 왼쪽
            if (b[1] > a[1]) == (cross(a, b, p) > 0):
                inside = not inside
    return "inside" if inside else "outside"


def sort_by_angle(points: list[Point], origin: Point = (0, 0)) -> list[Point]:
    """origin 을 기준으로 반시계 방향 각도순(+x 축 방향에서 시작, 0 이상 2π 미만). 각도가 같으면 가까운 점이 먼저. origin 과 같은 점은 맨 앞."""

    def half(p: Point) -> int:  # 위쪽 반평면(+x 축 포함)이 0, 아래쪽이 1
        dx, dy = p[0] - origin[0], p[1] - origin[1]
        return 0 if (dy > 0 or (dy == 0 and dx > 0)) else 1

    def compare(p: Point, q: Point) -> int:
        if p == origin or q == origin:
            return (q == origin) - (p == origin)
        hp, hq = half(p), half(q)
        if hp != hq:
            return hp - hq
        c = cross(origin, p, q)
        if c != 0:
            return -1 if c > 0 else 1
        dp = (p[0] - origin[0]) ** 2 + (p[1] - origin[1]) ** 2
        dq = (q[0] - origin[0]) ** 2 + (q[1] - origin[1]) ** 2
        return (dp > dq) - (dp < dq)

    return sorted(points, key=cmp_to_key(compare))


def main() -> None:
    data = sys.stdin.read().split()
    a = (int(data[0]), int(data[1]))
    b = (int(data[2]), int(data[3]))
    c = (int(data[4]), int(data[5]))
    print(ccw(a, b, c))


if __name__ == "__main__":
    main()
