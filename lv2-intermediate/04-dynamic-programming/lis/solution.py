"""LIS (가장 긴 증가하는 부분 수열) — O(n log n) 이분 탐색 풀이

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 핵심: `tails[k]` = 길이가 k+1 인 증가 부분 수열의 마지막 값 중 가장 작은 것. tails 는 항상 오름차순이라 이분 탐색이 가능합니다.
- 각 수 x 에 대해 tails 에서 x 이상인 첫 위치를 찾아 x 로 바꾸고, 없으면 끝에 붙입니다. 최종 tails 의 길이가 LIS 의 길이입니다.
  (tails 자체는 LIS 가 아닙니다. 길이만 정확합니다. 수열을 복원하려면 위치와 이전 원소를 따로 기록합니다)
- 직접 실행하면 `N` 과 수열을 받아 LIS 의 길이를 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right


def lis_length(numbers: list[int]) -> int:
    """엄격하게 증가하는(같은 값 불가) 부분 수열의 최대 길이."""
    tails = []
    for x in numbers:
        i = bisect_left(tails, x)  # x 이상인 첫 위치
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x  # 같은 길이의 증가 수열 중 더 작은 끝값으로 교체: 뒤에 이어 붙이기 더 쉽다
    return len(tails)


def lis_sequence(numbers: list[int]) -> list[int]:
    """LIS 하나를 복원한다. tails_idx[k] = tails[k] 값을 가진 원소의 위치, prev[i] = i 번째 원소 바로 앞에 이어지는 원소의 위치."""
    tails = []
    tails_idx = []
    prev = [-1] * len(numbers)
    for i, x in enumerate(numbers):
        pos = bisect_left(tails, x)
        prev[i] = tails_idx[pos - 1] if pos > 0 else -1
        if pos == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[pos] = x
            tails_idx[pos] = i
    sequence = []
    i = tails_idx[-1] if tails_idx else -1
    while i != -1:
        sequence.append(numbers[i])
        i = prev[i]
    return sequence[::-1]


def longest_non_decreasing(numbers: list[int]) -> int:
    """같은 값을 허용하는(비내림차순) 최장 부분 수열. 엄격 증가와 bisect_left → bisect_right 한 글자 차이다."""
    tails = []
    for x in numbers:
        i = bisect_right(tails, x)  # x 보다 큰 첫 위치
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def lis_lengths_ending_at(numbers: list[int]) -> list[int]:
    """result[i] = i 번째 원소를 마지막으로 하는 LIS 의 길이. 이분 탐색 위치 + 1 이 곧 그 길이다."""
    tails = []
    result = []
    for x in numbers:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
        result.append(i + 1)
    return result


def longest_bitonic(numbers: list[int]) -> int:
    """증가하다가 감소하는(한쪽이 비어도 된다) 부분 수열의 최대 길이.

    i 를 꼭대기로 하면 (i 에서 끝나는 LIS) + (i 에서 시작하는 감소 수열) - 1. 뒤집은 수열에서 구한 LIS 가 곧 i 에서 시작하는 감소 수열이다."""
    if not numbers:
        return 0
    up = lis_lengths_ending_at(numbers)
    down = lis_lengths_ending_at(numbers[::-1])[::-1]
    return max(u + d - 1 for u, d in zip(up, down))


def min_removals_to_sort(numbers: list[int]) -> int:
    """오름차순(엄격)으로 만들기 위해 지워야 하는 최소 원소 수 = n - LIS."""
    return len(numbers) - lis_length(numbers)


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    numbers = list(map(int, input().split()))[:n]
    print(lis_length(numbers))


if __name__ == "__main__":
    main()
