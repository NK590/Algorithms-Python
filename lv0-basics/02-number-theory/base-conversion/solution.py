"""진법 변환 — 같은 수를 2진법, 8진법, 16진법 … 로 적기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- b 진법에서는 자릿수마다 b 의 거듭제곱이 곱해집니다. 10 이상의 숫자는 A=10, B=11, … Z=35 로 적습니다.
- 직접 실행하면 `수 진법` 을 받아, 그 진법으로 적은 수를 10진수로 바꿔 출력합니다. (예: `ZZZZZ 36`)
"""
import sys

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base(n: int, base: int) -> str:
    """10진수 n 을 base 진법(2 ~ 36) 문자열로 바꾼다. 몫이 0 이 될 때까지 base 로 나눈 나머지를 모아 뒤집는다."""
    if not 2 <= base <= 36:
        raise ValueError("진법은 2 이상 36 이하여야 합니다")
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    digits = []
    while n > 0:
        n, remainder = divmod(n, base)
        digits.append(DIGITS[remainder])  # 나머지가 가장 낮은 자리부터 나온다
    return sign + "".join(reversed(digits))


def from_base(text: str, base: int) -> int:
    """base 진법 문자열을 10진수로 바꾼다. 앞자리부터 읽으면서 (지금까지의 값 × base + 새 자리) 를 반복한다."""
    if not 2 <= base <= 36:
        raise ValueError("진법은 2 이상 36 이하여야 합니다")
    negative = text.startswith("-")
    value = 0
    for ch in text.lstrip("-").upper():
        digit = DIGITS.index(ch)
        if digit >= base:
            raise ValueError(f"{ch!r} 는 {base} 진법의 숫자가 아닙니다")
        value = value * base + digit
    return -value if negative else value


def to_negative_base(n: int, base: int) -> str:
    """10진수 n 을 음수 진법(-2, -3, ...) 문자열로 바꾼다. 나머지가 음수가 되지 않게 몫을 한 칸 올려 준다."""
    if base > -2:
        raise ValueError("base 는 -2 이하여야 합니다")
    if n == 0:
        return "0"
    digits = []
    while n != 0:
        n, remainder = divmod(n, base)  # base < 0 이면 파이썬의 나머지는 (base, 0] 범위라 음수가 될 수 있다
        if remainder < 0:  # n = q*base + r 에서 r 을 0 이상으로 만들려면 r - base 를 쓰고 몫을 1 올린다
            remainder -= base
            n += 1
        digits.append(DIGITS[remainder])
    return "".join(reversed(digits))


def main() -> None:
    text, base = sys.stdin.readline().split()
    print(from_base(text, int(base)))


if __name__ == "__main__":
    main()
