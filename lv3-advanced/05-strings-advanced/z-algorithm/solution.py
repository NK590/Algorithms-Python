"""Z 알고리즘 — 문자열의 모든 위치에서 "문자열 전체의 접두사와 얼마나 길게 일치하는가" 를 O(n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- z[i] = s[i:] 와 s 의 최장 공통 접두사의 길이 (z[0] 은 관례상 n). 지금까지 찾은 가장 오른쪽 일치 구간 [l, r) 을 기억해 두고,
  새 위치 i 가 그 안에 있으면 z[i - l] 을 재활용합니다. 구간 밖으로 나갈 때만 직접 비교하므로 비교는 총 O(n) 번.
- 응용: 문자열 찾기(패턴 + 구분자 + 본문), 최소 주기·모든 테두리(border), 각 접두사가 본문에 몇 번 나오는가.
- 입력은 문자열뿐 아니라 리스트(원소를 비교할 수 있으면 무엇이든)도 됩니다. 구분자가 필요한 곳은 `None` 을 씁니다.
- 직접 실행하면 두 줄(본문 T, 패턴 P)을 받아 P 가 T 에서 시작하는 위치의 수와 위치(1 부터)를 출력합니다.
"""
import sys
from typing import Sequence


def z_function(s: Sequence) -> list[int]:
    """z[i] = lcp(s, s[i:]). z[0] = len(s)."""
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    left = right = 0  # s[left:right] 가 s 의 접두사 s[0:right-left] 와 같은, 가장 오른쪽까지 간 구간
    for i in range(1, n):
        if i < right:
            z[i] = min(right - i, z[i - left])  # 이미 알고 있는 일치를 재활용
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def z_search(text: Sequence, pattern: Sequence) -> list[int]:
    """text 에서 pattern 이 시작하는 모든 위치(0 부터, 겹쳐도 포함). 패턴 + 구분자 + 본문의 Z 배열에서 z 값이 len(pattern) 인 곳."""
    m = len(pattern)
    if m == 0:
        return []
    combined = list(pattern) + [None] + list(text)  # None 은 어떤 문자와도 같지 않다
    z = z_function(combined)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]


def smallest_period(s: Sequence) -> int:
    """s 가 어떤 문자열 u 를 반복해(마지막은 일부만 써도 됨) 만들어지는 가장 짧은 길이. 반복이 없으면 len(s). z[p] == n - p 인 가장 작은 p."""
    n = len(s)
    z = z_function(s)
    for p in range(1, n):
        if z[p] == n - p:
            return p
    return n


def all_borders(s: Sequence) -> list[int]:
    """접두사이면서 접미사인 (s 자신이 아닌) 부분 문자열의 길이들, 오름차순. 길이 k 가 테두리 ⟺ z[n - k] == k."""
    n = len(s)
    z = z_function(s)
    return [k for k in range(1, n) if z[n - k] == k]


def prefix_occurrence_counts(s: Sequence) -> list[int]:
    """result[k] = 길이 k 인 접두사가 s 안에 (겹쳐도) 나오는 횟수 (k = 1..n, result[0] 은 0). z[i] ≥ k 인 위치 i 의 개수를 차분으로 센다."""
    n = len(s)
    z = z_function(s)
    exact = [0] * (n + 2)  # exact[v] = z 값이 정확히 v 인 위치 수
    for value in z:
        exact[value] += 1
    counts = [0] * (n + 1)
    running = 0
    for k in range(n, 0, -1):
        running += exact[k]  # z[i] ≥ k 인 위치 수
        counts[k] = running
    return counts


def main() -> None:
    text = sys.stdin.readline().rstrip("\n")
    pattern = sys.stdin.readline().rstrip("\n")
    positions = z_search(text, pattern)
    print(len(positions))
    print(" ".join(str(p + 1) for p in positions))


if __name__ == "__main__":
    main()
