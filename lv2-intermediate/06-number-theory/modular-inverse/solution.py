"""모듈러 역원 — 나머지 연산에서의 "나눗셈": a · x ≡ 1 (mod m) 인 x

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 역원이 존재할 조건은 gcd(a, m) = 1 입니다. 존재하면 0 ≤ x < m 에서 유일합니다.
- 구하는 방법: ① m 이 소수: 페르마의 소정리 a^(m-2)  ② m 이 합성수: 오일러 정리 a^(φ(m)-1)  ③ 1..n 의 역원을 한꺼번에: 선형 점화식
  (확장 유클리드 호제법으로 구하는 방법은 Lv3 에서 다룹니다. 파이썬 3.8+ 에는 pow(a, -1, m) 도 있습니다)
- 나눗셈: (a / b) mod m = a · b⁻¹ mod m.  m 이 소수일 때 b 가 m 의 배수가 아니면 가능하다.
- 직접 실행하면 `a m` 을 받아 a 의 모듈러 역원을 출력합니다. 없으면 -1.
"""
import math
import sys


def power_mod(a: int, b: int, m: int) -> int:
    result = 1 % m
    a %= m
    while b > 0:
        if b & 1:
            result = result * a % m
        a = a * a % m
        b >>= 1
    return result


def has_inverse(a: int, m: int) -> bool:
    """a 의 모듈러 역원이 존재하는가: gcd(a, m) = 1 일 때만."""
    return m >= 1 and math.gcd(a, m) == 1


def inverse_fermat(a: int, p: int) -> int:
    """m 이 소수 p 일 때: a^(p-2) mod p (페르마의 소정리). a 가 p 의 배수이면 ValueError."""
    if a % p == 0:
        raise ValueError("역원이 없습니다")
    return power_mod(a, p - 2, p)


def phi(n: int) -> int:
    result, remaining, p = n, n, 2
    while p * p <= remaining:
        if remaining % p == 0:
            while remaining % p == 0:
                remaining //= p
            result -= result // p
        p += 1
    if remaining > 1:
        result -= result // remaining
    return result


def inverse_euler(a: int, m: int) -> int:
    """m 이 합성수여도 되는 방법: a^φ(m) ≡ 1 이므로 a · a^(φ(m)-1) ≡ 1. gcd(a, m) ≠ 1 이면 ValueError."""
    if not has_inverse(a, m):
        raise ValueError("역원이 없습니다")
    return power_mod(a, phi(m) - 1, m)


def inverse_brute_force(a: int, m: int) -> int:
    """정의 그대로 0..m-1 을 모두 시도하는 O(m) 방법 (검증용). 없으면 -1."""
    for x in range(m):
        if a * x % m == 1 % m:
            return x
    return -1


def inverse_table(n: int, p: int) -> list[int]:
    """1..n 의 모듈러 역원을 O(n) 에 (p 는 소수, n < p).  inv[i] = -(p // i) · inv[p % i] mod p.

    p = (p // i) · i + (p % i) 의 양변에 inv[i] · inv[p % i] 를 곱해 정리하면 나온다. inv[0] 은 의미 없는 자리표시(0)."""
    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = (p - (p // i) * inv[p % i] % p) % p
    return inv


def divide_mod(a: int, b: int, p: int) -> int:
    """(a / b) mod p. 소수 p 에서 b 가 p 의 배수가 아닐 때."""
    return a % p * inverse_fermat(b, p) % p


def main() -> None:
    a, m = map(int, sys.stdin.readline().split())
    print(inverse_euler(a, m) if has_inverse(a, m) else -1)


if __name__ == "__main__":
    main()
