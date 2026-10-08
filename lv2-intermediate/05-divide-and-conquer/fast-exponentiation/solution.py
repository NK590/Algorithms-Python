"""빠른 거듭제곱 — a^b 를 b 를 반으로 줄이며 O(log b) 번의 곱셈으로 계산하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 핵심 식: a^b = (a^(b/2))² (b 가 짝수),  a^b = (a^(b/2))² · a (b 가 홀수). b 를 이진수로 보면 켜진 비트에 해당하는 a^(2^i) 만 곱하는 것과 같습니다.
- 나머지 연산이 있는 `a^b mod m` 은 곱할 때마다 나머지를 구해 수가 커지지 않게 합니다.
- 같은 틀을 수 대신 행렬에 적용하면 점화식(피보나치 등)의 n 번째 항을 O(log n) 에 구합니다. → 행렬 거듭제곱(Lv3)
- 직접 실행하면 `A B C` 를 받아 A 를 B 번 곱한 수를 C 로 나눈 나머지를 출력합니다.
"""
import sys


def power(a: int, b: int) -> int:
    """a^b (b ≥ 0) 을 재귀로. 깊이는 log₂ b."""
    if b == 0:
        return 1
    half = power(a, b // 2)
    return half * half * a if b % 2 else half * half


def power_mod(a: int, b: int, m: int) -> int:
    """a^b mod m (b ≥ 0, m ≥ 1). 이진수로 반복하는 방법: b 의 낮은 비트부터 보며 a 를 계속 제곱한다.

    result 에는 b 의 켜진 비트에 해당하는 a^(2^i) 만 곱해진다."""
    result = 1 % m
    a %= m
    while b > 0:
        if b & 1:
            result = result * a % m
        a = a * a % m
        b >>= 1
    return result


def power_mod_recursive(a: int, b: int, m: int) -> int:
    """a^b mod m 을 재귀로. 반으로 줄인 값을 제곱한다 (홀수면 a 를 한 번 더)."""
    if b == 0:
        return 1 % m
    half = power_mod_recursive(a, b // 2, m)
    result = half * half % m
    return result * a % m if b % 2 else result


def count_multiplications(b: int) -> int:
    """power_mod 가 b 에 대해 하는 곱셈 횟수 (제곱 + 결과 곱). 제곱은 bit_length 번, 결과 곱은 켜진 비트 수만큼."""
    return b.bit_length() + bin(b).count("1") if b else 0


def power_float(x: float, n: int) -> float:
    """x^n (n 은 음수 가능). 음수 지수는 역수의 양수 지수로 바꾼다."""
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result


def fibonacci_doubling(n: int) -> tuple[int, int]:
    """(F(n), F(n+1)) 를 O(log n) 에 구한다 (빠른 배가법). F(0)=0, F(1)=1.

    F(2k) = F(k)·(2F(k+1) - F(k)),  F(2k+1) = F(k)² + F(k+1)²  — 행렬 거듭제곱을 식으로 풀어 쓴 것이다."""
    if n == 0:
        return 0, 1
    a, b = fibonacci_doubling(n // 2)
    c = a * (2 * b - a)
    d = a * a + b * b
    return (d, c + d) if n % 2 else (c, d)


def main() -> None:
    a, b, c = map(int, sys.stdin.readline().split())
    print(power_mod(a, b, c))


if __name__ == "__main__":
    main()
