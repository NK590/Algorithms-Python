"""solution.py 검증: 게임 트리를 끝까지 탐색하는 승패 계산(미니맥스)과 비교하고 그런디 수·XOR 규칙·이기는 수를 확인"""
import io
import itertools
import random
from functools import lru_cache

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def wins(position, moves):
    """일반 규칙 미니맥스: 위치에서 움직일 차례인 사람이 이기는가 (갈 수 있는 위치 중 지는 위치가 있으면 이긴다)."""

    @lru_cache(maxsize=None)
    def first_wins(state):
        return any(not first_wins(nxt) for nxt in moves(state))

    return first_wins(position)


def subtraction_moves(allowed):
    def moves(state):
        return [tuple(sorted(state[:i] + (state[i] - m,) + state[i + 1 :])) for i in range(len(state)) for m in allowed if m <= state[i]]

    return moves


def test_mex():
    assert solution.mex([]) == 0 and solution.mex([1, 2]) == 0 and solution.mex([0, 1, 3]) == 2 and solution.mex(iter([2, 0, 1])) == 3


def test_subtraction_game_grundy_zero_iff_losing_and_matches_general_function():
    rng = random.Random(0)
    for _ in range(200):
        allowed = sorted(rng.sample(range(1, 8), rng.randint(1, 4)))
        n = rng.randint(0, 30)
        grundy = solution.grundy_subtraction(n, allowed)
        for size in range(n + 1):
            assert (grundy[size] != 0) == wins((size,), subtraction_moves(allowed)), (allowed, size)
            assert grundy[size] == solution.grundy_of(size, lambda s: [s - m for m in allowed if m <= s]), (allowed, size)
    assert solution.grundy_subtraction(10, [1, 2, 3]) == [i % 4 for i in range(11)]
    assert solution.grundy_subtraction(0, [1]) == [0]


def test_sum_of_games_is_won_exactly_when_xor_is_nonzero():
    rng = random.Random(1)
    for _ in range(150):
        allowed = sorted(rng.sample(range(1, 6), rng.randint(1, 3)))
        sizes = tuple(sorted(rng.randint(0, 7) for _ in range(rng.randint(1, 3))))
        grundy = solution.grundy_subtraction(7, allowed)
        assert wins(sizes, subtraction_moves(allowed)) == (solution.nim_sum(grundy[s] for s in sizes) != 0), (allowed, sizes)


def test_nim_winning_move():
    rng = random.Random(2)
    for _ in range(500):
        piles = [rng.randint(0, 9) for _ in range(rng.randint(1, 5))]
        move = solution.nim_winning_move(piles)
        if solution.nim_sum(piles) == 0:
            assert move is None
        else:
            index, new_size = move
            assert 0 <= new_size < piles[index]
            after = list(piles)
            after[index] = new_size
            assert solution.nim_sum(after) == 0
    assert solution.nim_winning_move([]) is None and solution.nim_winning_move([0, 0]) is None
    assert solution.nim_winning_move([3, 4, 5]) == (0, 1)  # 3^4^5 = 2: 앞에서부터 줄어드는 더미는 3 (3 ^ 2 = 1 < 3)


def test_misere_nim_matches_game_search():
    def moves(state):
        return [tuple(sorted(state[:i] + (state[i] - take,) + state[i + 1 :])) for i in range(len(state)) for take in range(1, state[i] + 1)]

    @lru_cache(maxsize=None)
    def first_wins_misere(state):
        if sum(state) == 0:
            return True  # 직전 사람이 마지막 돌을 가져갔으므로 직전 사람이 졌다 = 지금 차례인 사람이 이긴 것
        return any(not first_wins_misere(nxt) for nxt in moves(state))

    for piles in itertools.chain.from_iterable(itertools.combinations_with_replacement(range(0, 5), r) for r in range(1, 5)):
        assert solution.misere_nim_first_player_wins(piles) == first_wins_misere(tuple(sorted(piles))), piles


def octal_moves(code):
    digits = [int(c) for c in code.split(".")[1]]

    def moves(state):
        result = set()
        for i, heap in enumerate(state):
            others = state[:i] + state[i + 1 :]
            for take, digit in enumerate(digits, start=1):
                if take > heap:
                    break
                rest = heap - take
                if digit & 1 and rest == 0:
                    result.add(tuple(sorted(others)))
                if digit & 2 and rest > 0:
                    result.add(tuple(sorted(others + (rest,))))
                if digit & 4 and rest >= 2:
                    for left in range(1, rest // 2 + 1):
                        result.add(tuple(sorted(others + (left, rest - left))))
        return list(result)

    return moves


def test_octal_games_match_game_search():
    for code in ["0.77", "0.07", "0.7", "0.137", "0.6", "0.15", "0.04", "0.3"]:
        grundy = solution.octal_game_grundy(code, 12)
        moves = octal_moves(code)
        for size in range(13):
            assert (grundy[size] != 0) == wins((size,) if size else (), moves), (code, size)
            assert grundy[size] == solution.grundy_of((size,) if size else (), moves) , (code, size)
        for heaps in itertools.chain.from_iterable(itertools.combinations_with_replacement(range(1, 8), r) for r in range(2, 4)):
            assert wins(heaps, moves) == (solution.nim_sum(grundy[h] for h in heaps) != 0), (code, heaps)


def test_known_kayles_and_dawson_values():
    assert solution.kayles_grundy(23) == [0, 1, 2, 3, 1, 4, 3, 2, 1, 4, 2, 6, 4, 1, 2, 7, 1, 4, 3, 2, 1, 4, 6, 7]
    assert solution.dawsons_kayles_grundy(10) == [0, 0, 1, 1, 2, 0, 3, 1, 1, 0, 3]
    assert solution.octal_game_grundy("0.6", 0) == [0]


def test_winning_move_in_sum_finds_a_zero_xor_position():
    rng = random.Random(3)
    for _ in range(200):
        allowed = sorted(rng.sample(range(1, 6), rng.randint(1, 3)))
        sizes = [rng.randint(0, 12) for _ in range(rng.randint(1, 4))]
        grundy = solution.grundy_subtraction(12, allowed)
        move = solution.winning_move_in_sum(sizes, lambda s: grundy[s], lambda s: [s - m for m in allowed if m <= s])
        total = solution.nim_sum(grundy[s] for s in sizes)
        if total == 0:
            assert move is None
        else:
            index, new_size = move
            assert new_size in [sizes[index] - m for m in allowed if m <= sizes[index]]
            after = list(sizes)
            after[index] = new_size
            assert solution.nim_sum(grundy[s] for s in after) == 0


def test_grundy_of_handles_deep_games_without_recursion():
    assert solution.grundy_of(100000, lambda s: [s - 1] if s > 0 else []) == 100000 % 2
    assert solution.grundy_of("start", lambda s: []) == 0


def test_main_nim_game_format(monkeypatch, capsys):
    for text, expected in [("3\n1 2 3\n", "cubelover"), ("2\n1 2\n", "koosaga"), ("1\n5\n", "koosaga")]:
        monkeypatch.setattr("sys.stdin", io.StringIO(text))
        solution.main()
        assert capsys.readouterr().out.strip() == expected
