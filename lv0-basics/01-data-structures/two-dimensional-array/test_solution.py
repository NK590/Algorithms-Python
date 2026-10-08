"""solution.py 검증: 손으로 확인한 예제 + zip 기반 기준 구현과의 랜덤 비교 + 나선 격자의 성질"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_grid(rng, max_side=6):
    rows, cols = rng.randint(1, max_side), rng.randint(1, max_side)
    return [[rng.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]


def test_make_grid_rows_are_independent():
    grid = solution.make_grid(2, 3, 0)
    grid[0][1] = 5
    assert grid == [[0, 5, 0], [0, 0, 0]]


def test_make_grid_wrong_shares_rows():
    grid = solution.make_grid_wrong(2, 3, 0)
    grid[0][1] = 5
    assert grid == [[0, 5, 0], [0, 5, 0]]  # 모든 행이 같은 리스트라서 함께 바뀐다


def test_transpose_example_and_involution():
    assert solution.transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    rng = random.Random(0)
    for _ in range(200):
        grid = random_grid(rng)
        assert solution.transpose(grid) == [list(col) for col in zip(*grid)]
        assert solution.transpose(solution.transpose(grid)) == grid


def test_rotate_clockwise_example_and_four_turns():
    assert solution.rotate_clockwise([[1, 2, 3], [4, 5, 6]]) == [[4, 1], [5, 2], [6, 3]]
    rng = random.Random(1)
    for _ in range(200):
        grid = random_grid(rng)
        expected = [list(row) for row in zip(*grid[::-1])]
        assert solution.rotate_clockwise(grid) == expected
        turned = grid
        for _ in range(4):
            turned = solution.rotate_clockwise(turned)
        assert turned == grid


def test_neighbors_stay_inside_the_grid():
    assert sorted(solution.neighbors(0, 0, 3, 3)) == [(0, 1), (1, 0)]
    assert sorted(solution.neighbors(1, 1, 3, 3)) == [(0, 1), (1, 0), (1, 2), (2, 1)]
    assert solution.neighbors(0, 0, 1, 1) == []
    for r in range(4):
        for c in range(5):
            for nr, nc in solution.neighbors(r, c, 4, 5):
                assert 0 <= nr < 4 and 0 <= nc < 5 and abs(nr - r) + abs(nc - c) == 1


def test_spiral_grid_example():
    assert solution.spiral_grid(3, 3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    assert solution.spiral_grid(1, 4) == [[1, 2, 3, 4]]
    assert solution.spiral_grid(4, 1) == [[1], [2], [3], [4]]


def test_spiral_grid_numbers_are_consecutive_neighbors():
    for rows in range(1, 8):
        for cols in range(1, 8):
            grid = solution.spiral_grid(rows, cols)
            position = {grid[r][c]: (r, c) for r in range(rows) for c in range(cols)}
            assert sorted(position) == list(range(1, rows * cols + 1))
            assert position[1] == (0, 0)
            for k in range(1, rows * cols):  # k 와 k+1 은 항상 이웃한 칸이다
                assert position[k + 1] in solution.neighbors(*position[k], rows, cols)


def test_row_and_column_sums():
    assert solution.row_and_column_sums([[1, 2, 3], [4, 5, 6]]) == ([6, 15], [5, 7, 9])
    assert solution.row_and_column_sums([]) == ([], [])


def test_main_prints_transpose(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2\n1 2\n3 4\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["1 3", "2 4"]
