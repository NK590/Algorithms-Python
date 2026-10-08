"""KMP 알고리즘 — 불일치가 났을 때 이미 맞춘 부분을 활용해 패턴을 건너뛰며 O(n + m) 에 문자열을 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 실패 함수(접두사 함수) failure[i] = pattern[: i + 1] 의 "접두사이면서 접미사인 가장 긴 부분 문자열(자기 자신 제외)" 의 길이.
- 본문을 한 번 훑으며 패턴과 맞춘 길이 k 를 유지하고, 불일치가 나면 k 를 failure[k - 1] 로 줄여서 다시 비교합니다. 본문 위치는 되돌아가지 않습니다.
- 겹치는 등장도 모두 찾습니다. 위치는 0 부터입니다.
- 직접 실행하면 두 줄(본문 T, 패턴 P)을 받아 등장 횟수와 시작 위치(1 부터)를 출력합니다. 공백이 포함될 수 있습니다.
"""
import sys


def failure_function(pattern: str) -> list[int]:
    """failure[i] = pattern[: i + 1] 에서 접두사이자 접미사인 가장 긴 (자기 자신이 아닌) 부분 문자열의 길이. 패턴 자신을 본문으로 삼아 KMP 처럼 채운다."""
    failure = [0] * len(pattern)
    k = 0  # 지금까지 맞춘 접두사의 길이
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = failure[k - 1]  # 불일치: 더 짧은 접두사로 후퇴
        if pattern[i] == pattern[k]:
            k += 1
        failure[i] = k
    return failure


def kmp_search(text: str, pattern: str) -> list[int]:
    """text 에서 pattern 이 시작하는 모든 위치(0 부터, 겹쳐도 포함). 빈 패턴은 빈 리스트."""
    if not pattern:
        return []
    failure = failure_function(pattern)
    positions = []
    k = 0
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            k = failure[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            positions.append(i - k + 1)
            k = failure[k - 1]  # 겹치는 다음 등장을 위해 후퇴
    return positions


def count_occurrences(text: str, pattern: str) -> int:
    return len(kmp_search(text, pattern))


def smallest_period(s: str) -> int:
    """s 가 어떤 문자열을 반복해서 만들어지는 가장 짧은 반복 단위의 길이. 반복이 아니면 len(s).

    n - failure[n-1] 이 후보 단위이고, 그 길이가 n 을 나누어떨어뜨릴 때만 s 전체가 그 단위의 반복이다."""
    n = len(s)
    if n == 0:
        return 0
    unit = n - failure_function(s)[-1]
    return unit if n % unit == 0 else n


def shortest_prefix_covering(s: str) -> int:
    """s 의 어떤 접두사를 (겹쳐서도) 이어 붙여 s 가 부분 문자열로 나오는 가장 짧은 길이 = n - failure[n-1]. 반복 단위를 겹쳐도 되는 경우의 '광고' 문제."""
    if not s:
        return 0
    return len(s) - failure_function(s)[-1]


def main() -> None:
    text = sys.stdin.readline().rstrip("\n")
    pattern = sys.stdin.readline().rstrip("\n")
    positions = kmp_search(text, pattern)
    print(len(positions))
    print(" ".join(str(p + 1) for p in positions))


if __name__ == "__main__":
    main()
