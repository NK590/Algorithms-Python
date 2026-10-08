"""누적 합 — 앞에서부터의 합을 미리 구해 두고, 구간 합을 O(1) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- prefix[i] 는 arr[0..i-1] 의 합입니다. (prefix[0] = 0 으로 두면 맨 앞 구간도 같은 식으로 처리됩니다)
- 직접 실행하면 `N M`, N 개의 수, M 개의 질문 `i j` (1부터, 양 끝 포함)를 받아 arr[i..j] 의 합을 한 줄씩 출력합니다.
"""
import sys


def build_prefix(arr: list) -> list:
    """prefix[i] = arr[0] + ... + arr[i-1]. 길이는 len(arr) + 1. O(n)"""
    prefix = [0] * (len(arr) + 1)
    for i, value in enumerate(arr):
        prefix[i + 1] = prefix[i] + value
    return prefix


def range_sum(prefix: list, left: int, right: int):
    """arr[left..right] (양 끝 포함, 0부터)의 합. (0..right 의 합) − (0..left-1 의 합) 이다. O(1)"""
    return prefix[right + 1] - prefix[left]


def count_subarrays_with_sum(arr: list, k) -> int:
    """합이 정확히 k 인 연속 부분 배열의 개수 (음수가 섞여 있어도 된다).

    j 에서 끝나는 구간의 합이 k 이려면 prefix[i] = prefix[j+1] − k 인 i 가 있어야 한다.
    지금까지 본 prefix 값의 개수를 딕셔너리에 세어 두면 한 번 훑어서 O(n) 이다.
    """
    seen = {0: 1}  # 아무것도 포함하지 않는 prefix[0] = 0
    total = 0
    count = 0
    for value in arr:
        total += value
        count += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return count


def apply_range_adds(n: int, updates: list) -> list:
    """길이 n 의 0 배열에 구간 더하기 (left, right, value) 들을 모두 적용한 결과. 차이 배열로 O(n + 업데이트 수).

    구간 [l, r] 에 v 를 더하는 일을 diff[l] += v, diff[r+1] -= v 두 칸만 바꿔 기록하고,
    마지막에 diff 의 누적 합을 구하면 각 칸의 최종 값이 된다.
    """
    diff = [0] * (n + 1)
    for left, right, value in updates:
        diff[left] += value
        diff[right + 1] -= value
    result = []
    running = 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    prefix = build_prefix(list(map(int, input().split()))[:n])
    out = []
    for _ in range(m):
        i, j = map(int, input().split())
        out.append(range_sum(prefix, i - 1, j - 1))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
