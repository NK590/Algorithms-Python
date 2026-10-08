"""문자열 기초 — 문자의 나열을 인덱스로 다루기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 파이썬 문자열은 바꿀 수 없는(immutable) 값입니다. 일부를 바꾸려면 새 문자열을 만들어야 합니다.
- 직접 실행하면 한 줄의 문자열을 받아 팰린드롬이면 1, 아니면 0 을 출력합니다.
"""
import sys


def is_palindrome(s: str) -> bool:
    """앞에서 읽으나 뒤에서 읽으나 같은 문자열인지. 양 끝에서 안쪽으로 한 쌍씩 비교한다."""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def char_counts(s: str) -> dict:
    """문자별 등장 횟수 (처음 나온 순서가 유지되는 딕셔너리)."""
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return counts


def reverse_words(sentence: str) -> str:
    """공백으로 구분된 단어의 순서를 뒤집는다. 연속된 공백은 하나로 합쳐진다."""
    return " ".join(reversed(sentence.split()))


def caesar_shift(s: str, k: int) -> str:
    """알파벳을 k칸씩 밀어 암호화한다. 대소문자는 유지하고 알파벳이 아닌 문자는 그대로 둔다."""
    result = []
    for ch in s:
        if "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + k) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + k) % 26 + ord("A")))
        else:
            result.append(ch)
    return "".join(result)  # 문자열을 += 로 계속 이어 붙이지 말고 리스트에 모아 한 번에 합친다


def is_anagram(a: str, b: str) -> bool:
    """두 문자열이 같은 문자들을 같은 개수만큼 가지고 있는지 (순서는 무관)."""
    return char_counts(a) == char_counts(b)


def main() -> None:
    word = sys.stdin.readline().rstrip("\n")
    print(1 if is_palindrome(word) else 0)


if __name__ == "__main__":
    main()
