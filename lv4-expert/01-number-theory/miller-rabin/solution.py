"""밀러-라빈 소수 판정법(Miller–Rabin) — 큰 수가 소수인지를 O(k log³ n) 에 판정하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- n - 1 = 2^s · d (d 는 홀수) 로 쓴다. n 이 소수이면 어떤 a 에 대해서도 a^d ≡ 1 이거나, 어떤 0 ≤ r < s 에 대해 a^(2^r · d) ≡ -1 (mod n).
  이 조건을 만족하지 않는 a 가 하나라도 있으면(증인, witness) n 은 합성수가 확실합니다.
- 페르마 판정(a^(n-1) ≡ 1) 은 카마이클 수(561 등) 에서 모든 a 에 대해 속지만, 이 강한 조건은 어떤 합성수든 적어도 3/4 의 a 에서 걸러냅니다.
- is_prime(n): 밑을 처음 13 개의 소수(2..41) 로 고정하면 n < 3 317 044 064 679 887 385 961 981 (≈ 3.3·10^24) 에서 결정적(오답 없음).
  그보다 큰 n 은 무작위 밑으로 `rounds` 번 (오답 확률 ≤ 4^(-rounds)).
- is_strong_probable_prime(n, a): 밑 하나로 한 번 시험. is_fermat_probable_prime(n, a): 페르마 판정(비교용).
- next_prime(n): n 보다 큰 가장 작은 소수.
- 직접 실행하면 BOJ 5615 형식 — `N` 과 N 개의 넓이 S — 을 받아, 2S + 1 이 소수인 S 의 개수를 출력합니다 (S = 2xy + x + y 로 쓸 수 없는 넓이).
"""
import random
import sys
from typing import Optional

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
DETERMINISTIC_LIMIT = 3_317_044_064_679_887_385_961_981  # 이 값 미만은 위 13 개 밑으로 결정적


def _decompose(n: int) -> tuple[int, int]:
    """n - 1 = 2^s · d (d 홀수) 의 (s, d)."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def is_strong_probable_prime(n: int, a: int) -> bool:
    """밑 a 에 대한 강한 확률적 소수 판정 (n 은 3 이상의 홀수, 1 < a < n - 1 인 경우 의미가 있다).
    소수는 모든 a 에서 True. 합성수가 True 를 받으면 "a 에 대한 강한 의사소수" 라 하고, 그런 a 는 전체의 1/4 이하."""
    s, d = _decompose(n)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def is_fermat_probable_prime(n: int, a: int) -> bool:
    """페르마 판정 a^(n-1) ≡ 1 (mod n). 카마이클 수는 n 과 서로소인 모든 a 에서 통과하므로 믿을 수 없다."""
    return pow(a, n - 1, n) == 1


def is_prime(n: int, rounds: int = 40, rng: Optional[random.Random] = None) -> bool:
    """n 이 소수인가. n < 3.3·10^24 이면 결정적, 그 이상이면 무작위 밑 `rounds` 개 (오답 확률 ≤ 4^(-rounds))."""
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p
    if n < DETERMINISTIC_LIMIT:
        bases = SMALL_PRIMES
    else:
        rng = rng or random.Random()
        bases = [rng.randrange(2, n - 1) for _ in range(rounds)]
    return all(is_strong_probable_prime(n, a) for a in bases)


def next_prime(n: int) -> int:
    """n 보다 큰 가장 작은 소수."""
    candidate = max(n + 1, 2)
    if candidate > 2 and candidate % 2 == 0:
        candidate += 1
    while not is_prime(candidate):
        candidate += 2  # 처음 후보가 2 면 곧바로 소수이므로 여기서는 항상 홀수
    return candidate


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    print(sum(1 for s in data[1 : 1 + n] if is_prime(2 * int(s) + 1)))


if __name__ == "__main__":
    main()
