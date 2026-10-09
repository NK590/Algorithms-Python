"""폴라드 로(Pollard's rho) — 큰 합성수의 약수를 O(n^(1/4)) 번의 연산으로 찾아 소인수분해하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 합성수 n 의 가장 작은 소인수를 p 라 하면, f(x) = x² + c (mod n) 로 만든 수열은 mod p 에서 약 √p 번 만에 순환에 들어간다 (생일 역설).
  mod n 으로는 아직 서로 다른 두 값 x, y 가 mod p 로는 같아지는 순간 gcd(|x - y|, n) 이 p 의 배수가 되어 약수가 튀어나옵니다.
- 순환을 찾는 데는 Brent 의 방법(지수적으로 늘리는 구간) 을 쓰고, gcd 를 매번 구하는 대신 |x - y| 를 128 개씩 곱해 한 번에 gcd 를 구해 비용을 줄입니다.
- factorize(n): 작은 소수로 먼저 나눈 뒤, 남은 수에 대해 (밀러-라빈으로 소수 판정) → (소수가 아니면 폴라드 로로 약수 분리) 를 되풀이한다.
  이 파일은 혼자 실행되도록 밀러-라빈 판정을 안에 포함합니다.
- 활용: divisors, count_divisors, sum_divisors, euler_phi 를 소인수분해로부터 계산.
- 직접 실행하면 소인수분해 예제 형식 — 큰 수 하나(< 2^62) — 를 받아 소인수를 오름차순으로 한 줄에 하나씩(중복 포함) 출력합니다.
"""
import math
import random
import sys
from typing import Optional

_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
_DETERMINISTIC_LIMIT = 3_317_044_064_679_887_385_961_981


def _sieve(limit: int) -> list[int]:
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, int(limit**0.5) + 1):
        if flags[i]:
            flags[i * i :: i] = bytearray(len(flags[i * i :: i]))
    return [i for i, f in enumerate(flags) if f]


SMALL_PRIMES = _sieve(1000)


def is_prime(n: int, rng: Optional[random.Random] = None) -> bool:
    """밀러-라빈 (n < 3.3·10^24 이면 결정적, 그 이상이면 무작위 밑 40 개)."""
    if n < 2:
        return False
    for p in _BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    if n < _DETERMINISTIC_LIMIT:
        bases = _BASES
    else:
        rng = rng or random.Random(n)
        bases = [rng.randrange(2, n - 1) for _ in range(40)]
    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _brent(n: int, c: int, rng: random.Random, batch: int = 128) -> int:
    """f(x) = x² + c 로 Brent 순환 탐색. n 의 약수(1 또는 n 이면 실패) 를 돌려준다."""
    y = rng.randrange(1, n)
    g = r = q = 1
    x = ys = y
    while g == 1:
        x = y
        for _ in range(r):
            y = (y * y + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for _ in range(min(batch, r - k)):
                y = (y * y + c) % n
                q = q * abs(x - y) % n
            g = math.gcd(q, n)
            k += batch
        r *= 2
    if g == n:  # 곱이 n 의 배수가 되어 버렸다: 직전 구간을 한 걸음씩 다시 보며 gcd 를 구한다
        g = 1
        while g == 1:
            ys = (ys * ys + c) % n
            g = math.gcd(abs(x - ys), n)
    return g


def pollard_rho(n: int, rng: Optional[random.Random] = None) -> int:
    """합성수 n 의 자명하지 않은 약수 (1 < d < n) 하나. n 이 소수이거나 4 미만이면 ValueError."""
    if n < 4 or is_prime(n):
        raise ValueError("합성수가 아닙니다")
    if n % 2 == 0:
        return 2
    rng = rng or random.Random(n)
    c = 1
    while True:
        d = _brent(n, c, rng)
        if 1 < d < n:
            return d
        c += 1  # 실패하면 다른 상수 c 로 다시


def factorize(n: int, rng: Optional[random.Random] = None) -> dict[int, int]:
    """{소인수: 지수}. factorize(1) == {}."""
    if n < 1:
        raise ValueError("n 은 1 이상이어야 합니다")
    result: dict[int, int] = {}
    for p in SMALL_PRIMES:  # 작은 소수는 시행 나눗셈으로 먼저
        if p * p > n:
            break
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m, rng):
            result[m] = result.get(m, 0) + 1
            continue
        d = pollard_rho(m, rng)
        stack.append(d)
        stack.append(m // d)
    return dict(sorted(result.items()))


def prime_factors(n: int) -> list[int]:
    """소인수를 오름차순으로, 중복 포함 (12 -> [2, 2, 3])."""
    return [p for p, e in factorize(n).items() for _ in range(e)]


def divisors(n: int) -> list[int]:
    """n 의 모든 약수를 오름차순으로."""
    result = [1]
    for p, e in factorize(n).items():
        result = [d * p**k for d in result for k in range(e + 1)]
    return sorted(result)


def count_divisors(n: int) -> int:
    count = 1
    for e in factorize(n).values():
        count *= e + 1
    return count


def sum_divisors(n: int) -> int:
    total = 1
    for p, e in factorize(n).items():
        total *= (p ** (e + 1) - 1) // (p - 1)
    return total


def euler_phi(n: int) -> int:
    """1..n 중 n 과 서로소인 수의 개수."""
    result = n
    for p in factorize(n):
        result = result // p * (p - 1)
    return result


def main() -> None:
    n = int(sys.stdin.readline())
    print("\n".join(map(str, prime_factors(n))))


if __name__ == "__main__":
    main()
