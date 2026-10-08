"""라빈-카프 알고리즘 — 문자열을 해시 값으로 바꿔 O(1) 에 비교하고, 한 칸 밀 때 해시를 O(1) 에 갱신(롤링 해시)하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 다항 해시: H(s) = (s[0]·B^(L-1) + s[1]·B^(L-2) + … + s[L-1]) mod M.  한 칸 밀면 앞 글자를 빼고 뒤 글자를 붙여 O(1) 에 갱신합니다.
- 해시가 같다고 문자열이 같은 것은 아니므로(충돌), 해시가 같을 때는 실제 문자열을 비교해 확인합니다. 이 구현의 검색은 항상 정확합니다.
- 접두사 해시를 미리 구해 두면 부분 문자열의 해시를 O(1) 에 얻을 수 있어, 반복 부분 문자열 같은 문제를 이분 탐색과 함께 풉니다.
- 직접 실행하면 두 줄(본문 T, 패턴 P)을 받아 P 가 T 의 부분 문자열로 나오는 횟수를 출력합니다.
"""
import sys

BASE = 257
MOD = (1 << 61) - 1  # 큰 소수: 충돌 확률이 매우 낮다


def polynomial_hash(s: str, base: int = BASE, mod: int = MOD) -> int:
    value = 0
    for ch in s:
        value = (value * base + ord(ch)) % mod
    return value


def rabin_karp(text: str, pattern: str, base: int = BASE, mod: int = MOD) -> list[int]:
    """text 에서 pattern 이 시작하는 모든 위치(0 부터). 해시가 같으면 실제 문자열을 비교하므로 mod 가 작아도 결과가 정확하다(느려질 뿐)."""
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    high = pow(base, m - 1, mod)  # 맨 앞 글자의 자릿수 B^(m-1)
    target = polynomial_hash(pattern, base, mod)
    window = polynomial_hash(text[:m], base, mod)
    positions = []
    for i in range(n - m + 1):
        if window == target and text[i : i + m] == pattern:
            positions.append(i)
        if i + m < n:  # 창을 한 칸 민다: 앞 글자를 빼고 뒤 글자를 붙인다
            window = ((window - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return positions


class PrefixHash:
    """접두사 해시: prefix[i] = H(s[:i]). 부분 문자열 s[l:r] 의 해시를 O(1) 에 구한다."""

    def __init__(self, s: str, base: int = BASE, mod: int = MOD):
        self.mod = mod
        self.prefix = [0] * (len(s) + 1)
        self.power = [1] * (len(s) + 1)
        for i, ch in enumerate(s):
            self.prefix[i + 1] = (self.prefix[i] * base + ord(ch)) % mod
            self.power[i + 1] = self.power[i] * base % mod

    def substring_hash(self, left: int, right: int) -> int:
        """s[left:right] 의 해시 (right 는 포함하지 않음)."""
        return (self.prefix[right] - self.prefix[left] * self.power[right - left]) % self.mod


def has_repeated_substring(s: str, length: int, base: int = BASE, mod: int = MOD) -> bool:
    """길이 length 인 부분 문자열이 두 번 이상(겹쳐도) 나오는가. 해시를 집합에 넣고, 같은 해시가 나오면 실제 문자열로 확인한다."""
    if length <= 0 or length > len(s):
        return False
    hashes = PrefixHash(s, base, mod)
    seen: dict[int, list[int]] = {}
    for i in range(len(s) - length + 1):
        h = hashes.substring_hash(i, i + length)
        for j in seen.get(h, []):
            if s[j : j + length] == s[i : i + length]:
                return True
        seen.setdefault(h, []).append(i)
    return False


def longest_repeated_substring_length(s: str, base: int = BASE, mod: int = MOD) -> int:
    """두 번 이상 나오는 가장 긴 부분 문자열의 길이 (겹쳐도 됨). 길이 L 이 가능하면 L-1 도 가능하므로 L 을 이분 탐색한다. O(n log n)."""
    lo, hi = 0, len(s) - 1  # 가능한 최대 길이
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if has_repeated_substring(s, mid, base, mod):
            lo = mid
        else:
            hi = mid - 1
    return lo


def main() -> None:
    text = sys.stdin.readline().rstrip("\n")
    pattern = sys.stdin.readline().rstrip("\n")
    print(len(rabin_karp(text, pattern)))


if __name__ == "__main__":
    main()
