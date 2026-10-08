"""매개변수 탐색(Parametric Search) — "답이 X 이하/이상으로 가능한가?" 를 판정하는 함수를 만들고, 답 X 를 이분 탐색하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 조건: 판정 함수 ok(x) 가 단조여야 합니다. 즉 x 가 커질수록 (또는 작아질수록) False…False True…True 처럼 한 번만 바뀝니다.
- 최솟값을 구할 때(최소 x 로 ok) 는 첫 True 를, 최댓값을 구할 때(최대 x 로 ok) 는 마지막 True 를 이분 탐색합니다.
- 다섯 가지 응용: 랜선 자르기, 나무 자르기, 공유기 설치(가장 가까운 두 공유기 사이 거리의 최대), 배열 나누기(부분 합의 최대를 최소로), 최소 시간.
- 직접 실행하면 `K N` 과 K 개의 랜선 길이를 받아 N 개 이상 만들 수 있는 최대 길이를 출력합니다.
"""
import sys
from typing import Callable


def first_true(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """[lo, hi] 에서 ok 가 처음 True 가 되는 값. 모두 False 이면 hi + 1. ok 는 False…False True…True 모양이어야 한다."""
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid - 1  # mid 도 답의 후보이므로 더 작은 쪽을 찾는다
        else:
            lo = mid + 1
    return lo


def last_true(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """[lo, hi] 에서 ok 가 마지막으로 True 인 값. 모두 False 이면 lo - 1. ok 는 True…True False…False 모양이어야 한다."""
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            lo = mid + 1  # mid 도 답의 후보이므로 더 큰 쪽을 찾는다
        else:
            hi = mid - 1
    return hi


def max_cable_length(cables: list[int], need: int) -> int:
    """같은 길이로 잘라 need 개 이상을 만들 수 있는 가장 긴 길이 (정수). 만들 수 없으면 0."""
    if not cables:
        return 0
    return last_true(1, max(cables), lambda length: sum(c // length for c in cables) >= need)


def max_cutter_height(trees: list[int], need: int) -> int:
    """절단기 높이를 정해 그 위쪽을 잘라 얻는 나무 길이가 need 이상이 되는 가장 높은 높이. 나무가 모자라면 -1."""
    return last_true(0, max(trees, default=0), lambda h: sum(t - h for t in trees if t > h) >= need)


def max_min_distance(positions: list[int], count: int) -> int:
    """위치 positions 중 count 개를 골라 이웃한 두 개 사이의 최소 거리를 최대화한 값 (공유기 설치).

    판정: 거리 d 이상 떨어뜨려 count 개를 놓을 수 있는가 — 앞에서부터 가능한 가장 앞의 위치에 그리디로 놓는다."""
    pts = sorted(positions)
    if count < 2 or len(pts) < count:
        return 0

    def can_place(d):
        placed, last = 1, pts[0]
        for x in pts[1:]:
            if x - last >= d:
                placed += 1
                last = x
        return placed >= count

    return last_true(1, pts[-1] - pts[0], can_place)


def split_array_min_largest_sum(numbers: list[int], parts: int) -> int:
    """배열을 연속한 parts 개의 묶음으로 나눌 때, 묶음 합의 최댓값을 최소로 만든 값 (numbers 는 0 이상).

    판정: 묶음 합이 limit 이하가 되도록 나눴을 때 묶음 수가 parts 이하인가 — 한 묶음에 가능한 한 많이 담는 그리디."""
    if not numbers:
        return 0

    def can_split(limit):
        groups, current = 1, 0
        for x in numbers:
            if current + x > limit:
                groups += 1
                current = x
            else:
                current += x
        return groups <= parts

    return first_true(max(numbers), sum(numbers), can_split)


def min_time_to_finish(speeds: list[int], jobs: int) -> int:
    """일꾼마다 한 개를 만드는 데 걸리는 시간 speeds[i] 가 있을 때, 모두 동시에 일해 jobs 개를 만드는 최소 시간 (정수)."""
    if jobs <= 0:
        return 0
    return first_true(1, min(speeds) * jobs, lambda t: sum(t // s for s in speeds) >= jobs)


def main() -> None:
    input = sys.stdin.readline
    k, n = map(int, input().split())
    cables = [int(input()) for _ in range(k)]
    print(max_cable_length(cables, n))


if __name__ == "__main__":
    main()
