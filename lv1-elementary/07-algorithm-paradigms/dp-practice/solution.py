"""1차원·2차원 DP 연습 — 상태를 어떻게 잡느냐가 전부인 대표 유형 일곱 가지

README.md 의 설명과 짝을 이루는 참고 구현입니다. 1 차원 표 4 개, 2 차원 표 3 개.
 1D  max_subarray_sum   dp[i] = i 에서 끝나는 구간 합의 최댓값
 1D  lis_length / lis_sequence  dp[i] = i 를 마지막으로 하는 증가 부분 수열의 최대 길이
 1D  rob_houses         dp[i] = 앞의 i 채까지 고려한 최대 금액 (이웃은 못 턴다)
 1D  stairs_max_score   연속 세 계단은 못 밟는다 → 상태에 "연속 몇 칸째"를 넣는다
 2D  min_path_sum       오른쪽·아래로만 이동하는 최소 비용
 2D  triangle_max_path  삼각형 위에서 아래로 내려가는 최대 합
 2D  count_paths        장애물이 있는 격자에서 경로의 수
- 직접 실행하면 `N` 과 N 개의 수를 받아 연속 부분 구간 합의 최댓값을 출력합니다.
"""
import sys


def max_subarray_sum(numbers: list) -> int:
    """비어 있지 않은 연속 구간의 합의 최댓값 (카데인 알고리즘).

    dp[i] = i 번째 수에서 끝나는 구간 합의 최댓값 = max(numbers[i], dp[i-1] + numbers[i]).
    앞이 손해면 버리고 새로 시작한다. 직전 값만 쓰므로 변수 하나면 된다."""
    best = current = numbers[0]
    for x in numbers[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best


def lis_length(numbers: list) -> int:
    """가장 긴 증가하는 부분 수열의 길이. O(n²). (Lv2 에서 O(n log n) 으로 줄인다)"""
    if not numbers:
        return 0
    dp = [1] * len(numbers)
    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp)


def lis_sequence(numbers: list) -> list:
    """LIS 하나를 복원해서 반환한다. 앞 원소를 가리키는 prev 를 따라 거슬러 올라간다."""
    if not numbers:
        return []
    n = len(numbers)
    dp = [1] * n
    prev = [-1] * n
    for i in range(n):
        for j in range(i):
            if numbers[j] < numbers[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    i = max(range(n), key=lambda k: dp[k])
    sequence = []
    while i != -1:
        sequence.append(numbers[i])
        i = prev[i]
    return sequence[::-1]


def rob_houses(money: list) -> int:
    """일렬로 놓인 집에서 이웃한 두 집을 모두 털 수는 없을 때 훔칠 수 있는 최대 금액.

    dp[i] = max(dp[i-1] (i 번째를 건너뜀), dp[i-2] + money[i] (i 번째를 텀))."""
    skip, take = 0, 0  # dp[i-1], dp[i-2] 역할
    for m in money:
        skip, take = max(skip, take + m), skip
    return skip


def stairs_max_score(scores: list) -> int:
    """계단을 한 번에 1칸 또는 2칸 오르고, 연속된 세 계단을 모두 밟을 수는 없다. 마지막 계단은 반드시 밟는다. 점수의 합의 최댓값.

    dp[i][k] = i 번째 계단을 밟았고 연속 k 번째(1 또는 2)로 밟았을 때의 최댓값."""
    n = len(scores)
    if n == 0:
        return 0
    neg = float("-inf")
    dp = [[neg, neg] for _ in range(n)]
    dp[0][0] = scores[0]  # 첫 계단을 밟음 (연속 1)
    for i in range(1, n):
        dp[i][1] = dp[i - 1][0] + scores[i]  # 바로 전 계단에서 올라옴 → 연속 2
        prior = max(dp[i - 2]) if i >= 2 else 0  # 두 칸 전에서 올라옴 → 연속 1 (i = 1 이면 시작 전에서 두 칸)
        dp[i][0] = prior + scores[i]
    return max(dp[-1])


def min_path_sum(grid: list) -> int:
    """왼쪽 위에서 오른쪽 아래까지 오른쪽·아래로만 이동할 때 지나는 칸의 합의 최솟값.

    dp[r][c] = (r, c) 까지의 최소 합 = grid[r][c] + min(위, 왼쪽)."""
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                dp[r][c] = grid[0][0]
            elif r == 0:
                dp[r][c] = dp[r][c - 1] + grid[r][c]
            elif c == 0:
                dp[r][c] = dp[r - 1][c] + grid[r][c]
            else:
                dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]
    return dp[-1][-1]


def triangle_max_path(triangle: list) -> int:
    """맨 위에서 시작해 아래 줄의 왼쪽·오른쪽 대각선으로 내려갈 때 지나는 수의 합의 최댓값.

    아래에서 위로 올라오며 계산하면 마지막 줄의 처리가 따로 필요 없다: dp[r][c] = t[r][c] + max(dp[r+1][c], dp[r+1][c+1])."""
    dp = list(triangle[-1])
    for row in range(len(triangle) - 2, -1, -1):
        dp = [triangle[row][c] + max(dp[c], dp[c + 1]) for c in range(len(triangle[row]))]
    return dp[0]


def count_paths(grid: list) -> int:
    """0 은 길, 1 은 장애물인 격자에서 왼쪽 위 → 오른쪽 아래로 오른쪽·아래로만 가는 경로의 수.

    dp[r][c] = dp[r-1][c] + dp[r][c-1] (장애물이면 0)."""
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1:
        return 0
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 or (r == 0 and c == 0):
                continue
            dp[r][c] = (dp[r - 1][c] if r else 0) + (dp[r][c - 1] if c else 0)
    return dp[-1][-1]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    numbers = list(map(int, input().split()))[:n]
    print(max_subarray_sum(numbers))


if __name__ == "__main__":
    main()
