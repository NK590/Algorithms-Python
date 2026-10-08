"""페르마의 소정리 — p 가 소수이고 a 가 p 의 배수가 아니면 a^(p-1) ≡ 1 (mod p)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 쓰임 ① 모듈러 역원: a^(p-2) 가 a 의 역원이다. ② 큰 지수 줄이기: a^e ≡ a^(e mod (p-1)). ③ 소수 판정(페르마 검사).
- 역은 성립하지 않습니다. 합성수가 소수처럼 보이는 경우(유사 소수), 특히 모든 서로소인 a 에서 통과하는 카마이클 수가 있습니다.
- 직접 실행하면 `a p` (p 는 소수, a 는 p 의 배수가 아님) 를 받아 a 의 모듈러 역원 a^(p-2) mod p 를 출력합니다.
"""
import sys


def power_mod(a: int, b: int, m: int) -> int:
    """a^b mod m (b ≥ 0). 지수를 반으로 줄이며 제곱하는 빠른 거듭제곱."""
    result = 1 % m
    a %= m
    while b > 0:
        if b & 1:
            result = result * a % m
        a = a * a % m
        b >>= 1
    return result


def fermat_holds(a: int, p: int) -> bool:
    """a^(p-1) ≡ 1 (mod p) 인가. p 가 소수이고 a 가 p 의 배수가 아니면 항상 True."""
    return power_mod(a, p - 1, p) == 1


def inverse_mod_prime(a: int, p: int) -> int:
    """소수 p 에 대한 a 의 모듈러 역원: a · a^(p-2) = a^(p-1) ≡ 1 이므로 a^(p-2) mod p. a 가 p 의 배수이면 역원이 없다."""
    if a % p == 0:
        raise ValueError("a 가 p 의 배수이면 역원이 없습니다")
    return power_mod(a, p - 2, p)


def fermat_test(n: int, bases: tuple = (2, 3, 5, 7)) -> bool:
    """n 이 소수일 가능성이 있는가. 어떤 밑 a 에서든 a^(n-1) ≢ 1 이면 n 은 확실히 합성수. 모두 통과하면 '소수일 수도 있음' (합성수가 통과할 수 있다)."""
    if n < 2:
        return False
    for a in bases:
        if a % n == 0:
            continue  # n 이 밑 자신이거나 밑의 약수이면 이 밑은 쓸 수 없다
        if power_mod(a, n - 1, n) != 1:
            return False
    return True


def fermat_pseudoprimes(limit: int, base: int = 2) -> list[int]:
    """밑 base 의 페르마 검사를 통과하는 합성수(페르마 유사 소수)를 limit 이하에서 모두 찾는다. 밑 2 의 가장 작은 것은 341 = 11 · 31."""
    result = []
    for n in range(3, limit + 1):
        if power_mod(base, n - 1, n) == 1 and not _is_prime(n):
            result.append(n)
    return result


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def carmichael_numbers(limit: int) -> list[int]:
    """카마이클 수: 모든 a (n 과 서로소) 에 대해 a^(n-1) ≡ 1 (mod n) 을 만족하는 합성수. 페르마 검사로는 소수와 구별할 수 없다.

    코르젤트 판정법: n 이 합성수이고, 제곱 인수가 없고, n 의 모든 소인수 p 에 대해 (p - 1) | (n - 1) 이면 카마이클 수다."""
    result = []
    for n in range(3, limit + 1, 2):
        m, p, ok, factors = n, 2, True, 0
        while p * p <= m:
            if m % p == 0:
                m //= p
                if m % p == 0 or (n - 1) % (p - 1) != 0:
                    ok = False
                    break
                factors += 1
            p += 1
        if ok and m > 1:
            if (n - 1) % (m - 1) != 0:
                ok = False
            factors += 1
        if ok and factors >= 2:
            result.append(n)
    return result


def main() -> None:
    a, p = map(int, sys.stdin.readline().split())
    print(inverse_mod_prime(a, p))


if __name__ == "__main__":
    main()
