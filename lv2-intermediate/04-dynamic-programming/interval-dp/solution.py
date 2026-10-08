"""구간 DP — 구간 [l, r] 의 답을 더 짧은 구간들의 답으로 만드는 DP

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 상태: dp[l][r] = 구간 l..r 의 답. 점화식은 "구간을 어디서 나누는가(k)" 또는 "양 끝을 어떻게 처리하는가" 로 세웁니다.
- 계산 순서: 구간의 길이가 짧은 것부터 (길이 1 → 2 → … → n). 이렇게 하면 필요한 더 짧은 구간이 항상 먼저 계산되어 있습니다.
- 다섯 가지: 행렬 곱셈 순서, 인접한 파일 합치기, 최장 팰린드롬 부분 수열, 팰린드롬 구간 표, 풍선 터뜨리기.
- 직접 실행하면 `T`, 테스트 케이스마다 `K` 와 K 개의 파일 크기를 받아 모두 합치는 최소 비용을 출력합니다.
"""
import sys


def matrix_chain_order(dims: list[int]) -> tuple[int, str]:
    """행렬 k 개의 곱 A1 A2 … Ak 를 어떤 순서로 묶어 계산할지. i 번째 행렬의 크기는 dims[i-1] × dims[i] (dims 의 길이는 k + 1).

    (최소 스칼라 곱셈 횟수, 괄호를 친 식) 을 반환한다. dp[i][j] = Ai..Aj 를 곱하는 최소 횟수,
    dp[i][j] = min over k (dp[i][k] + dp[k+1][j] + dims[i-1]·dims[k]·dims[j])."""
    k = len(dims) - 1
    if k <= 0:
        return 0, ""
    inf = float("inf")
    dp = [[0] * (k + 1) for _ in range(k + 1)]
    split = [[0] * (k + 1) for _ in range(k + 1)]
    for length in range(2, k + 1):
        for i in range(1, k - length + 2):
            j = i + length - 1
            dp[i][j] = inf
            for m in range(i, j):
                cost = dp[i][m] + dp[m + 1][j] + dims[i - 1] * dims[m] * dims[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = m

    def build(i, j):
        if i == j:
            return f"A{i}"
        m = split[i][j]
        return f"({build(i, m)}{build(m + 1, j)})"

    return dp[1][k], build(1, k)


def min_merge_cost(sizes: list[int]) -> int:
    """일렬로 놓인 파일들을 **인접한 둘씩** 합쳐 하나로 만든다. 합치는 비용 = 두 파일 크기의 합. 총 비용의 최솟값.

    dp[l][r] = l..r 을 하나로 합치는 최소 비용 = min over k (dp[l][k] + dp[k+1][r]) + (l..r 의 크기 합).
    구간 합은 누적 합으로 O(1). (인접하지 않아도 되는 문제는 힙으로 푸는 그리디라서 전혀 다르다)"""
    n = len(sizes)
    if n <= 1:
        return 0
    prefix = [0]
    for s in sizes:
        prefix.append(prefix[-1] + s)
    inf = float("inf")
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            best = inf
            for k in range(l, r):
                cost = dp[l][k] + dp[k + 1][r]
                if cost < best:
                    best = cost
            dp[l][r] = best + prefix[r + 1] - prefix[l]
    return dp[0][n - 1]


def longest_palindromic_subsequence(s: str) -> int:
    """부분 수열 중 팰린드롬인 것의 최대 길이. dp[l][r]: 양 끝 글자가 같으면 안쪽 + 2, 다르면 한쪽을 버린 것 중 큰 쪽."""
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            if s[l] == s[r]:
                dp[l][r] = dp[l + 1][r - 1] + 2 if length > 2 else 2
            else:
                dp[l][r] = max(dp[l + 1][r], dp[l][r - 1])
    return dp[0][n - 1]


def palindrome_table(s: str) -> list[list[bool]]:
    """is_pal[l][r] = s[l..r] 이 팰린드롬인가. 양 끝이 같고 안쪽이 팰린드롬(또는 비어 있음/한 글자)이면 True. 질의마다 O(1) 로 답할 수 있다."""
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            if s[l] == s[r] and (length <= 2 or is_pal[l + 1][r - 1]):
                is_pal[l][r] = True
    return is_pal


def burst_balloons(nums: list[int]) -> int:
    """풍선을 하나씩 터뜨릴 때 i 번째를 터뜨리면 (왼쪽 이웃) × nums[i] × (오른쪽 이웃) 코인을 얻는다. 끝 밖은 1. 코인 합의 최댓값.

    "마지막에 터뜨릴 풍선" 을 기준으로 구간을 나누는 것이 핵심이다. 마지막 풍선 k 의 이웃은 구간의 양 끝 밖 풍선이라서 정해진다.
    dp[l][r] = max over k in (l, r) (dp[l][k] + dp[k][r] + a[l]·a[k]·a[r]), 양 끝에 1 을 붙인 배열 a 의 열린 구간."""
    a = [1] + list(nums) + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(n - length):
            r = l + length
            best = 0
            for k in range(l + 1, r):
                best = max(best, dp[l][k] + dp[k][r] + a[l] * a[k] * a[r])
            dp[l][r] = best
    return dp[0][n - 1]


def main() -> None:
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        k = int(input())
        sizes = list(map(int, input().split()))[:k]
        out.append(str(min_merge_cost(sizes)))
    print("\n".join(out))


if __name__ == "__main__":
    main()
