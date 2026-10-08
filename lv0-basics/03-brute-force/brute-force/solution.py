"""브루트 포스(완전 탐색) — 가능한 모든 경우를 하나씩 확인해서 답을 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
느리더라도 정답이 확실한 풀이는, 나중에 빠른 풀이를 검증하는 기준(test_solution.py 의 비교 대상)이 됩니다.
- 직접 실행하면 `N M` 과 N 개의 카드를 받아, 카드 3장의 합이 M 을 넘지 않는 최대값을 출력합니다.
"""
import sys
from itertools import combinations


def has_pair_with_sum(arr: list, target: int) -> bool:
    """서로 다른 두 위치의 합이 target 인 쌍이 있는지. 모든 쌍을 보므로 O(n²)."""
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):  # j 를 i + 1 부터 시작하면 같은 쌍을 두 번 보지 않는다
            if arr[i] + arr[j] == target:
                return True
    return False


def max_subarray_sum(arr: list) -> int:
    """연속한 구간(1개 이상)의 합 중 최댓값. 시작·끝을 모두 정하고 합을 이어서 더하므로 O(n²)."""
    best = arr[0]
    for start in range(len(arr)):
        total = 0
        for end in range(start, len(arr)):
            total += arr[end]
            best = max(best, total)
    return best


def closest_triple_sum(cards: list, limit: int) -> int:
    """카드 3장을 골라 합이 limit 를 넘지 않으면서 가장 크게 만든다. 가능한 모든 3장 조합을 본다. O(n³)."""
    best = -1
    for a, b, c in combinations(cards, 3):
        total = a + b + c
        if total <= limit and total > best:
            best = total
    return best


def smallest_generator(n: int) -> int:
    """x + (x 의 각 자릿수의 합) == n 인 가장 작은 x (분해합의 생성자). 없으면 0. 1 부터 n 까지 모두 시험한다."""
    for x in range(1, n):
        if x + sum(map(int, str(x))) == n:
            return x
    return 0


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    cards = list(map(int, input().split()))[:n]
    print(closest_triple_sum(cards, m))


if __name__ == "__main__":
    main()
