"""스위핑(Sweep Line) — 평면이나 직선 위의 도형을 한 방향으로 훑으며(이벤트를 정렬해 순서대로 처리) 상태를 갱신하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 구간의 시작과 끝을 "이벤트" 로 만들어 위치순으로 정렬한 뒤 차례로 처리합니다. 같은 위치에서는 끝 이벤트를 시작 이벤트보다 먼저 처리해야
  [시작, 끝) 처럼 맞닿는 구간이 겹치지 않는 것으로 계산됩니다.
- 다섯 가지: 가장 많이 겹치는 곳, 구간 합치기, 덮인 길이(선 긋기), 스카이라인, 직사각형들의 합집합 넓이.
- 직접 실행하면 `N` 과 N 개의 선분 `x y` 를 받아 선분들이 덮은 전체 길이를 출력합니다.
"""
import heapq
import sys


def max_overlap(intervals: list[tuple[int, int]]) -> int:
    """반열린 구간 [시작, 끝) 들이 한 점에서 겹치는 최대 개수. 시작 +1, 끝 -1 이벤트를 정렬하고, 같은 위치에서는 끝(-1) 을 먼저 처리한다."""
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    events.sort()  # (위치, +1/-1) 이므로 같은 위치에서 -1 이 +1 보다 앞선다
    best = current = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """닫힌 구간 [l, r] 들 중 겹치거나 끝점이 맞닿은 것을 합쳐 서로소인 구간 목록으로. 시작점 순으로 훑으며 지금까지의 끝을 늘려 간다."""
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(l, r) for l, r in merged]


def covered_length(segments: list[tuple[int, int]]) -> int:
    """선분 [l, r] 들(l ≤ r)이 직선 위에서 덮는 전체 길이(합집합의 길이)."""
    return sum(r - l for l, r in merge_intervals(segments))


def skyline(buildings: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    """건물 (왼쪽 x, 오른쪽 x, 높이) 들의 윤곽선: 높이가 바뀌는 지점 (x, 새 높이) 목록. 땅으로 내려오면 높이 0.

    x 순으로 훑으며 현재 덮고 있는 건물들의 높이를 최대 힙으로 관리한다. 끝난 건물은 맨 위에 올 때 지연 삭제한다."""
    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))  # 시작: 높이가 큰 것을 먼저 (같은 x 에서 높이 내림차순)
        events.append((right, 0, 0))  # 끝: 힙에서 지연 삭제하므로 표시만 한다
    events.sort()
    result: list[tuple[int, int]] = []
    heap = [(0, float("inf"))]  # (-높이, 끝나는 x): 땅
    for x, neg_height, right in events:
        while heap and heap[0][1] <= x:
            heapq.heappop(heap)  # 이미 끝난 건물
        if neg_height != 0:
            heapq.heappush(heap, (neg_height, right))
        top = -heap[0][0]
        if not result or result[-1][1] != top:
            result.append((x, top))
    return result


def rectangle_union_area(rects: list[tuple[int, int, int, int]]) -> int:
    """축에 평행한 직사각형 (x1, y1, x2, y2) 들의 합집합의 넓이 (x1 < x2, y1 < y2).

    x 좌표를 압축해 인접한 두 x 사이의 '띠' 마다, 그 띠를 가로지르는 직사각형들의 y 구간을 합쳐 덮인 높이를 구하고 너비를 곱한다.
    O(n² log n) 이라 직사각형이 수백 개까지 쓸 수 있고, 많으면 세그먼트 트리로 높이를 관리한다(Lv3)."""
    xs = sorted({x for x1, _, x2, _ in rects for x in (x1, x2)})
    area = 0
    for left, right in zip(xs, xs[1:]):
        ys = [(y1, y2) for x1, y1, x2, y2 in rects if x1 <= left and right <= x2]
        area += (right - left) * covered_length(ys)
    return area


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    segments = []
    for _ in range(n):
        x, y = map(int, input().split())
        segments.append((min(x, y), max(x, y)))
    print(covered_length(segments))


if __name__ == "__main__":
    main()
