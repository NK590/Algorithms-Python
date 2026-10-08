"""볼록 껍질(Convex Hull) — 점들을 모두 감싸는 가장 작은 볼록 다각형 구하기 (Andrew 의 단조 체인 알고리즘)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 점을 x(같으면 y) 순으로 정렬한 뒤, 왼쪽에서 오른쪽으로 훑으며 아래 껍질을, 오른쪽에서 왼쪽으로 훑으며 위 껍질을 만듭니다.
  새 점을 넣을 때 마지막 두 점과 새 점이 "왼쪽으로 꺾이지 않으면"(외적 ≤ 0) 마지막 점을 버립니다 (스택).
- 결과는 가장 왼쪽 아래 점에서 시작해 반시계 방향. 정렬이 지배적이라 O(n log n).
- 껍질의 변 위에 있는 점(일직선)은 기본적으로 뺍니다. keep_collinear=True 이면 변 위의 점도 포함합니다.
- 회전하는 캘리퍼스(rotating_calipers_diameter): 껍질의 가장 먼 두 점(지름)을 O(n) 에 찾습니다. 변을 따라 한 바퀴 돌며 대척점을 가리키는 포인터를 한 방향으로만 전진시킵니다.
- 점은 (x, y) 정수 튜플이고 외적은 정수라서 오차가 없습니다. 같은 점이 여러 번 들어와도 됩니다.
- 직접 실행하면 `N` 과 N 개의 점 `x y` 를 받아 볼록 껍질을 이루는 점의 수(변 위의 점 제외)를 출력합니다.
"""
import sys

Point = tuple[int, int]


def cross(o: Point, a: Point, b: Point) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[Point], keep_collinear: bool = False) -> list[Point]:
    """볼록 껍질의 꼭짓점을 반시계 방향으로, 가장 왼쪽 아래 점부터. 점이 하나뿐이면 그 점, 모두 일직선이면 양 끝 두 점 (keep_collinear 이면 정렬된 모든 점)."""
    unique = sorted(set(points))
    if len(unique) <= 1:
        return unique
    if all(cross(unique[0], unique[1], p) == 0 for p in unique):  # 모두 일직선
        return unique if keep_collinear else [unique[0], unique[-1]]

    def turns_wrong(o: Point, a: Point, b: Point) -> bool:
        c = cross(o, a, b)
        return c < 0 if keep_collinear else c <= 0  # 왼쪽으로 꺾이지 않으면 a 를 버린다

    lower: list[Point] = []
    for p in unique:
        while len(lower) >= 2 and turns_wrong(lower[-2], lower[-1], p):
            lower.pop()
        lower.append(p)
    upper: list[Point] = []
    for p in reversed(unique):
        while len(upper) >= 2 and turns_wrong(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]  # 각 껍질의 마지막 점은 다른 껍질의 첫 점과 같다


def polygon_area2(polygon: list[Point]) -> int:
    """다각형 넓이의 2 배 (반시계면 양수)."""
    return sum(
        polygon[i][0] * polygon[(i + 1) % len(polygon)][1] - polygon[(i + 1) % len(polygon)][0] * polygon[i][1]
        for i in range(len(polygon))
    )


def hull_perimeter(hull: list[Point]) -> float:
    """껍질의 둘레."""
    return sum(
        ((hull[i][0] - hull[(i + 1) % len(hull)][0]) ** 2 + (hull[i][1] - hull[(i + 1) % len(hull)][1]) ** 2) ** 0.5
        for i in range(len(hull))
    )


def squared_distance(a: Point, b: Point) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def rotating_calipers_diameter(points: list[Point]) -> tuple[int, Point, Point]:
    """가장 먼 두 점 사이 거리의 제곱과 그 두 점 (점이 하나뿐이면 거리 0). 먼저 껍질을 구하고 O(h) 로 대척점을 찾는다."""
    hull = convex_hull(points)
    if len(hull) == 1:
        return 0, hull[0], hull[0]
    n = len(hull)
    best = (0, hull[0], hull[0])
    j = 1
    for i in range(n):
        a, b = hull[i], hull[(i + 1) % n]
        # 변 ab 에서 가장 먼 꼭짓점: 변과의 거리(= 외적 크기)가 더는 늘지 않을 때까지 j 를 전진
        while cross(a, b, hull[(j + 1) % n]) > cross(a, b, hull[j]):
            j = (j + 1) % n
        for k in (j, (j + 1) % n):  # 평행한 변이 있을 때 두 꼭짓점 모두 후보
            for p in (a, b):
                d = squared_distance(p, hull[k])
                if d > best[0]:
                    best = (d, p, hull[k])
    return best


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    points = [(int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n)]
    print(len(convex_hull(points)))


if __name__ == "__main__":
    main()
