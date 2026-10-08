"""민-25 체(Min_25 Sieve) — 곱셈적 함수의 합 Σ_{m≤n} f(m) 을 에라토스테네스의 체로는 불가능한 큰 n (10⁹~10¹¹) 까지 O(n^{3/4}/log n) 정도에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 1단계 (소수 테이블): "n // i 꼴의 값 v 마다 v 이하 소수의 p^k 의 합 g_k(v) (k = 0 이면 개수, 1 이면 합, 2 이면 제곱합)" 을 한 번에 구한다 (Lucy_Hedgehog).
  처음에는 "2 이상 모든 수" 의 p^k 합으로 시작해 작은 소수 p = 2, 3, 5, … (p² ≤ n) 의 배수 중 합성수를 차례로 지운다: g_k(v) -= p^k (g_k(v // p) - g_k(p - 1)) (v ≥ p²).
  n // i 꼴의 수만 필요하므로 상태가 O(√n) 개이고 전체 O(n^{3/4}).
- 2단계 (재귀): S(x, j) = 2 ≤ m ≤ x 이고 m 의 가장 작은 소인수가 j 번째 소수 이상인 m 에 대한 f(m) 의 합.
  S(x, j) = (x 이하 소수에서 j 번째 미만을 뺀 소수들의 f(p) 합) + Σ_{k ≥ j, p_k² ≤ x} Σ_{e ≥ 1, p_k^{e+1} ≤ x} ( f(p_k^e)·S(x // p_k^e, k + 1) + f(p_k^{e+1}) ).
  소수에서의 f(p) 는 p 의 (차수 ≤ 2) 다항식으로 주어지므로 1단계의 g_0, g_1, g_2 로 한 번에 구한다. 답은 1 + S(n, 1).
- prime_count(n), prime_sum(n): 1단계만. min25_sum(n, prime_poly, prime_power, mod=None): 일반 곱셈적 함수 (f(p) = Σ prime_poly[k]·p^k, f(p^e) = prime_power(p, e)).
- sum_totient(n) = Σ φ(m), sum_sigma(n) = Σ σ(m) (약수의 합), sum_mobius(n) = Σ μ(m) (메르텐스 함수): 곱셈적 함수의 대표 예.
- 직접 실행하면 `n` 하나를 받아 소수의 개수, 소수의 합, Σφ(m) 을 한 줄에 하나씩 출력합니다.
"""
import sys
from math import isqrt
from typing import Callable, Optional, Sequence


def _tables(n: int, degree: int):
    """(small, large, primes): small[k][v] = g_k(v) (v ≤ √n), large[k][i] = g_k(n // i) (1 ≤ i ≤ √n), primes = √n 이하 소수."""
    r = isqrt(n)

    def initial(k: int, v: int) -> int:
        if k == 0:
            return v - 1
        if k == 1:
            return v * (v + 1) // 2 - 1
        return v * (v + 1) * (2 * v + 1) // 6 - 1

    small = [[initial(k, v) for v in range(r + 1)] for k in range(degree + 1)]
    large = [[0] + [initial(k, n // i) for i in range(1, r + 1)] for k in range(degree + 1)]
    primes = []
    for p in range(2, r + 1):
        if small[0][p] == small[0][p - 1]:
            continue  # 합성수 (아직 소수 개수 테이블이 늘지 않았다)
        primes.append(p)
        limit = min(r, n // (p * p))
        for k in range(degree + 1):
            before = small[k][p - 1]
            weight = p ** k
            s, g = small[k], large[k]
            for i in range(1, limit + 1):
                ip = i * p
                g[i] -= weight * ((g[ip] if ip <= r else s[n // ip]) - before)
            for v in range(r, p * p - 1, -1):  # 큰 v 부터: 아직 갱신되지 않은 s[v // p] 를 읽어야 한다
                s[v] -= weight * (s[v // p] - before)
    return small, large, primes


def _lookup(n: int, r: int, small, large, k: int, v: int) -> int:
    """g_k(v) (v 는 n // i 꼴이거나 √n 이하)."""
    return small[k][v] if v <= r else large[k][n // v]


def prime_count(n: int) -> int:
    """n 이하 소수의 개수 π(n)."""
    if n < 2:
        return 0
    small, large, _ = _tables(n, 0)
    return large[0][1]


def prime_sum(n: int) -> int:
    """n 이하 소수의 합."""
    if n < 2:
        return 0
    small, large, _ = _tables(n, 1)
    return large[1][1]


def min25_sum(
    n: int,
    prime_poly: Sequence[int],
    prime_power: Callable[[int, int], int],
    mod: Optional[int] = None,
) -> int:
    """곱셈적 함수 f 에 대한 Σ_{m=1}^{n} f(m).

    prime_poly: f(p) = Σ prime_poly[k]·p^k 의 계수 (길이 1~3).  prime_power(p, e): f(p^e) (e ≥ 1, f(p) 와 일치해야 한다).
    계산은 정확한 정수로 하고, mod 가 주어지면 마지막에 mod 로 나눈 나머지를 돌려준다.
    """
    if n < 1:
        return 0
    degree = len(prime_poly) - 1
    if not 0 <= degree <= 2:
        raise ValueError("prime_poly 의 길이는 1 이상 3 이하여야 합니다")
    small, large, primes = _tables(n, degree)
    r = isqrt(n)

    def prime_f_total(v: int) -> int:
        """v 이하 모든 소수 p 에 대한 f(p) 의 합."""
        return sum(prime_poly[k] * _lookup(n, r, small, large, k, v) for k in range(degree + 1))

    # prefix[j] = 처음 j 개 소수의 f(p) 합
    prefix = [0]
    for p in primes:
        prefix.append(prefix[-1] + sum(prime_poly[k] * p ** k for k in range(degree + 1)))

    def recurse(x: int, j: int) -> int:
        result = prime_f_total(x) - prefix[j]  # x ≥ p_{j-1} 이므로 (p_{j-1}, x] 의 소수들
        for k in range(j, len(primes)):
            p = primes[k]
            if p * p > x:
                break
            pe, e = p, 1
            while pe * p <= x:
                result += prime_power(p, e) * recurse(x // pe, k + 1) + prime_power(p, e + 1)
                pe *= p
                e += 1
        return result

    total = 1 + recurse(n, 0)
    return total % mod if mod else total


def sum_totient(n: int, mod: Optional[int] = None) -> int:
    """Σ_{m≤n} φ(m): f(p) = p - 1, f(p^e) = p^{e-1}(p - 1)."""
    return min25_sum(n, [-1, 1], lambda p, e: p ** (e - 1) * (p - 1), mod)


def sum_sigma(n: int, mod: Optional[int] = None) -> int:
    """Σ_{m≤n} σ(m) (약수의 합): f(p) = p + 1, f(p^e) = 1 + p + … + p^e."""
    return min25_sum(n, [1, 1], lambda p, e: (p ** (e + 1) - 1) // (p - 1), mod)


def sum_mobius(n: int, mod: Optional[int] = None) -> int:
    """메르텐스 함수 M(n) = Σ_{m≤n} μ(m): f(p) = -1, f(p^e) = 0 (e ≥ 2)."""
    return min25_sum(n, [-1], lambda p, e: -1 if e == 1 else 0, mod)


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    print(prime_count(n))
    print(prime_sum(n))
    print(sum_totient(n))


if __name__ == "__main__":
    main()
