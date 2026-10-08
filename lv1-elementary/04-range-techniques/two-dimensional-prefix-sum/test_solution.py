"""solution.py 검증: 직사각형을 직접 더한 값과 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_grid(rng, max_side=6):
    rows, cols = rng.randint(1, max_side), rng.randint(1, max_side)
    return [[rng.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]


def test_readme_example():
    grid = [[1, 2, 4], [3, 4, 5], [5, 6, 7]]
    prefix = solution.build_prefix_2d(grid)
    assert prefix == [[0, 0, 0, 0], [0, 1, 3, 7], [0, 4, 10, 19], [0, 9, 21, 37]]
    assert solution.rect_sum(prefix, 1, 1, 2, 2) == 22  # 4 + 5 + 6 + 7
    assert solution.rect_sum(prefix, 0, 0, 2, 2) == 37
    assert solution.rect_sum(prefix, 2, 0, 2, 0) == 5


def test_every_rectangle_matches_direct_sum():
    rng = random.Random(0)
    for _ in range(100):
        grid = random_grid(rng)
        prefix = solution.build_prefix_2d(grid)
        rows, cols = len(grid), len(grid[0])
        for r1 in range(rows):
            for r2 in range(r1, rows):
                for c1 in range(cols):
                    for c2 in range(c1, cols):
                        expected = sum(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))
                        assert solution.rect_sum(prefix, r1, c1, r2, c2) == expected


def test_best_square_sum_matches_brute_force():
    rng = random.Random(1)
    for _ in range(200):
        grid = random_grid(rng)
        k = rng.randint(1, min(len(grid), len(grid[0])))
        expected = max(
            sum(grid[r + i][c + j] for i in range(k) for j in range(k))
            for r in range(len(grid) - k + 1) for c in range(len(grid[0]) - k + 1))
        assert solution.best_square_sum(grid, k) == expected


def test_large_grid():
    n = 400
    grid = [[1] * n for _ in range(n)]
    prefix = solution.build_prefix_2d(grid)
    assert solution.rect_sum(prefix, 10, 20, 109, 219) == 100 * 200


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 3\n1 2 4\n3 4 5\n5 6 7\n2\n2 2 3 3\n1 1 3 3\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["22", "37"]
