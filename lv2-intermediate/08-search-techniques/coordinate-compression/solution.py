"""좌표 압축 — 값의 크기 자체는 필요 없고 "순서" 만 중요할 때, 큰 값들을 0, 1, 2, … 의 작은 번호로 바꾸기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 값을 정렬하고 중복을 제거한 목록에서의 위치(순위)로 바꿉니다. 값의 대소 관계는 그대로 유지되고 값의 범위가 n 이하로 줄어듭니다.
- 값의 범위가 10⁹ 인 문제에서 배열(누적 합, 차분 배열, 세그먼트 트리, 펜윅 트리)을 쓰기 위한 전처리입니다.
- 순위를 매기는 방법: 같은 값이 같은 순위(compress), 같은 값도 서로 다른 순위(ordinal_ranks).
- 직접 실행하면 `N` 과 수열을 받아, 각 값보다 작은 서로 다른 값의 개수(압축된 좌표)를 출력합니다.
"""
import sys
from bisect import bisect_left


def coordinate_maps(values: list) -> tuple[list, dict]:
    """(정렬된 서로 다른 값 목록, 값 → 순위 딕셔너리). 압축한 좌표를 원래 값으로 되돌릴 때는 목록의 인덱스."""
    ordered = sorted(set(values))
    return ordered, {v: i for i, v in enumerate(ordered)}


def compress(values: list) -> list[int]:
    """각 값을 '자기보다 작은 서로 다른 값의 개수'(0 부터)로 바꾼다. 같은 값은 같은 번호가 된다."""
    ordered = sorted(set(values))
    return [bisect_left(ordered, v) for v in values]


def ordinal_ranks(values: list) -> list[int]:
    """같은 값도 서로 다른 번호를 주는 순위 (0 부터). 같은 값끼리는 처음 나온 순서대로 번호가 매겨진다 (안정 정렬)."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0] * len(values)
    for rank, i in enumerate(order):
        ranks[i] = rank
    return ranks


def decompress(compressed: list[int], ordered: list) -> list:
    """compress 의 반대: 번호를 원래 값으로."""
    return [ordered[c] for c in compressed]


def compress_points(points: list[tuple]) -> list[tuple[int, int]]:
    """점 (x, y) 들의 x 와 y 를 각각 따로 압축한다. 점들의 상대적인 위치(위/아래/왼쪽/오른쪽 관계)는 유지된다."""
    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})
    return [(bisect_left(xs, x), bisect_left(ys, y)) for x, y in points]


def max_overlap_count(intervals: list[tuple[int, int]]) -> int:
    """닫힌 구간 [l, r] 들(좌표는 매우 클 수 있다)이 한 점에서 겹치는 최대 개수.

    구간의 시작 l 에 +1, 끝 다음 지점 r + 1 에 -1 을 놓는 차분 배열을 만들되, 좌표를 압축해서 배열의 크기를 구간 수의 2 배로 줄인다."""
    points = sorted({p for l, r in intervals for p in (l, r + 1)})
    index = {p: i for i, p in enumerate(points)}
    diff = [0] * (len(points) + 1)
    for l, r in intervals:
        diff[index[l]] += 1
        diff[index[r + 1]] -= 1
    best = current = 0
    for d in diff:
        current += d
        best = max(best, current)
    return best


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    values = list(map(int, input().split()))[:n]
    print(" ".join(map(str, compress(values))))


if __name__ == "__main__":
    main()
