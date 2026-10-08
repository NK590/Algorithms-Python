"""뫼비우스 반전(Möbius Inversion) — "약수에 대한 합" 을 거꾸로 풀어, 서로소 쌍·제곱 없는 수·gcd 합을 세기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 뫼비우스 함수 μ(n): n = 1 이면 1, 제곱수로 나누어떨어지면 0, 서로 다른 소수 k 개의 곱이면 (-1)^k.  핵심 성질  Σ_{d|n} μ(d) = [n == 1].
- 반전 공식: F(n) = Σ_{d|n} f(d)  ⟺  f(n) = Σ_{d|n} μ(n/d)·F(d).  약수에 대한 합 F 만 쉽게 구해질 때 f 를 되찾는다.
- 서로소 세기: [gcd(a, b) = 1] = Σ_{d|gcd(a,b)} μ(d) 를 대입하면 서로소 쌍의 수 = Σ_d μ(d)·⌊n/d⌋².  ⌊n/d⌋ 가 같은 d 를 묶으면 O(√n) 구간 (뫼비우스의 누적 합 = 메르텐스 함수 필요).
- mobius_sieve(n): 선형 체로 μ(1..n).  divisor_sum_transform / inverse_divisor_sum_transform: F ↔ f 를 O(N log N) 에 변환.
- count_coprime_pairs(_fast), count_pairs_with_gcd, count_coprime_to(n, m), count_squarefree(n), sum_of_gcds(n), sum_gcd_all_pairs(n).
- 직접 실행하면 n 을 받아 1 ≤ a, b ≤ n 이고 gcd(a, b) = 1 인 순서쌍의 수를 출력합니다.
"""
import math
import sys


def mobius_sieve(n: int) -> list[int]:
    """mu[0..n] (mu[0] = 0). 선형 체: 각 합성수를 가장 작은 소인수로 한 번씩만 지운다."""
    mu = [0] * (n + 1)
    if n >= 1:
        mu[1] = 1
    primes: list[int] = []
    composite = bytearray(n + 1)
    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            composite[i * p] = 1
            if i % p == 0:
                mu[i * p] = 0  # p² 가 약수
                break
            mu[i * p] = -mu[i]
    return mu


def mobius(n: int) -> int:
    """μ(n) 하나를 시행 나눗셈으로 (n ≥ 1)."""
    if n < 1:
        raise ValueError("n 은 1 이상이어야 합니다")
    result = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            result = -result
        p += 1
    return -result if n > 1 else result


def divisor_sum_transform(f: list[int]) -> list[int]:
    """f[1..N] 에서 F[n] = Σ_{d|n} f[d] (인덱스 0 은 무시). O(N log N)."""
    size = len(f)
    result = [0] * size
    for d in range(1, size):
        value = f[d]
        if value:
            for m in range(d, size, d):
                result[m] += value
    return result


def inverse_divisor_sum_transform(big_f: list[int]) -> list[int]:
    """뫼비우스 반전: F[n] = Σ_{d|n} f[d] 인 f 를 되찾는다. d 를 키우며 확정된 f[d] 를 모든 배수에서 뺀다. O(N log N)."""
    f = list(big_f)
    f[0] = 0
    size = len(f)
    for d in range(1, size):
        value = f[d]
        if value:
            for m in range(2 * d, size, d):
                f[m] -= value
    return f


def euler_phi_table(n: int) -> list[int]:
    """φ(1..n). 뫼비우스 반전: n = Σ_{d|n} φ(d) 이므로 φ 는 항등 함수의 반전."""
    return inverse_divisor_sum_transform(list(range(n + 1)))


def mertens_prefix(mu: list[int]) -> list[int]:
    """M[k] = μ(1) + … + μ(k)."""
    prefix = [0] * len(mu)
    for k in range(1, len(mu)):
        prefix[k] = prefix[k - 1] + mu[k]
    return prefix


