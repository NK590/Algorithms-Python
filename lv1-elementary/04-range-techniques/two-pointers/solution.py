"""투 포인터 — 두 위치(포인터)를 한 방향으로만 움직이며 O(n) 에 구간·쌍을 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 정렬된 배열의 양 끝에서 안쪽으로 오는 방식(pair_with_sum_sorted)과, 같은 방향으로 움직이는 구간 방식(슬라이딩 윈도우)이 있습니다.
- 구간 방식은 원소가 모두 양수라서 "구간을 늘리면 합이 커지고, 줄이면 작아진다"는 단조성이 있을 때 쓸 수 있습니다.
- 직접 실행하면 `N M` 과 N 개의 양의 정수를 받아 합이 M 인 연속 부분 구간의 개수를 출력합니다.
"""
import sys


def pair_with_sum_sorted(arr: list, target):
    """오름차순 arr 에서 합이 target 인 서로 다른 두 위치 (i, j) (i < j). 없으면 None.

    양 끝에서 시작해, 합이 크면 큰 쪽(오른쪽)을 줄이고 작으면 작은 쪽(왼쪽)을 늘린다. 각 포인터는 한 방향으로만 가므로 O(n).
    """
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return left, right
        if total < target:
            left += 1  # 왼쪽 값을 늘려야 합이 커진다. 지금의 left 는 어떤 right 와도 target 이 안 되므로 버려도 된다
        else:
            right -= 1
    return None


def count_subarrays_with_sum(arr: list, target) -> int:
    """합이 정확히 target 인 연속 부분 배열의 개수. arr 의 원소는 모두 양수여야 한다. O(n)

    오른쪽 끝(end)을 하나씩 늘리며 합이 target 을 넘으면 왼쪽 끝(start)을 줄인다.
    """
    count = 0
    total = 0
    start = 0
    for end in range(len(arr)):
        total += arr[end]
        while total > target and start <= end:
            total -= arr[start]
            start += 1
        if total == target:
            count += 1
    return count


def shortest_subarray_at_least(arr: list, s) -> int:
    """합이 s 이상인 연속 부분 배열 중 가장 짧은 것의 길이. 없으면 0. arr 의 원소는 모두 양수여야 한다. O(n)"""
    best = 0
    total = 0
    start = 0
    for end in range(len(arr)):
        total += arr[end]
        while total >= s:  # 조건을 만족하는 동안 왼쪽을 줄여 가며 최소 길이를 갱신한다
            length = end - start + 1
            if best == 0 or length < best:
                best = length
            total -= arr[start]
            start += 1
    return best


def merge_sorted(a: list, b: list) -> list:
    """정렬된 두 리스트를 합친다. 각 리스트에 포인터를 하나씩 두고 작은 쪽을 가져간다. O(len(a) + len(b))"""
    merged = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    arr = list(map(int, input().split()))[:n]
    print(count_subarrays_with_sum(arr, m))


if __name__ == "__main__":
    main()
