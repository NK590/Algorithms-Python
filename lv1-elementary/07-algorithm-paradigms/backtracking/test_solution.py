"""solution.py 검증: itertools / 전수 탐색 / 카탈란 수 / 알려진 N-Queens 값과 비교"""
import io
import itertools
import math

from tools.loader import load_solution

solution = load_solution(__file__)


def test_pick_permutations_matches_itertools_in_order():
    for n in range(0, 6):
        for m in range(0, n + 1):
            assert solution.pick_permutations(n, m) == list(itertools.permutations(range(1, n + 1), m)), (n, m)
    assert solution.pick_permutations(3, 2) == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]


def test_pick_combinations_matches_itertools_in_order():
    for n in range(0, 8):
        for m in range(0, n + 1):
            assert solution.pick_combinations(n, m) == list(itertools.combinations(range(1, n + 1), m)), (n, m)
    assert solution.pick_combinations(4, 2) == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert solution.pick_combinations(3, 5) == []


def test_all_subsets():
    assert sorted(map(tuple, solution.all_subsets([1, 2, 3]))) == sorted(
        c for r in range(4) for c in itertools.combinations([1, 2, 3], r)
    )
    assert solution.all_subsets([]) == [[]]
    assert len(solution.all_subsets(list(range(10)))) == 2**10
    assert solution.all_subsets([7]) == [[], [7]]


def test_n_queens_matches_known_counts():
    known = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352}
    for n, count in known.items():
        assert solution.n_queens_count(n) == count, n


def test_n_queens_matches_brute_force_over_permutations():
    for n in range(1, 8):
        brute = sum(
            1
            for perm in itertools.permutations(range(n))
            if all(abs(perm[i] - perm[j]) != j - i for i in range(n) for j in range(i + 1, n))
        )
        assert solution.n_queens_count(n) == brute, n


def test_n_queens_first_is_valid_and_lexicographically_first():
    assert solution.n_queens_first(2) is None and solution.n_queens_first(3) is None
    assert solution.n_queens_first(4) == [1, 3, 0, 2]
    for n in (1, 4, 5, 6, 7, 8):
        placement = solution.n_queens_first(n)
        assert sorted(placement) == list(range(n))
        assert all(abs(placement[i] - placement[j]) != j - i for i in range(n) for j in range(i + 1, n))
        first = next(
            list(p) for p in itertools.permutations(range(n)) if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n))
        )
        assert placement == first


def count_valid_partial_placements(n):
    """앞의 r 행에 퀸 r 개를 서로 공격하지 못하게 놓은 배치의 수를 r = 1..n 에 대해 모두 더한다 (독립적인 전수 계산)"""
    total = 0
    for r in range(1, n + 1):
        total += sum(
            1
            for cols in itertools.product(range(n), repeat=r)
            if all(cols[i] != cols[j] and abs(cols[i] - cols[j]) != j - i for i in range(r) for j in range(i + 1, r))
        )
    return total


def test_pruning_visits_far_fewer_states_than_exhaustive_search():
    for n in range(1, 7):
        assert solution.n_queens_nodes(n) == count_valid_partial_placements(n), n
    # 8 퀸: 퀸을 놓은 횟수 2056 (빈 판까지 세면 2057). 순열을 모두 만들어 보는 8! = 40,320 보다 훨씬 적다
    assert solution.n_queens_nodes(8) == 2056
    assert solution.n_queens_nodes(8) < math.factorial(8)


def test_generate_parentheses_matches_catalan_and_brute_force():
    def balanced(s):
        depth = 0
        for ch in s:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                return False
        return depth == 0

    for n in range(0, 8):
        result = solution.generate_parentheses(n)
        assert len(result) == math.comb(2 * n, n) // (n + 1)
        assert result == sorted(result)
        if n <= 5:
            brute = sorted("".join(p) for p in itertools.product("()", repeat=2 * n) if balanced(p))
            assert result == brute
    assert solution.generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def is_valid_solution(board, puzzle):
    full = set(range(1, 10))
    for r in range(9):
        assert set(board[r]) == full
        assert {board[i][r] for i in range(9)} == full
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            assert {board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)} == full
    for r in range(9):
        for c in range(9):
            if puzzle[r][c]:
                assert board[r][c] == puzzle[r][c]


def test_solve_sudoku():
    original = [row[:] for row in PUZZLE]
    board = solution.solve_sudoku(PUZZLE)
    assert PUZZLE == original  # 입력은 바뀌지 않는다
    is_valid_solution(board, PUZZLE)
    assert board[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]


def test_solve_sudoku_already_complete_and_unsolvable():
    solved = solution.solve_sudoku(PUZZLE)
    assert solution.solve_sudoku(solved) == solved
    bad = [row[:] for row in PUZZLE]
    bad[0][2] = 5  # 첫 행에 5 가 두 번
    assert solution.solve_sudoku(bad) is None
    # 같은 3×3 상자 안에만 중복이 있는 경우 (행·열은 겹치지 않는다)
    in_box = [[0] * 9 for _ in range(9)]
    in_box[0][0] = in_box[1][1] = 5
    assert solution.solve_sudoku(in_box) is None
    # 규칙은 어기지 않지만 풀 수 없는 경우: (0,0) 에 들어갈 수가 없다
    stuck = [[0] * 9 for _ in range(9)]
    stuck[0][1:9] = [1, 2, 3, 4, 5, 6, 7, 8]
    stuck[1][0] = 9
    assert solution.solve_sudoku(stuck) is None


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
