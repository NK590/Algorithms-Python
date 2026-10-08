"""퀵 정렬 — 기준값(pivot)을 정해 작은 쪽과 큰 쪽으로 나누고, 각각을 같은 방식으로 정렬하는 정렬

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- quick_sort 는 입력을 바꾸지 않고 정렬된 새 리스트를 반환합니다. (이해하기 쉬운 버전)
- quick_sort_inplace 는 입력을 제자리에서 정렬합니다. (추가 리스트 없이 원소를 맞바꿈)
- quick_select 는 같은 분할을 이용해 k번째로 작은 값을 평균 O(n) 에 구합니다.
- 어느 쪽도 안정 정렬은 아닙니다. 기준값은 무작위로 고르고, 기준값과 같은 값들은 따로 모아 두 번 다시 정렬하지 않습니다.
- 직접 실행하면 첫 줄에 N, 둘째 줄부터 N개의 정수를 받아 오름차순으로 한 줄에 하나씩 출력합니다.
"""
import random
import sys


def quick_sort(arr: list) -> list:
    """arr 을 오름차순으로 정렬한 새 리스트를 반환한다. arr 은 바꾸지 않는다."""
    if len(arr) <= 1:
        return list(arr)
    pivot = arr[random.randrange(len(arr))]
    smaller = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]  # 기준값과 같은 값은 이미 제자리에 있다. 다시 정렬하지 않는다.
    larger = [x for x in arr if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)


def _partition(arr: list, lo: int, hi: int) -> tuple[int, int]:
    """arr[lo..hi] 를 (기준값보다 작은 값 | 기준값과 같은 값 | 큰 값) 으로 나누고, 같은 값 구간 [lt, gt] 를 반환한다."""
    pivot = arr[random.randint(lo, hi)]
    lt, i, gt = lo, lo, hi  # arr[lo:lt] < pivot,  arr[lt:i] == pivot,  arr[gt+1:hi+1] > pivot,  arr[i:gt+1] 은 미확인
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1  # 새로 온 arr[i] 는 아직 확인하지 않았으므로 i 는 그대로 둔다
        else:
            i += 1
    return lt, gt


def quick_sort_inplace(arr: list) -> None:
    """arr 을 제자리에서 오름차순으로 정렬한다."""
    stack = [(0, len(arr) - 1)]  # 재귀 대신 직접 만든 스택을 써서 재귀 깊이 제한을 피한다
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        lt, gt = _partition(arr, lo, hi)
        stack.append((lo, lt - 1))
        stack.append((gt + 1, hi))


def quick_select(arr: list, k: int):
    """arr 에서 k번째(0부터 센다)로 작은 값을 구한다. arr 은 바꾸지 않는다."""
    if not 0 <= k < len(arr):
        raise IndexError("k 가 범위를 벗어났습니다")
    arr = list(arr)
    lo, hi = 0, len(arr) - 1
    while True:
        lt, gt = _partition(arr, lo, hi)
        if k < lt:  # 찾는 값은 기준값보다 작은 쪽에 있다 → 그쪽만 다시 본다
            hi = lt - 1
        elif k > gt:
            lo = gt + 1
        else:
            return arr[k]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    quick_sort_inplace(arr)
    print("\n".join(map(str, arr)))


if __name__ == "__main__":
    main()
