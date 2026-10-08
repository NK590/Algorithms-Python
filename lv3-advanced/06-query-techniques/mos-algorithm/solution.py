"""모스 알고리즘(Mo's Algorithm) — 갱신 없는 구간 질의를 순서만 바꿔서 O((n + q)·√n) 에 오프라인으로 풀기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 구간 [l, r) 의 답을 "원소 하나를 넣기(add)" 와 "빼기(remove)" 로만 갱신할 수 있으면, 질의를 알맞은 순서로 처리하면서
  현재 구간의 두 끝점 (cl, cr) 을 다음 질의의 구간까지 한 칸씩 옮겨 가며 답을 유지합니다.
- 순서: 왼쪽 끝 l 을 크기 B 의 블록으로 나눠 블록 번호순으로, 같은 블록 안에서는 오른쪽 끝 r 의 오름차순으로 (블록마다 오름/내림을 번갈아 — 홀짝 최적화).
  왼쪽 끝은 한 질의에서 많아야 B 칸, 오른쪽 끝은 블록 하나당 n 칸 움직이므로 q·B + (n/B)·n, B = n/√q 로 잡으면 총 O(n√q).
- 구간은 반열린 [l, r) (0 부터). 빈 구간(l == r)도 허용.
- 직접 실행하면 `N`, 수열, `M`, M 개의 질의(1 부터, 양 끝 포함) 를 받아 각 질의 구간의 서로 다른 값의 수를 출력합니다.
"""
import sys
from typing import Callable, Sequence


def mo_order(n: int, queries: Sequence[tuple[int, int]]) -> list[int]:
    """질의 번호를 처리할 순서로 정렬해 돌려준다. 왼쪽 끝의 블록 번호순, 같은 블록 안에서는 오른쪽 끝을 오름/내림 번갈아."""
    q = len(queries)
    block = max(1, round(n / max(1, q) ** 0.5))

    def key(index: int) -> tuple[int, int]:
        left, right = queries[index]
        b = left // block
        return (b, right if b % 2 == 0 else -right)

    return sorted(range(q), key=key)


def mo(
    n: int,
    queries: Sequence[tuple[int, int]],
    add: Callable[[int], None],
    remove: Callable[[int], None],
    answer: Callable[[], object],
) -> list:
    """queries[i] = (l, r) (반열린). add(i)/remove(i) 는 원소 i 를 구간에 넣고/빼며 상태를 갱신하고, answer() 는 지금 구간의 답을 돌려준다.
    결과는 질의가 들어온 순서대로."""
    result = [None] * len(queries)
    cl = cr = 0  # 현재 구간 [cl, cr)
    for index in mo_order(n, queries):
        left, right = queries[index]
        while cl > left:  # 넓히는 쪽을 먼저 해야 구간이 음수 길이가 되지 않는다
            cl -= 1
            add(cl)
        while cr < right:
            add(cr)
            cr += 1
        while cl < left:
            remove(cl)
            cl += 1
        while cr > right:
            cr -= 1
            remove(cr)
        result[index] = answer()
    return result


def pointer_moves(order: Sequence[int], queries: Sequence[tuple[int, int]]) -> int:
    """order 순서로 처리할 때 두 끝점이 움직이는 총 칸 수 ((0, 0) 에서 시작). 순서를 바꾸면 얼마나 줄어드는지 보는 용도."""
    cl = cr = total = 0
    for index in order:
        left, right = queries[index]
        total += abs(cl - left) + abs(cr - right)
        cl, cr = left, right
    return total


def distinct_counts(a: Sequence, queries: Sequence[tuple[int, int]]) -> list[int]:
    """각 구간 [l, r) 에 서로 다른 값이 몇 종류 있는가."""
    ids = {}
    compressed = [ids.setdefault(x, len(ids)) for x in a]
    count = [0] * len(ids)
    state = [0]  # state[0] = 지금 구간의 서로 다른 값의 수

    def add(i: int) -> None:
        v = compressed[i]
        if count[v] == 0:
            state[0] += 1
        count[v] += 1

    def remove(i: int) -> None:
        v = compressed[i]
        count[v] -= 1
        if count[v] == 0:
            state[0] -= 1

    return mo(len(a), queries, add, remove, lambda: state[0])


def equal_pair_counts(a: Sequence, queries: Sequence[tuple[int, int]]) -> list[int]:
    """각 구간 [l, r) 에서 값이 같은 두 위치 쌍 (i < j) 의 수. 값 v 가 c 번 나오면 c(c-1)/2 쌍."""
    ids = {}
    compressed = [ids.setdefault(x, len(ids)) for x in a]
    count = [0] * len(ids)
    state = [0]

    def add(i: int) -> None:
        v = compressed[i]
        state[0] += count[v]  # 새 원소가 이미 있던 같은 값 count[v] 개와 각각 한 쌍
        count[v] += 1

    def remove(i: int) -> None:
        v = compressed[i]
        count[v] -= 1
        state[0] -= count[v]

    return mo(len(a), queries, add, remove, lambda: state[0])


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = data[1 : 1 + n]
    m = int(data[1 + n])
    queries = [(int(data[2 + n + 2 * i]) - 1, int(data[3 + n + 2 * i])) for i in range(m)]  # 1 부터 양 끝 포함 -> 0 부터 반열린
    print("\n".join(map(str, distinct_counts(a, queries))))


if __name__ == "__main__":
    main()
