"""접미사 배열(Suffix Array)과 LCP 배열 — 문자열의 모든 접미사를 사전순으로 정렬하고, 이웃한 접미사의 공통 접두사 길이를 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- suffix_array(s): sa[i] = 사전순으로 i 번째인 접미사의 시작 위치. 접두사 배가법: 길이 1, 2, 4, … 의 접두사 순위를 이용해
  (앞 절반의 순위, 뒤 절반의 순위) 쌍을 키로 정렬합니다. 길이가 2^k 인 접두사로 모든 접미사가 구별되면 끝. O(n log² n) (정렬이 C 로 구현되어 실제로는 빠름).
- lcp_array(s, sa): 카사이(Kasai) 알고리즘. lcp[i] = sa[i-1] 과 sa[i] 가 시작하는 접미사의 최장 공통 접두사 길이 (lcp[0] = 0).
  접미사 i 를 순위 순으로 보지 않고 위치 순으로 보면서, 다음 위치의 lcp 가 최소 h - 1 임을 이용해 h 를 한 번에 1 만 줄입니다. O(n).
- 응용: 서로 다른 부분 문자열의 수, 가장 긴 반복 부분 문자열, 두 문자열의 가장 긴 공통 부분 문자열, 패턴 위치 찾기(이진 탐색), 임의의 두 접미사의 lcp(희소 배열).
- 입력은 문자열 또는 정수 리스트. 직접 실행하면 문자열 하나를 받아 접미사 배열(1 부터)과, 첫 칸이 `x` 인 LCP 배열을 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right
from typing import Sequence


def _compress(s: Sequence) -> list[int]:
    values = sorted(set(s))
    index = {v: i for i, v in enumerate(values)}
    return [index[c] for c in s]


def suffix_array(s: Sequence) -> list[int]:
    n = len(s)
    if n == 0:
        return []
    rank = _compress(s)
    sa = list(range(n))
    k = 1
    while True:
        base = n + 1
        key = [rank[i] * base + (rank[i + k] + 1 if i + k < n else 0) for i in range(n)]  # (앞 절반 순위, 뒤 절반 순위) 를 정수 하나로
        sa.sort(key=key.__getitem__)
        new_rank = [0] * n
        for position in range(1, n):
            new_rank[sa[position]] = new_rank[sa[position - 1]] + (key[sa[position]] != key[sa[position - 1]])
        rank = new_rank
        if rank[sa[-1]] == n - 1:  # 모든 접미사의 순위가 달라졌다
            return sa
        k *= 2


def lcp_array(s: Sequence, sa: list[int]) -> list[int]:
    """lcp[i] = lcp(s[sa[i-1]:], s[sa[i]:]), lcp[0] = 0."""
    n = len(s)
    rank = [0] * n
    for position, start in enumerate(sa):
        rank[start] = position
    lcp = [0] * n
    h = 0
    for i in range(n):  # 접미사를 위치 순으로 본다
        if rank[i] > 0:  # rank[i] == 0 (사전순 첫 접미사) 이면 앞 접미사가 없고, 이때 h 는 이미 0 이다
            j = sa[rank[i] - 1]  # 사전순으로 바로 앞 접미사
            while j + h < n and s[i + h] == s[j + h]:  # j 가 사전순으로 앞이므로 j + h < n 이면 i + h < n 도 보장된다
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1  # 다음 위치의 lcp 는 적어도 h - 1
    return lcp


def count_distinct_substrings(s: Sequence) -> int:
    """서로 다른 (비어 있지 않은) 부분 문자열의 수 = 모든 접두사의 수 n(n+1)/2 - Σ lcp (이웃한 접미사가 공유하는 접두사는 이미 센 것)."""
    n = len(s)
    return n * (n + 1) // 2 - sum(lcp_array(s, suffix_array(s)))


def longest_repeated_substring(s: str) -> str:
    """두 번 이상(겹쳐도) 나오는 가장 긴 부분 문자열 (같은 길이면 사전순으로 가장 앞). 없으면 빈 문자열."""
    if not s:
        return ""
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    best = max(range(len(s)), key=lambda i: (lcp[i], -i))
    return s[sa[best] : sa[best] + lcp[best]]


def longest_common_substring(a: str, b: str) -> str:
    """두 문자열의 가장 긴 공통 부분 문자열 (같은 길이면 사전순으로 가장 앞). a, b 사이에 어떤 글자보다도 작은 구분자를 끼워 하나로 합친다."""
    combined = [c + 1 for c in map(ord, a)] + [0] + [c + 1 for c in map(ord, b)]  # 0 은 한 번만 나오는 구분자
    sa = suffix_array(combined)
    lcp = lcp_array(combined, sa)
    boundary = len(a)  # 이 위치보다 앞에서 시작하는 접미사는 a 에서, 뒤에서 시작하는 접미사는 b 에서 온 것
    best_len, best_start = 0, 0
    for i in range(1, len(sa)):
        x, y = sa[i - 1], sa[i]
        if (x < boundary) != (y < boundary) and lcp[i] > best_len:  # 서로 다른 문자열에서 온 이웃. 구분자 때문에 공통 접두사가 경계를 넘지 않는다
            best_len, best_start = lcp[i], min(x, y)
    return a[best_start : best_start + best_len]


def find_occurrences(s: str, sa: list[int], pattern: str) -> list[int]:
    """pattern 이 s 에서 시작하는 모든 위치(오름차순). 접미사를 pattern 길이로 자른 것은 sa 순서에서도 정렬되어 있으므로,
    pattern 과 같은 것들의 구간 [low, high) 을 이진 탐색 두 번으로 찾는다. O(m log n)."""
    if not pattern:
        return []
    m = len(pattern)
    low = bisect_left(sa, pattern, key=lambda i: s[i : i + m])
    high = bisect_right(sa, pattern, key=lambda i: s[i : i + m])
    return sorted(sa[low:high])


class LcpQuery:
    """임의의 두 접미사의 최장 공통 접두사를 O(1) 에 답한다: 두 접미사의 순위 사이 구간에서 lcp 배열의 최솟값 (희소 배열)."""

    def __init__(self, s: Sequence):
        self.n = len(s)
        self.sa = suffix_array(s)
        self.lcp = lcp_array(s, self.sa)
        self.rank = [0] * self.n
        for position, start in enumerate(self.sa):
            self.rank[start] = position
        self.table = [self.lcp]
        k = 1
        while (1 << k) <= self.n:
            previous = self.table[-1]
            half = 1 << (k - 1)
            self.table.append([min(previous[i], previous[i + half]) for i in range(self.n - (1 << k) + 1)])
            k += 1

    def lcp_of_suffixes(self, i: int, j: int) -> int:
        """s[i:] 와 s[j:] 의 최장 공통 접두사의 길이."""
        if i == j:
            return self.n - i
        a, b = sorted((self.rank[i], self.rank[j]))
        left, right = a + 1, b  # lcp[left..right] 의 최솟값
        k = (right - left + 1).bit_length() - 1
        return min(self.table[k][left], self.table[k][right - (1 << k) + 1])


def main() -> None:
    s = sys.stdin.readline().strip()
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    print(" ".join(str(i + 1) for i in sa))
    print(" ".join(["x"] + [str(v) for v in lcp[1:]]))


if __name__ == "__main__":
    main()
