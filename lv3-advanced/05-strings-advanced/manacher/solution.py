"""매내처 알고리즘(Manacher) — 문자열의 모든 중심에서 가장 긴 회문의 반지름을 O(n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- odd[i] = i 를 한가운데로 하는 홀수 길이 회문의 개수(= 반지름, 자기 자신 포함). 가장 긴 홀수 회문의 길이는 2·odd[i] - 1.
  even[i] = i 를 오른쪽 가운데로 하는 짝수 길이 회문의 개수(= 반지름). 가장 긴 짝수 회문의 길이는 2·even[i] (s[i-1] == s[i] 가 아니면 0).
- 지금까지 찾은 가장 오른쪽까지 간 회문 [l, r] 의 대칭성을 이용해, 새 중심 i 의 반지름을 이미 계산한 거울 위치의 값에서 시작합니다.
  경계 밖으로 나갈 때만 한 글자씩 넓히므로 전체 O(n).
- 응용: 가장 긴 회문 부분 문자열, 회문 부분 문자열의 개수, 구간 [l, r] 이 회문인지 O(1) 질의, 가장 짧게 회문으로 쪼개기(DP).
- 입력은 문자열 또는 리스트. 직접 실행하면 문자열 하나를 받아 가장 긴 회문 부분 문자열의 길이를 출력합니다.
"""
import sys
from typing import Sequence


def manacher(s: Sequence) -> tuple[list[int], list[int]]:
    """(odd, even). odd[i]: i 가 한가운데인 홀수 회문의 개수, even[i]: s[i-1], s[i] 사이가 한가운데인 짝수 회문의 개수 (even[0] = 0)."""
    n = len(s)
    odd = [0] * n
    left, right = 0, -1  # 가장 오른쪽까지 간 홀수 회문의 구간 [left, right]
    for i in range(n):
        k = 1 if i > right else min(odd[left + right - i], right - i + 1)  # 거울 위치의 값에서 시작
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        odd[i] = k
        if i + k - 1 > right:
            left, right = i - k + 1, i + k - 1
    even = [0] * n
    left, right = 0, -1
    for i in range(n):
        k = 0 if i > right else min(even[left + right - i + 1], right - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        even[i] = k
        if i + k - 1 > right:
            left, right = i - k, i + k - 1
    return odd, even


def longest_palindromic_substring(s: str) -> str:
    """가장 긴 회문 부분 문자열 (같은 길이면 가장 앞). 빈 문자열이면 빈 문자열."""
    odd, even = manacher(s)
    best_len, best_start = 0, 0
    for i in range(len(s)):
        if 2 * odd[i] - 1 > best_len:
            best_len, best_start = 2 * odd[i] - 1, i - odd[i] + 1
        if 2 * even[i] > best_len:
            best_len, best_start = 2 * even[i], i - even[i]
    return s[best_start : best_start + best_len]


def count_palindromic_substrings(s: Sequence) -> int:
    """회문인 부분 문자열의 개수 (위치가 다르면 내용이 같아도 따로 센다). 중심마다 반지름만큼의 회문이 있으므로 odd 와 even 의 합."""
    odd, even = manacher(s)
    return sum(odd) + sum(even)


class PalindromeChecker:
    """구간 s[l:r] 이 회문인지 O(1) 에 답하는 질의 구조 (전처리 O(n))."""

    def __init__(self, s: Sequence):
        self.n = len(s)
        self.odd, self.even = manacher(s)

    def is_palindrome(self, left: int, right: int) -> bool:
        """s[left:right] (반열린) 이 회문인가. 빈 구간과 길이 1 은 회문."""
        length = right - left
        if length <= 1:
            return True
        if length % 2:
            center = left + length // 2
            return self.odd[center] >= length // 2 + 1
        center = left + length // 2
        return self.even[center] >= length // 2


def min_palindrome_cuts(s: str) -> int:
    """문자열을 회문 조각으로 나눌 때 필요한 최소 자르는 횟수 (O(n²), 회문 판정은 O(1))."""
    n = len(s)
    if n == 0:
        return 0
    checker = PalindromeChecker(s)
    cuts = [0] * (n + 1)  # cuts[i] = 앞의 i 글자를 나누는 최소 자르는 횟수
    for i in range(1, n + 1):
        cuts[i] = min(cuts[j] + 1 for j in range(i) if checker.is_palindrome(j, i))
    return cuts[n] - 1


def main() -> None:
    s = sys.stdin.readline().strip()
    print(len(longest_palindromic_substring(s)))


if __name__ == "__main__":
    main()
