"""문자열 처리 — 문자열을 한 글자씩 훑으며 쪼개고, 세고, 바꾸기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 내장 메서드(split, join, replace)로 되는 것은 내장을 쓰고, 그렇지 않은 규칙은 직접 훑어서 처리합니다.
- 직접 실행하면 한 줄을 받아 크로아티아 알파벳으로 몇 글자인지 출력합니다.
"""
import sys

CROATIAN = ["c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="]


def run_length_encode(s: str) -> str:
    """같은 글자가 연속된 구간을 `글자 + 개수` 로 줄인다. aaabcc → a3b1c2"""
    if not s:
        return ""
    pieces = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            pieces.append(f"{s[i - 1]}{count}")
            count = 1
    pieces.append(f"{s[-1]}{count}")  # 마지막 구간은 반복문 안에서 닫히지 않으므로 따로 처리한다
    return "".join(pieces)


def run_length_decode(encoded: str) -> str:
    """run_length_encode 의 반대. 개수는 여러 자리 숫자일 수 있다."""
    pieces = []
    i = 0
    while i < len(encoded):
        ch = encoded[i]
        i += 1
        start = i
        while i < len(encoded) and encoded[i].isdigit():
            i += 1
        pieces.append(ch * int(encoded[start:i]))
    return "".join(pieces)


def longest_common_prefix(words: list) -> str:
    """모든 문자열이 공통으로 시작하는 가장 긴 접두사."""
    if not words:
        return ""
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]  # 맞을 때까지 한 글자씩 줄인다 (빈 문자열은 항상 접두사다)
    return prefix


def count_words(s: str) -> int:
    """공백으로 구분된 단어의 수. 앞뒤·연속 공백이 있어도 단어 경계(공백 → 글자)를 세면 된다."""
    count = 0
    in_word = False
    for ch in s:
        if ch != " " and not in_word:
            count += 1
        in_word = ch != " "
    return count


def split_by(s: str, sep: str) -> list:
    """s.split(sep) 와 같은 결과를 직접 만든다. sep 는 한 글자 이상의 비어 있지 않은 문자열."""
    parts = []
    start = 0
    i = 0
    while i <= len(s) - len(sep):
        if s[i:i + len(sep)] == sep:
            parts.append(s[start:i])
            i += len(sep)
            start = i
        else:
            i += 1
    parts.append(s[start:])
    return parts


def count_croatian(s: str) -> int:
    """크로아티아 알파벳(c=, c-, dz=, d-, lj, nj, s=, z=)을 한 글자로 세었을 때의 글자 수. 긴 것부터 맞춰 본다."""
    count = 0
    i = 0
    while i < len(s):
        for pattern in ("dz=",) + tuple(p for p in CROATIAN if len(p) == 2):  # 3글자를 먼저 확인한다
            if s.startswith(pattern, i):
                i += len(pattern)
                break
        else:
            i += 1
        count += 1
    return count


def main() -> None:
    print(count_croatian(sys.stdin.readline().strip()))


if __name__ == "__main__":
    main()
