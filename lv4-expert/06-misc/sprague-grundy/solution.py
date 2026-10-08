"""스프라그-그런디 정리(Sprague–Grundy) — 공정(impartial) 게임의 합을 그런디 수의 XOR 하나로 분석하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 공정 게임: 두 사람이 번갈아 움직이고, 어느 위치에서든 두 사람의 가능한 수가 같으며, 더 움직일 수 없는 사람이 진다 (정상 규칙).
- 그런디 수 g(P) = mex{ g(Q) : P 에서 한 수로 Q 에 간다 }  (mex = 집합에 없는 가장 작은 음이 아닌 정수). g(P) = 0 ⟺ P 는 진다(P-위치).
- 정리: 독립된 게임 여러 개의 합(한 번에 한 게임에서만 움직인다)의 그런디 수는 각 그런디 수의 XOR. 그래서 합의 승패는 XOR != 0 인가 하나로 결정된다.
  각 게임은 따로 분석하면 되고, 이기는 수는 XOR 를 0 으로 만드는 한 성분의 수를 찾아 고르면 된다.
- 여기서 제공하는 것: mex, grundy_subtraction(뺄셈 게임), grundy_of(일반 게임: 위치에서 다음 위치들을 돌려주는 함수, 반복형 메모), nim_sum / nim_winning_move,
  misere_nim_first_player_wins(마지막에 가져가면 지는 님), octal_game_grundy(8진 게임 코드 — 케일스 0.77, 도슨의 케일스 0.07 등), winning_move_in_sum(합에서 이기는 수 찾기).
- 직접 실행하면 BOJ 11868 형식 — 돌 더미 개수 N 과 각 더미의 크기 — 을 받아 선공이 이기면 koosaga, 지면 cubelover 를 출력합니다.
"""
import sys
from typing import Callable, Hashable, Iterable, Optional, Sequence


def mex(values: Iterable[int]) -> int:
    present = set(values)
    result = 0
    while result in present:
        result += 1
    return result


def grundy_subtraction(n: int, moves: Sequence[int]) -> list[int]:
    """더미 크기 0..n 의 그런디 수. 한 번에 moves 에 있는 개수만큼 가져갈 수 있는 뺄셈 게임."""
    grundy = [0] * (n + 1)
    for size in range(1, n + 1):
        grundy[size] = mex(grundy[size - m] for m in moves if m <= size)
    return grundy


def grundy_of(start: Hashable, next_positions: Callable[[Hashable], Iterable[Hashable]]) -> int:
    """위치 start 의 그런디 수. next_positions(P) 는 P 에서 한 수로 갈 수 있는 위치들 (사이클이 없어야 한다). 반복형 DFS + 메모."""
    memo: dict[Hashable, int] = {}
    stack: list[tuple[Hashable, Optional[list[Hashable]]]] = [(start, None)]
    while stack:
        position, children = stack.pop()
        if position in memo:
            continue
        if children is None:
            children = list(next_positions(position))
            stack.append((position, children))
            stack.extend((child, None) for child in children if child not in memo)
        else:
            memo[position] = mex(memo[child] for child in children)
    return memo[start]


def nim_sum(piles: Iterable[int]) -> int:
    result = 0
    for pile in piles:
        result ^= pile
    return result


def nim_winning_move(piles: Sequence[int]) -> Optional[tuple[int, int]]:
    """님에서 이기는 수 (더미 번호, 그 더미의 새 크기). 이미 지는 위치(XOR = 0)면 None."""
    total = nim_sum(piles)
    if total == 0:
        return None
    for index, pile in enumerate(piles):
        target = pile ^ total
        if target < pile:  # 이 더미를 줄여서 XOR 를 0 으로 만들 수 있다
            return index, target
    raise AssertionError("XOR != 0 이면 반드시 줄일 더미가 있다")


def misere_nim_first_player_wins(piles: Sequence[int]) -> bool:
    """마지막 돌을 가져가는 사람이 지는 님. 크기가 2 이상인 더미가 있으면 일반 님과 같고, 모두 0 또는 1 이면 1 인 더미의 수가 짝수일 때 선공이 이긴다."""
    if any(pile >= 2 for pile in piles):
        return nim_sum(piles) != 0
    return sum(piles) % 2 == 0


def octal_game_grundy(code: str, n: int) -> list[int]:
    """8진 게임의 더미 크기 0..n 의 그런디 수. 코드 "0.d1d2d3…": d_k 의 비트가 더미에서 k 개를 가져갈 때 허용되는 결과를 정한다 —
    1: 더미가 비면(k = 크기) 가능, 2: 하나의 비어 있지 않은 더미가 남으면 가능, 4: 두 개의 비어 있지 않은 더미로 갈라지면 가능.
    예: "0.77" 케일스(핀 1~2 개를 쓰러뜨림), "0.07" 도슨의 케일스."""
    digits = [int(ch) for ch in code.split(".")[1]]
    grundy = [0] * (n + 1)
    for size in range(1, n + 1):
        options = set()
        for take, digit in enumerate(digits, start=1):
            if take > size:
                break
            rest = size - take
            if digit & 1 and rest == 0:
                options.add(0)
            if digit & 2 and rest > 0:
                options.add(grundy[rest])
            if digit & 4 and rest >= 2:
                for left in range(1, rest // 2 + 1):  # 두 더미의 크기 (left, rest - left), 둘 다 1 이상
                    options.add(grundy[left] ^ grundy[rest - left])
        grundy[size] = mex(options)
    return grundy


def kayles_grundy(n: int) -> list[int]:
    return octal_game_grundy("0.77", n)


def dawsons_kayles_grundy(n: int) -> list[int]:
    return octal_game_grundy("0.07", n)


def winning_move_in_sum(
    components: Sequence[Hashable],
    grundy: Callable[[Hashable], int],
    next_positions: Callable[[Hashable], Iterable[Hashable]],
) -> Optional[tuple[int, Hashable]]:
    """게임의 합에서 이기는 수 (성분 번호, 그 성분의 새 위치). 지는 위치면 None. 합의 그런디 수 = 성분들의 XOR 이므로,
    어느 한 성분을 그런디 수가 (전체 XOR 와 그 성분의 그런디 수의 XOR) 인 위치로 옮기면 합이 0 이 된다."""
    values = [grundy(c) for c in components]
    total = nim_sum(values)
    if total == 0:
        return None
    for index, component in enumerate(components):
        target = values[index] ^ total
        if target < values[index]:  # mex 의 정의상 더 작은 그런디 수를 가진 이웃이 반드시 존재한다
            for candidate in next_positions(component):
                if grundy(candidate) == target:
                    return index, candidate
    raise AssertionError("XOR != 0 이면 이기는 수가 있다")


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    print("koosaga" if nim_sum(int(x) for x in data[1 : 1 + n]) else "cubelover")


if __name__ == "__main__":
    main()
