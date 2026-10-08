"""에라토스테네스의 체 — 작은 소수의 배수를 차례로 지워 가며 범위 안의 소수를 한꺼번에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 시간 O(n log log n), 메모리 O(n). 수 하나가 소수인지만 알고 싶다면 단순 소수 판별(O(√n))이 낫습니다.
- 직접 실행하면 `M N` 을 받아 M 이상 N 이하의 소수를 한 줄에 하나씩 출력합니다.
"""
import sys


def prime_table(n: int) -> list:
    """is_prime[i] = i 가 소수인가 (0 ~ n)."""
    is_prime = [True] * (n + 1)
    is_prime[0:2] = [False] * min(2, n + 1)  # 0 과 1 은 소수가 아니다
    i = 2
    while i * i <= n:  # √n 까지의 소수의 배수만 지우면 된다
        if is_prime[i]:
            for multiple in range(i * i, n + 1, i):  # i*i 보다 작은 i 의 배수는 이미 더 작은 소수가 지웠다
                is_prime[multiple] = False
        i += 1
    return is_prime


def sieve(n: int) -> list:
    """n 이하의 소수 목록."""
    return [i for i, flag in enumerate(prime_table(n)) if flag]


def count_primes(n: int) -> int:
    return sum(prime_table(n))


def smallest_prime_factor_table(n: int) -> list:
    """spf[i] = i 의 가장 작은 소인수 (i >= 2). 체와 같은 방식으로 만들며, 이것으로 어떤 수든 O(log n) 에 소인수분해된다."""
    spf = list(range(n + 1))
    i = 2
    while i * i <= n:
        if spf[i] == i:  # i 가 소수
            for multiple in range(i * i, n + 1, i):
                if spf[multiple] == multiple:  # 아직 더 작은 소인수가 정해지지 않은 경우에만
                    spf[multiple] = i
        i += 1
    return spf


def main() -> None:
    m, n = map(int, sys.stdin.readline().split())
    print("\n".join(str(p) for p in sieve(n) if p >= m))


if __name__ == "__main__":
    main()
