"""나머지 연산 — 큰 수를 직접 다루지 않고 나머지만 가지고 계산하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 덧셈·뺄셈·곱셈은 중간마다 나머지를 취해도 최종 나머지가 같습니다.
    (a + b) % m == ((a % m) + (b % m)) % m,   (a * b) % m == ((a % m) * (b % m)) % m
- 나눗셈은 이 성질이 성립하지 않습니다. (모듈러 역원이 필요합니다. Lv2 에서 다룹니다)
- 직접 실행하면 `A B C` 를 받아 (A+B)%C, ((A%C)+(B%C))%C, (A*B)%C, ((A%C)*(B%C))%C 를 한 줄씩 출력합니다.
"""
import sys


def add_mod(a: int, b: int, m: int) -> int:
    return (a % m + b % m) % m


def sub_mod(a: int, b: int, m: int) -> int:
    """뺄셈은 음수가 나올 수 있다. 파이썬의 % 는 항상 0 이상이지만, C/C++/Java 는 음수가 나오므로 + m 으로 보정하는 습관이 필요하다."""
    return (a % m - b % m + m) % m


def mul_mod(a: int, b: int, m: int) -> int:
    return (a % m) * (b % m) % m


def factorial_mod(n: int, m: int) -> int:
    """n! % m. 중간마다 나머지를 취하면 값이 m 보다 커지지 않는다."""
    result = 1 % m
    for i in range(2, n + 1):
        result = result * i % m
    return result


def fibonacci_mod(n: int, m: int) -> int:
    """n 번째 피보나치 수 (F0 = 0, F1 = 1) 를 m 으로 나눈 나머지. 큰 수를 만들지 않고 O(n)."""
    a, b = 0, 1 % m
    for _ in range(n):
        a, b = b, (a + b) % m
    return a


def power_mod_slow(a: int, b: int, m: int) -> int:
    """a^b % m 을 b 번 곱해서 구한다. O(b). b 가 크면 쓸 수 없다. (빠른 방법은 Lv2 의 빠른 거듭제곱)"""
    result = 1 % m
    for _ in range(b):
        result = result * a % m
    return result


def main() -> None:
    a, b, c = map(int, sys.stdin.readline().split())
    print((a + b) % c)
    print((a % c + b % c) % c)
    print((a * b) % c)
    print((a % c) * (b % c) % c)


if __name__ == "__main__":
    main()