def count_coprime_pairs(n: int) -> int:
    """1 ≤ a, b ≤ n 이고 gcd(a, b) = 1 인 순서쌍의 수 = Σ_d μ(d)·⌊n/d⌋².  O(n)."""
    mu = mobius_sieve(n)
    return sum(mu[d] * (n // d) ** 2 for d in range(1, n + 1))


def count_coprime_pairs_fast(n: int, mu_prefix: list[int] | None = None) -> int:
    """같은 값을 ⌊n/d⌋ 가 같은 d 구간으로 묶어 O(√n) 항으로. 메르텐스 함수(μ 의 누적 합) 표는 O(n) 에 만들거나 받는다."""
    if mu_prefix is None:
        mu_prefix = mertens_prefix(mobius_sieve(n))
    total = 0
    d = 1
    while d <= n:
        q = n // d
        last = n // q  # ⌊n/d'⌋ = q 인 마지막 d'
        total += (mu_prefix[last] - mu_prefix[d - 1]) * q * q
        d = last + 1
    return total


def count_pairs_with_gcd(n: int, m: int, g: int) -> int:
    """1 ≤ a ≤ n, 1 ≤ b ≤ m 이고 gcd(a, b) = g 인 순서쌍의 수 = (n/g, m/g) 범위의 서로소 쌍 = Σ_d μ(d)·⌊n/(gd)⌋·⌊m/(gd)⌋."""
    if g < 1:
        raise ValueError("g 는 1 이상이어야 합니다")
    n, m = n // g, m // g
    limit = min(n, m)
    mu = mobius_sieve(limit)
    return sum(mu[d] * (n // d) * (m // d) for d in range(1, limit + 1))


def count_coprime_to(n: int, m: int) -> int:
    """1..n 중 m 과 서로소인 수의 개수 = Σ_{d|m} μ(d)·⌊n/d⌋ (포함-배제를 뫼비우스로 쓴 것). m 은 시행 나눗셈으로 소인수분해."""
    if m < 1:
        raise ValueError("m 은 1 이상이어야 합니다")
    primes = []
    rest, p = m, 2
    while p * p <= rest:
        if rest % p == 0:
            primes.append(p)
            while rest % p == 0:
                rest //= p
        p += 1
    if rest > 1:
        primes.append(rest)
    total = 0
    for mask in range(1 << len(primes)):  # 제곱 없는 약수 d (μ(d) ≠ 0) 만 나열
        d, sign = 1, 1
        for i, prime in enumerate(primes):
            if mask >> i & 1:
                d *= prime
                sign = -sign
        total += sign * (n // d)
    return total


def count_squarefree(n: int) -> int:
    """1..n 중 제곱수(>1) 로 나누어떨어지지 않는 수의 개수 = Σ_{d ≥ 1} μ(d)·⌊n/d²⌋.  O(√n)."""
    if n < 1:
        return 0
    root = math.isqrt(n)
    mu = mobius_sieve(root)
    return sum(mu[d] * (n // (d * d)) for d in range(1, root + 1))


def sum_of_gcds(n: int) -> int:
    """Σ_{i=1..n} gcd(i, n) = Σ_{d|n} d·φ(n/d)  (Pillai 함수)."""
    phi = euler_phi_table(n)
    return sum(d * phi[n // d] for d in range(1, n + 1) if n % d == 0)


def sum_gcd_all_pairs(n: int) -> int:
    """Σ_{a=1..n} Σ_{b=1..n} gcd(a, b) = Σ_d φ(d)·⌊n/d⌋²  (gcd(a, b) = Σ_{d|gcd} φ(d) 를 대입)."""
    phi = euler_phi_table(n)
    return sum(phi[d] * (n // d) ** 2 for d in range(1, n + 1))


def main() -> None:
    n = int(sys.stdin.readline())
    print(count_coprime_pairs_fast(n))


if __name__ == "__main__":
    main()
