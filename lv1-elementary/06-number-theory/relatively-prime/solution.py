"""서로소 — 공약수가 1 뿐인 두 수

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- a 와 b 가 서로소 ⇔ gcd(a, b) = 1 ⇔ lcm(a, b) = a × b.
- 직접 실행하면 두 분수 `a b` `c d` 를 받아 합을 기약분수로 출력합니다.
"""
import sys


def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)


def is_coprime(a: int, b: int) -> bool:
    """서로소인지. 최대공약수가 1 이면 서로소다."""
    return gcd(a, b) == 1


def coprimes_up_to(limit: int, m: int) -> list:
    """1 이상 limit 이하의 수 중 m 과 서로소인 것들."""
    return [k for k in range(1, limit + 1) if is_coprime(k, m)]


def reduce_fraction(numerator: int, denominator: int) -> tuple:
    """분자와 분모를 최대공약수로 나눠 기약분수로 만든다. 부호는 분자에 둔다."""
    if denominator == 0:
        raise ZeroDivisionError("분모가 0 입니다")
    g = gcd(numerator, denominator)
    numerator, denominator = numerator // g, denominator // g
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    return numerator, denominator


def add_fractions(a: tuple, b: tuple) -> tuple:
    """두 분수의 합을 기약분수로. 분모를 곱해 통분한 뒤 약분한다."""
    return reduce_fraction(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def pairwise_coprime(numbers: list) -> bool:
    """어느 두 수를 골라도 서로소인지. (전체의 gcd 가 1 이라고 해서 쌍마다 서로소인 것은 아니다: 6, 10, 15)"""
    return all(is_coprime(numbers[i], numbers[j]) for i in range(len(numbers)) for j in range(i + 1, len(numbers)))


def main() -> None:
    input = sys.stdin.readline
    a, b = map(int, input().split())
    c, d = map(int, input().split())
    print(*add_fractions((a, b), (c, d)))


if __name__ == "__main__":
    main()
