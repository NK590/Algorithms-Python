"""슬라이딩 윈도우 — 고정되었거나 늘었다 줄었다 하는 구간(창)을 한 칸씩 밀며, 구간의 합·최솟값·중복 여부를 O(n) 에 갱신하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 고정 길이 창: 들어오는 원소를 더하고 나가는 원소를 뺀다. 최대·최소는 덱(단조 덱)으로 O(1) 에 유지합니다.
- 가변 길이 창: 오른쪽 끝을 늘리다가 조건이 깨지면 왼쪽 끝을 줄인다(투 포인터). 각 끝점은 한 방향으로만 움직이므로 O(n).
- window_max / window_min 은 각 위치 i 에서 "i 에서 끝나는 길이 k 의 창(앞부분은 짧은 창)" 의 값을 돌려줍니다. 완전한 창만 보려면 result[k-1:].
- 직접 실행하면 `N L` 과 수열을 받아 각 i 에 대해 최근 L 개(앞부분은 더 적게)의 최솟값을 출력합니다.
"""
import sys
from collections import deque


def window_max(numbers: list[int], k: int) -> list[int]:
    """result[i] = numbers[max(0, i-k+1) .. i] 의 최댓값. 덱에는 창 안의 후보 위치를 값이 큰 순서(내림차순)로 둔다.

    새 원소가 들어오면 그보다 작은 후보는 영원히 최댓값이 될 수 없으므로 뒤에서 버린다. 앞의 원소는 창을 벗어나면 버린다."""
    result = []
    candidates: deque[int] = deque()
    for i, x in enumerate(numbers):
        while candidates and numbers[candidates[-1]] <= x:
            candidates.pop()
        candidates.append(i)
        if candidates[0] <= i - k:  # 창을 벗어난 맨 앞 후보
            candidates.popleft()
        result.append(numbers[candidates[0]])
    return result


def window_min(numbers: list[int], k: int) -> list[int]:
    """result[i] = numbers[max(0, i-k+1) .. i] 의 최솟값. window_max 의 부등호만 반대."""
    result = []
    candidates: deque[int] = deque()
    for i, x in enumerate(numbers):
        while candidates and numbers[candidates[-1]] >= x:
            candidates.pop()
        candidates.append(i)
        if candidates[0] <= i - k:
            candidates.popleft()
        result.append(numbers[candidates[0]])
    return result


def max_sum_of_k_consecutive(numbers: list[int], k: int) -> int:
    """길이 k 인 연속 구간의 합의 최댓값 (고정 길이 창). 들어오는 값을 더하고 나가는 값을 뺀다. k > n 이면 0."""
    if k <= 0 or k > len(numbers):
        return 0
    window = sum(numbers[:k])
    best = window
    for i in range(k, len(numbers)):
        window += numbers[i] - numbers[i - k]
        best = max(best, window)
    return best


def longest_unique_substring(s: str) -> int:
    """같은 글자가 없는 가장 긴 연속 부분 문자열의 길이 (가변 길이 창). 글자가 중복되면 왼쪽 끝을 그 글자의 이전 위치 바로 뒤로 옮긴다."""
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def longest_with_at_most_k_distinct(items: list, k: int) -> int:
    """서로 다른 값이 k 가지 이하인 가장 긴 연속 구간의 길이. 오른쪽을 늘리고, 종류가 k 를 넘으면 왼쪽을 줄인다."""
    if k <= 0:
        return 0
    counts: dict = {}
    left = best = 0
    for right, x in enumerate(items):
        counts[x] = counts.get(x, 0) + 1
        while len(counts) > k:
            y = items[left]
            counts[y] -= 1
            if counts[y] == 0:
                del counts[y]
            left += 1
        best = max(best, right - left + 1)
    return best


def shortest_subarray_sum_at_least(numbers: list[int], target: int) -> int:
    """합이 target 이상인 가장 짧은 연속 구간의 길이 (원소는 모두 양수). 없으면 0.

    합이 target 이상이 되면 왼쪽을 줄여 보며 가장 짧은 길이를 갱신한다. 원소가 양수라서 구간을 줄이면 합이 단조 감소한다(음수가 있으면 틀린다)."""
    left = total = 0
    best = len(numbers) + 1
    for right, x in enumerate(numbers):
        total += x
        while total >= target and left <= right:
            best = min(best, right - left + 1)
            total -= numbers[left]
            left += 1
    return best if best <= len(numbers) else 0


def min_window_covering(s: str, t: str) -> str:
    """s 의 연속 부분 문자열 중 t 의 모든 글자(중복 포함)를 포함하는 가장 짧은 것. 같은 길이면 가장 왼쪽. 없으면 빈 문자열."""
    if not t:
        return ""
    need: dict[str, int] = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    missing = len(t)  # 아직 채우지 못한 글자 수
    left = 0
    best = (len(s) + 1, 0)
    for right, ch in enumerate(s):
        if need.get(ch, 0) > 0:
            missing -= 1
        need[ch] = need.get(ch, 0) - 1
        while missing == 0:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best[0] > len(s) else s[best[1] : best[1] + best[0]]


def main() -> None:
    input = sys.stdin.readline
    n, k = map(int, input().split())
    numbers = list(map(int, input().split()))[:n]
    print(" ".join(map(str, window_min(numbers, k))))


if __name__ == "__main__":
    main()
