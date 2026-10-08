"""약수와 배수 — 나누어떨어지는 관계를 다루기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- a 가 b 로 나누어떨어지면 b 는 a 의 약수, a 는 b 의 배수입니다. (a % b == 0)
- 직접 실행하면 첫 줄에 N, 둘째 줄에 K 를 받아 N 의 약수 중 K번째로 작은 것을 출력합니다. 없으면 0 입니다.
"""
import sys
from math import isqrt


def divisors_slow(n: int) -> list:
    """1 부터 n 까지 전부 나누어 보는 방법. O(n). 비교용."""
    return [d for d in range(1, n + 1) if n % d == 0]


def divisors(n: int) -> list:
    """n 의 약수를 오름차순으로 반환한다. 약수는 (d, n // d) 쌍으로 나오므로 √n 까지만 보면 된다. O(√n)."""
    small, large = [], []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            small.append(d)
            if d != n // d:  # n 이 제곱수일 때 √n 이 두 번 들어가면 안 된다
                large.append(n // d)
    return small + large[::-1]


def multiples(n: int, limit: int) -> list:
    """n 의 배수 중 limit 이하인 것들 (n, 2n, 3n, ...)."""
    return list(range(n, limit + 1, n))


def is_perfect_number(n: int) -> bool:
    """자기 자신을 뺀 약수의 합이 자기 자신과 같은 수인지 (6 = 1 + 2 + 3)."""
    return n > 1 and sum(divisors(n)) - n == n


def kth_divisor(n: int, k: int) -> int:
    """n 의 약수 중 k번째(1부터)로 작은 값. 약수가 k개보다 적으면 0."""
    found = divisors(n)
    return found[k - 1] if k <= len(found) else 0


def main() -> None:
    input = sys.stdin.readline
    n, k = map(int, input().split())
    print(kth_divisor(n, k))


if __name__ == "__main__":
    main()
