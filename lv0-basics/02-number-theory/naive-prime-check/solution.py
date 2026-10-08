"""단순 소수 판별 — 2부터 √n 까지 나누어 보기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 소수: 1과 자기 자신 외에는 약수가 없는 2 이상의 정수. 1은 소수가 아닙니다.
- 직접 실행하면 첫 줄에 N, 둘째 줄에 N개의 정수를 받아 그중 소수의 개수를 출력합니다.
"""
import sys
from math import isqrt


def is_prime(n: int) -> bool:
    """n 이 소수인지 판별한다. n 이 합성수라면 √n 이하의 약수가 반드시 하나 있으므로 거기까지만 확인하면 된다. O(√n)."""
    if n < 2:
        return False
    for d in range(2, isqrt(n) + 1):  # isqrt: 정수 제곱근(내림). 실수 sqrt 는 큰 수에서 오차가 날 수 있다
        if n % d == 0:
            return False
    return True


def is_prime_slow(n: int) -> bool:
    """2 부터 n-1 까지 전부 나누어 보는 가장 단순한 판별. O(n). 비교용."""
    if n < 2:
        return False
    return all(n % d != 0 for d in range(2, n))


def primes_up_to(limit: int) -> list:
    """limit 이하의 소수를 하나씩 판별해서 모은다. 한 번에 많이 구할 때는 에라토스테네스의 체가 훨씬 빠르다."""
    return [n for n in range(2, limit + 1) if is_prime(n)]


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    numbers = list(map(int, input().split()))[:n]
    print(sum(is_prime(x) for x in numbers))


if __name__ == "__main__":
    main()
