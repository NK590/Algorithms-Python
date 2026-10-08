"""조합 nCr mod p — 팩토리얼과 역원 팩토리얼로 큰 이항 계수를 나머지로 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- nCr = n! / (r! (n-r)!). p 가 소수이면 나눗셈을 모듈러 역원(페르마의 소정리)으로 바꿔 O(n) 전처리 후 질의당 O(1) 입니다.
- 모듈러 p 가 합성수라면 역원이 없을 수 있으므로, 덧셈만 쓰는 파스칼의 삼각형(nCr = (n-1)C(r-1) + (n-1)Cr) 으로 O(n·r) 에 구합니다.
- 직접 실행하면 `N K` 를 받아 C(N, K) 를 1,000,000,007 로 나눈 나머지를 출력합니다.
"""
import sys

MOD = 1_000_000_007


def build_factorials(n: int, p: int) -> tuple[list[int], list[int]]:
    """(fact, inv_fact) : fact[i] = i! mod p,  inv_fact[i] = (i!)⁻¹ mod p  (0 ≤ i ≤ n, p 는 n 보다 큰 소수).

    역원은 마지막 하나만 거듭제곱으로 구하고, inv_fact[i-1] = inv_fact[i] · i 로 거꾸로 채운다. 역원 계산을 n 번이 아니라 한 번만 한다."""
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], p - 2, p)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % p
    return fact, inv_fact


def binomial_mod(n: int, r: int, p: int, fact: list[int], inv_fact: list[int]) -> int:
    """C(n, r) mod p. 전처리한 fact, inv_fact 로 O(1). r < 0 이거나 r > n 이면 0."""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % p * inv_fact[n - r] % p


def binomial_once(n: int, r: int, p: int = MOD) -> int:
    """질의가 하나뿐일 때: 전체 팩토리얼 표 없이 분자·분모를 r 번의 곱으로 계산하고 분모의 역원을 한 번만 구한다. O(r + log p)."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    numerator = denominator = 1
    for i in range(r):
        numerator = numerator * (n - i) % p
        denominator = denominator * (i + 1) % p
    return numerator * pow(denominator, p - 2, p) % p


def binomial_pascal(n: int, r: int, mod: int) -> int:
    """p 가 소수가 아니어도 되는 방법: 파스칼의 삼각형을 r 열까지만 한 줄(1 차원)로 갱신한다. O(n·r)."""
    if r < 0 or r > n:
        return 0
    row = [1] + [0] * r
    for i in range(1, n + 1):
        for j in range(min(i, r), 0, -1):
            row[j] = (row[j] + row[j - 1]) % mod
    return row[r] % mod


def catalan_mod(n: int, p: int, fact: list[int], inv_fact: list[int]) -> int:
    """카탈란 수 C(2n, n) / (n+1) mod p.  역원 없이 C(2n, n) - C(2n, n+1) 로 구한다 (fact 는 2n 까지 필요)."""
    return (binomial_mod(2 * n, n, p, fact, inv_fact) - binomial_mod(2 * n, n + 1, p, fact, inv_fact)) % p


def grid_paths_mod(rows: int, cols: int, p: int, fact: list[int], inv_fact: list[int]) -> int:
    """rows × cols 칸의 왼쪽 위에서 오른쪽 아래까지 오른쪽·아래로만 가는 경로의 수 mod p = C(rows + cols - 2, rows - 1)."""
    return binomial_mod(rows + cols - 2, rows - 1, p, fact, inv_fact)


def multiset_count(n: int, k: int, p: int, fact: list[int], inv_fact: list[int]) -> int:
    """n 종류에서 중복을 허용해 k 개를 고르는 방법 (중복 조합) = C(n + k - 1, k) mod p."""
    return binomial_mod(n + k - 1, k, p, fact, inv_fact)


def main() -> None:
    n, k = map(int, sys.stdin.readline().split())
    print(binomial_once(n, k, MOD))


if __name__ == "__main__":
    main()
