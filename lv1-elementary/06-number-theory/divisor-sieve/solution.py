"""약수 체 — 1 부터 n 까지 모든 수의 약수(개수·합·목록)를 한꺼번에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 수마다 약수를 따로 구하는 대신, d 를 약수로 갖는 수는 d 의 배수라는 점을 이용해 배수에 d 를 더해 나갑니다. 전체 O(n log n).
- 직접 실행하면 `T` 와 T 개의 `N` 을 받아, 각 N 에 대해 1 부터 N 까지 모든 수의 약수의 합을 더한 값을 출력합니다.
"""
import sys


def divisor_counts(n: int) -> list:
    """count[k] = k 의 약수의 개수 (1 ≤ k ≤ n). d = 1..n 마다 d 의 배수 모두에 1 을 더한다. 전체 n(1 + 1/2 + 1/3 + …) = O(n log n)."""
    count = [0] * (n + 1)
    for d in range(1, n + 1):
        for multiple in range(d, n + 1, d):
            count[multiple] += 1
    return count


def divisor_sums(n: int) -> list:
    """sigma[k] = k 의 약수의 합 (1 ≤ k ≤ n)."""
    sigma = [0] * (n + 1)
    for d in range(1, n + 1):
        for multiple in range(d, n + 1, d):
            sigma[multiple] += d
    return sigma


def divisor_lists(n: int) -> list:
    """divisors[k] = k 의 약수 목록 (오름차순). d 를 작은 것부터 넣으므로 자연히 정렬된다."""
    divisors = [[] for _ in range(n + 1)]
    for d in range(1, n + 1):
        for multiple in range(d, n + 1, d):
            divisors[multiple].append(d)
    return divisors


def sum_of_divisor_sums(n: int) -> int:
    """σ(1) + σ(2) + … + σ(n) (σ 는 약수의 합). d 는 1..n 의 수 중 d 의 배수 ⌊n / d⌋ 개에 약수로 들어가므로 Σ d × ⌊n / d⌋ 로 표 없이 구할 수 있다."""
    return sum(d * (n // d) for d in range(1, n + 1))


def main() -> None:
    input = sys.stdin.readline
    t = int(input())
    queries = [int(input()) for _ in range(t)]
    limit = max(queries, default=0)
    sigma = divisor_sums(limit)
    prefix = [0] * (limit + 1)
    for k in range(1, limit + 1):
        prefix[k] = prefix[k - 1] + sigma[k]
    print("\n".join(str(prefix[q]) for q in queries))


if __name__ == "__main__":
    main()
