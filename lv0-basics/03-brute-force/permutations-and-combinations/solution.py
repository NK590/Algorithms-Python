"""순열과 조합 나열하기 — 모든 경우를 빠짐없이, 중복 없이 만들어 내기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 순열: 순서가 있는 선택 (n 개 중 r 개를 순서대로 줄 세우기), 조합: 순서가 없는 선택
- 결과는 파이썬 itertools 와 같은 순서(입력 위치 기준 사전순)로 나옵니다.
- 직접 실행하면 `N M` 을 받아 1..N 중 M 개를 고른 순열을 사전순으로 한 줄씩 출력합니다.
"""
import sys


def permutations(items: list, r: int | None = None) -> list:
    """items 에서 r 개를 순서대로 뽑는 모든 경우. 이미 쓴 위치를 표시(used)하며 한 자리씩 채운다."""
    r = len(items) if r is None else r
    result = []
    chosen = []
    used = [False] * len(items)

    def fill():
        if len(chosen) == r:
            result.append(tuple(chosen))
            return
        for i, item in enumerate(items):
            if not used[i]:
                used[i] = True
                chosen.append(item)
                fill()
                chosen.pop()  # 되돌리기: 다음 후보를 시도하기 전에 선택을 취소한다
                used[i] = False

    fill()
    return result


def combinations(items: list, r: int) -> list:
    """items 에서 순서 없이 r 개를 뽑는 모든 경우. 항상 앞 위치에서 뒤 위치로만 고르면 같은 조합을 두 번 만들지 않는다."""
    result = []
    chosen = []

    def pick(start: int):
        if len(chosen) == r:
            result.append(tuple(chosen))
            return
        for i in range(start, len(items)):
            chosen.append(items[i])
            pick(i + 1)  # 다음에는 i 보다 뒤의 위치만 고를 수 있다
            chosen.pop()

    pick(0)
    return result


def unique_permutations(items: list) -> list:
    """값이 중복된 items 에서 서로 다른 순열만 사전순으로. 정렬한 뒤, 같은 값은 앞의 것이 쓰인 뒤에만 쓰게 한다."""
    items = sorted(items)
    result = []
    chosen = []
    used = [False] * len(items)

    def fill():
        if len(chosen) == len(items):
            result.append(tuple(chosen))
            return
        for i in range(len(items)):
            if used[i]:
                continue
            if i > 0 and items[i] == items[i - 1] and not used[i - 1]:
                continue  # 같은 값은 앞의 것부터 쓴다. 그렇지 않으면 같은 순열이 중복해서 나온다
            used[i] = True
            chosen.append(items[i])
            fill()
            chosen.pop()
            used[i] = False

    fill()
    return result


def next_permutation(arr: list) -> bool:
    """arr 를 사전순으로 다음 순열로 바꾼다. 마지막 순열이면 바꾸지 않고 False 를 반환한다. O(n)."""
    i = len(arr) - 2
    while i >= 0 and arr[i] >= arr[i + 1]:  # 뒤에서부터 처음으로 오름차순이 깨지는 곳
        i -= 1
    if i < 0:
        return False
    j = len(arr) - 1
    while arr[j] <= arr[i]:  # i 보다 큰 값 중 가장 오른쪽(= 가장 작은) 것
        j -= 1
    arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1:] = reversed(arr[i + 1:])  # 뒤쪽은 내림차순이었으므로 뒤집어 가장 작은 순서로 만든다
    return True


def subsets(items: list) -> list:
    """모든 부분집합 (2^n 개). 각 원소를 넣거나 넣지 않는 두 갈래를 모두 간다."""
    result = []
    chosen = []

    def decide(i: int):
        if i == len(items):
            result.append(tuple(chosen))
            return
        decide(i + 1)  # i 번째를 넣지 않는 경우
        chosen.append(items[i])
        decide(i + 1)  # 넣는 경우
        chosen.pop()

    decide(0)
    return result


def main() -> None:
    n, m = map(int, sys.stdin.readline().split())
    print("\n".join(" ".join(map(str, p)) for p in permutations(list(range(1, n + 1)), m)))


if __name__ == "__main__":
    main()
