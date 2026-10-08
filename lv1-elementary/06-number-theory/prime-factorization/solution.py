"""소인수분해 — 자연수를 소수의 곱으로 나타내기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 작은 소수부터 나눌 수 있을 때까지 나눕니다. √n 까지만 보면 되고, 마지막에 남은 1 보다 큰 수는 그 자체가 소수입니다.
- 직접 실행하면 N 을 받아 소인수를 오름차순으로 한 줄에 하나씩 출력합니다. (1 이면 아무것도 출력하지 않습니다)
"""
import sys


def factorize(n: int) -> list:
    """n 의 소인수를 오름차순으로 (중복 포함) 반환한다. 예: 12 → [2, 2, 3]. O(√n)"""
    factors = []
    d = 2
    while d * d <= n:  # 남은 n 이 합성수라면 √n 이하의 약수가 반드시 있다
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)  # √n 이하로 다 나눈 뒤 남은 1 보다 큰 수는 소수다
    return factors


def prime_exponents(n: int) -> dict:
    """소인수와 지수. 예: 360 → {2: 3, 3: 2, 5: 1}"""
    exponents = {}
    for p in factorize(n):
        exponents[p] = exponents.get(p, 0) + 1
    return exponents


def factorize_with_spf(n: int, spf: list) -> list:
    """가장 작은 소인수 표(spf)를 이용한 소인수분해. 표를 한 번 만들어 두면 수마다 O(log n) 이다."""
    factors = []
    while n > 1:
        factors.append(spf[n])
        n //= spf[n]
    return factors


def count_divisors(n: int) -> int:
    """약수의 개수 = (지수 + 1) 의 곱. 예: 360 = 2³·3²·5 → 4 × 3 × 2 = 24"""
    result = 1
    for exponent in prime_exponents(n).values():
        result *= exponent + 1
    return result


def sum_of_divisors(n: int) -> int:
    """약수의 합 = 각 소인수 p^e 에 대해 (1 + p + … + p^e) 의 곱."""
    result = 1
    for p, e in prime_exponents(n).items():
        result *= (p ** (e + 1) - 1) // (p - 1)
    return result


def main() -> None:
    n = int(sys.stdin.readline())
    print("\n".join(map(str, factorize(n))))


if __name__ == "__main__":
    main()
