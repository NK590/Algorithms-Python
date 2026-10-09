"""뤼카 정리(Lucas' Theorem)와 그 일반화 — n 이 10^18 이어도 C(n, k) mod m 을 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 뤼카 정리: p 가 소수이고 n = Σ n_i·p^i, k = Σ k_i·p^i (p 진법) 이면  C(n, k) ≡ Π C(n_i, k_i) (mod p).  (k_i > n_i 인 자리가 있으면 0)
  각 자리의 이항 계수는 n_i, k_i < p 이므로 p 이하의 팩토리얼 표 하나(O(p))로 구한다.  lucas(n, k, p): O(p + log_p n).
- 쿠머 정리: C(n, k) 에 들어 있는 소수 p 의 지수 = k 와 n - k 를 p 진법으로 더할 때 올림의 횟수.
- 소수의 거듭제곱 p^e 가 모듈러일 때는 n! 에서 p 의 배수를 모두 뺀 값을 "p^e 를 주기로 하는 곱" 의 성질로 O(p^e) 에 구한다 (그랜빌).
  binomial_prime_power(n, k, p, e).  일반 m 은 m 을 p^e 들로 분해해 각각 구한 뒤 중국인의 나머지 정리로 합친다: binomial_mod(n, k, m).
- catalan_mod: C_n = C(2n, n) - C(2n, n + 1) (나눗셈 없이).
- 직접 실행하면 이항계수 예제 형식 — `N K M` (M 은 소수) — 을 받아 C(N, K) mod M 을 출력합니다.
"""
import sys
from functools import lru_cache


def _is_prime_small(p: int) -> bool:
    if p < 2:
        return False
    i = 2
    while i * i <= p:
        if p % i == 0:
            return False
        i += 1
    return True


@lru_cache(maxsize=32)
def _factorial_tables(p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """(0! … (p-1)! mod p, 각각의 역원)."""
    fact = [1] * p
    for i in range(1, p):
        fact[i] = fact[i - 1] * i % p
    inverse = [pow(f, -1, p) for f in fact]  # p 는 소수이고 f < p 는 0 이 아니므로 역원이 있다
    return tuple(fact), tuple(inverse)


TABLE_LIMIT = 2_000_000  # 이 크기까지의 소수는 팩토리얼 표를 만들어 쓴다


def _small_binomial(ni: int, ki: int, p: int) -> int:
    """C(ni, ki) mod p (0 ≤ ki ≤ ni < p). p 가 작으면 표, 크면 곱으로 O(min(ki, ni - ki))."""
    if p <= TABLE_LIMIT:
        fact, inverse = _factorial_tables(p)
        return fact[ni] * inverse[ki] % p * inverse[ni - ki] % p
    ki = min(ki, ni - ki)
    numerator = denominator = 1
    for j in range(1, ki + 1):
        numerator = numerator * (ni - ki + j) % p
        denominator = denominator * j % p
    return numerator * pow(denominator, -1, p) % p


def lucas(n: int, k: int, p: int) -> int:
    """C(n, k) mod p (p 소수). n, k 는 매우 커도 된다. p 가 작으면 O(p + log_p n), p 가 크면 자릿수마다 O(min(k_i, n_i - k_i))."""
    if not _is_prime_small(p):
        raise ValueError("p 는 소수여야 합니다")
    if k < 0 or k > n:
        return 0
    result = 1
    while k:
        ni, ki = n % p, k % p
        if ki > ni:
            return 0
        result = result * _small_binomial(ni, ki, p) % p
        n //= p
        k //= p
    return result


def digit_sum(n: int, p: int) -> int:
    total = 0
    while n:
        total += n % p
        n //= p
    return total


def kummer_valuation(n: int, k: int, p: int) -> int:
    """C(n, k) 를 나누는 p 의 최대 거듭제곱의 지수 = (s_p(k) + s_p(n-k) - s_p(n)) / (p - 1)  (올림의 횟수)."""
    if k < 0 or k > n:
        raise ValueError("0 ≤ k ≤ n 이어야 합니다")
    return (digit_sum(k, p) + digit_sum(n - k, p) - digit_sum(n, p)) // (p - 1)


def _unit_products(p: int, pe: int) -> list[int]:
    """table[i] = 1..i 중 p 의 배수가 아닌 수들의 곱 mod p^e."""
    table = [1] * (pe + 1)
    for i in range(1, pe + 1):
        table[i] = table[i - 1] * i % pe if i % p else table[i - 1]
    return table


def _factorial_without_p(n: int, p: int, pe: int, table: list[int]) -> int:
    """n! / p^(v_p(n!)) mod p^e.  n! = (p 와 서로소인 인수들의 곱) · p^(n//p) · (n//p)! 를 되풀이한다."""
    result = 1
    while n:
        result = result * pow(table[pe], n // pe, pe) % pe * table[n % pe] % pe
        n //= p
    return result


def binomial_prime_power(n: int, k: int, p: int, e: int) -> int:
    """C(n, k) mod p^e (p 소수)."""
    if not _is_prime_small(p) or e < 1:
        raise ValueError("p 는 소수, e 는 1 이상이어야 합니다")
    if k < 0 or k > n:
        return 0
    pe = p**e
    valuation = kummer_valuation(n, k, p)
    if valuation >= e:
        return 0
    table = _unit_products(p, pe)
    numerator = _factorial_without_p(n, p, pe, table)
    denominator = _factorial_without_p(k, p, pe, table) * _factorial_without_p(n - k, p, pe, table) % pe
    return numerator * pow(denominator, -1, pe) % pe * pow(p, valuation, pe) % pe


def _factor_small(m: int) -> list[tuple[int, int]]:
    factors = []
    p = 2
    while p * p <= m:
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            factors.append((p, e))
        p += 1
    if m > 1:
        factors.append((m, 1))
    return factors


def binomial_mod(n: int, k: int, m: int) -> int:
    """C(n, k) mod m (m ≥ 1 임의의 정수). m 의 소인수 p^e 마다 구해 중국인의 나머지 정리로 합친다. m 의 가장 큰 소인수의 거듭제곱이 약 10^7 이하일 때 실용적."""
    if m < 1:
        raise ValueError("m 은 1 이상이어야 합니다")
    if m == 1 or k < 0 or k > n:
        return 0
    result, modulus = 0, 1
    for p, e in _factor_small(m):
        pe = p**e
        r = lucas(n, k, p) if e == 1 else binomial_prime_power(n, k, p, e)
        # x ≡ result (mod modulus), x ≡ r (mod pe) 를 합친다 (modulus 와 pe 는 서로소)
        t = (r - result) * pow(modulus, -1, pe) % pe
        result += modulus * t
        modulus *= pe
    return result % m


def catalan_mod(n: int, m: int) -> int:
    """카탈란 수 C_n mod m = C(2n, n) - C(2n, n + 1)  (분모 n + 1 로 나누지 않아도 된다)."""
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    return (binomial_mod(2 * n, n, m) - binomial_mod(2 * n, n + 1, m)) % m


def main() -> None:
    n, k, m = (int(x) for x in sys.stdin.read().split()[:3])
    print(lucas(n, k, m))


if __name__ == "__main__":
    main()
