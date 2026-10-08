"""이분 탐색 — 정렬된 배열에서 탐색 범위를 절반씩 줄여 가며 값을 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 입력 배열은 오름차순으로 정렬되어 있어야 합니다. 정렬되지 않았다면 결과는 의미가 없습니다.
- 직접 실행하면 `N M`, 정렬된 N 개의 수, M 개의 질문을 받아 각 질문의 수가 배열에 있으면 1, 없으면 0 을 한 줄에 출력합니다.
"""
import sys


def binary_search(arr: list, target) -> int:
    """target 이 있는 위치를 반환한다. 없으면 -1. 같은 값이 여러 개면 그중 어느 위치가 나올지는 정해지지 않는다. O(log n)"""
    lo, hi = 0, len(arr) - 1  # 답이 있다면 arr[lo..hi] 안에 있다
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1  # 가운데보다 작은 쪽은 모두 버린다
        else:
            hi = mid - 1
    return -1


def binary_search_recursive(arr: list, target, lo: int = 0, hi: int | None = None) -> int:
    """같은 탐색을 재귀로. 깊이가 log n 이라 깊이 제한 걱정은 없다."""
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, hi)
    return binary_search_recursive(arr, target, lo, mid - 1)


def binary_search_steps(arr: list, target) -> int:
    """탐색이 끝날 때까지 가운데를 들여다본 횟수. 최악에도 ⌊log2 n⌋ + 1 번이다."""
    lo, hi = 0, len(arr) - 1
    steps = 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if arr[mid] == target:
            break
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return steps


def integer_sqrt(n: int) -> int:
    """x * x <= n 인 가장 큰 x. 배열이 없어도 "x 가 크면 x*x 도 크다"는 단조성만 있으면 이분 탐색을 쓸 수 있다."""
    lo, hi = 0, n  # lo 는 항상 조건을 만족하고, hi + 1 은 항상 만족하지 않는다
    while lo < hi:
        mid = (lo + hi + 1) // 2  # 올림해야 lo = mid 로 갈 때 무한 반복에 빠지지 않는다
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))[:n]
    queries = list(map(int, input().split()))[:m]
    print(*(1 if binary_search(arr, q) != -1 else 0 for q in queries))


if __name__ == "__main__":
    main()
