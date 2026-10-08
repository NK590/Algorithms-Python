"""LCS (최장 공통 부분 수열) 와 편집 거리 — 두 문자열을 2 차원 표로 비교하는 DP

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- dp[i][j] = a 의 앞 i 글자와 b 의 앞 j 글자만 봤을 때의 답. 마지막 글자 a[i-1], b[j-1] 가 같은지에 따라 경우를 나눕니다.
- 부분 수열(subsequence)은 순서만 유지하면 되고 연속하지 않아도 되지만, 부분 문자열(substring)은 연속해야 합니다.
- 직접 실행하면 두 줄의 문자열을 받아 LCS 의 길이를 출력합니다.
"""
import sys


def lcs_table(a: str, b: str) -> list[list[int]]:
    """dp[i][j] = a[:i] 와 b[:j] 의 LCS 길이."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1  # 마지막 글자가 같으면 둘 다 하나씩 줄이고 +1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # 다르면 한쪽을 줄인 것 중 큰 쪽
    return dp


def lcs_length(a: str, b: str) -> int:
    """LCS 의 길이. 이전 행만 필요하므로 길이가 짧은 쪽을 열로 두어 공간 O(min(n, m)) 으로 줄인다."""
    if len(b) > len(a):
        a, b = b, a
    previous = [0] * (len(b) + 1)
    for ch in a:
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if ch == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def lcs_string(a: str, b: str) -> str:
    """LCS 하나를 복원한다. 표의 오른쪽 아래에서 시작해, 글자가 같으면 포함하고 대각선으로, 다르면 값이 큰 쪽으로 이동한다."""
    dp = lcs_table(a, b)
    i, j = len(a), len(b)
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))


def edit_distance(a: str, b: str) -> int:
    """편집 거리(레벤슈타인): 한 글자 삽입·삭제·교체를 최소 몇 번 해야 a 가 b 가 되는가.

    dp[i][j] = a[:i] 를 b[:j] 로 바꾸는 최소 횟수. 글자가 같으면 dp[i-1][j-1], 다르면 교체/삭제/삽입 중 최소 + 1."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        dp[i][0] = i  # a[:i] 를 빈 문자열로: i 번 삭제
    for j in range(len(b) + 1):
        dp[0][j] = j  # 빈 문자열을 b[:j] 로: j 번 삽입
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


def longest_common_substring(a: str, b: str) -> tuple[int, str]:
    """연속한 공통 부분 문자열 중 가장 긴 것의 (길이, 문자열). dp[i][j] = a[i-1], b[j-1] 로 끝나는 공통 부분 문자열의 길이."""
    best_len, best_end = 0, 0
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1  # 같은 글자가 이어진 만큼만 늘어난다 (다르면 0 으로 끊긴다)
                if current[j] > best_len:
                    best_len, best_end = current[j], i
        previous = current
    return best_len, a[best_end - best_len : best_end]


def shortest_common_supersequence(a: str, b: str) -> str:
    """a 와 b 를 모두 부분 수열로 포함하는 가장 짧은 문자열. 길이는 len(a) + len(b) - LCS."""
    dp = lcs_table(a, b)
    i, j = len(a), len(b)
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            chars.append(a[i - 1])
            i -= 1
        else:
            chars.append(b[j - 1])
            j -= 1
    while i > 0:
        chars.append(a[i - 1])
        i -= 1
    while j > 0:
        chars.append(b[j - 1])
        j -= 1
    return "".join(reversed(chars))


def main() -> None:
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()
    print(lcs_length(a, b))


if __name__ == "__main__":
    main()
