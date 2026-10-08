"""병합 정렬 — 반으로 나눠 각각 정렬한 뒤, 두 정렬된 리스트를 합치는 정렬 (분할 정복)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- merge_sort 는 입력을 바꾸지 않고 정렬된 새 리스트를 반환합니다. (안정 정렬)
- count_inversions 는 같은 방식으로 뒤집힌 쌍(역전)의 수를 O(n log n) 에 셉니다.
- 직접 실행하면 첫 줄에 N, 둘째 줄부터 N개의 정수를 받아 오름차순으로 한 줄에 하나씩 출력합니다.
"""
import sys


def merge(left: list, right: list) -> list:
    """정렬된 두 리스트를 하나의 정렬된 리스트로 합친다."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # 같을 때 왼쪽을 먼저 꺼내야 안정 정렬이 된다
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    # 둘 중 한쪽이 먼저 바닥나면, 남은 쪽은 이미 정렬되어 있으므로 통째로 붙인다.
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: list) -> list:
    """arr 을 오름차순으로 정렬한 새 리스트를 반환한다. arr 은 바꾸지 않는다."""
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def count_inversions(arr: list) -> int:
    """i < j 이면서 arr[i] > arr[j] 인 쌍의 수를 센다. arr 은 바꾸지 않는다."""
    return _sort_and_count(list(arr))[1]


def _sort_and_count(arr: list) -> tuple[list, int]:
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, left_count = _sort_and_count(arr[:mid])
    right, right_count = _sort_and_count(arr[mid:])

    merged = []
    count = left_count + right_count
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # right[j] 가 left[i:] 의 모든 원소보다 작다. 이 원소들은 모두 right[j] 와 뒤집힌 쌍이다.
            count += len(left) - i
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, count


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    print("\n".join(map(str, merge_sort(arr))))


if __name__ == "__main__":
    main()
