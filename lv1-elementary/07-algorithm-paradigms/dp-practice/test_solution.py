"""solution.py 검증: 모든 부분 구간·부분 수열·부분집합·경로를 직접 나열한 결과와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_max_subarray_sum_matches_all_subarrays():
    rng = random.Random(0)
    for _ in range(400):
        numbers = [rng.randint(-9, 9) for _ in range(rng.randint(1, 10))]
        expected = max(sum(numbers[i:j]) for i in range(len(numbers)) for j in range(i + 1, len(numbers) + 1))
        assert solution.max_subarray_sum(numbers) == expected, numbers
    assert solution.max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solution.max_subarray_sum([-3, -1, -2]) == -1  # 모두 음수면 가장 큰 수 하나
    assert solution.max_subarray_sum([5]) == 5


def longest_increasing_by_enumeration(numbers):
    best = 0
    for mask in range(1 << len(numbers)):
        picked = [numbers[i] for i in range(len(numbers)) if mask >> i & 1]
        if all(a < b for a, b in zip(picked, picked[1:])):
            best = max(best, len(picked))
    return best


def is_subsequence(small, big):
    it = iter(big)
    return all(x in it for x in small)


def test_lis_matches_enumeration_and_sequence_is_valid():
    rng = random.Random(1)
    for _ in range(300):
        numbers = [rng.randint(1, 8) for _ in range(rng.randint(0, 10))]
        expected = longest_increasing_by_enumeration(numbers)
        assert solution.lis_length(numbers) == expected, numbers
        sequence = solution.lis_sequence(numbers)
        assert len(sequence) == expected
        assert all(a < b for a, b in zip(sequence, sequence[1:]))
        assert is_subsequence(sequence, numbers)
    assert solution.lis_length([10, 20, 10, 30, 20, 50]) == 4
    assert solution.lis_sequence([10, 20, 10, 30, 20, 50]) == [10, 20, 30, 50]
    assert solution.lis_length([]) == 0 and solution.lis_sequence([]) == []
    assert solution.lis_length([5, 5, 5]) == 1  # 같은 값은 증가가 아니다


def test_rob_houses_matches_subsets_without_neighbors():
    rng = random.Random(2)
    for _ in range(300):
        money = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
        best = 0
        for mask in range(1 << len(money)):
            if mask & (mask >> 1):
                continue  # 이웃한 두 집을 함께 텀
            best = max(best, sum(money[i] for i in range(len(money)) if mask >> i & 1))
        assert solution.rob_houses(money) == best, money
    assert solution.rob_houses([2, 7, 9, 3, 1]) == 12
    assert solution.rob_houses([]) == 0


def stairs_by_enumeration(scores):
    n = len(scores)
    best = None
    for mask in range(1 << n):
        stepped = [i for i in range(n) if mask >> i & 1]
        if not stepped or stepped[-1] != n - 1 or stepped[0] > 1:
            continue
        if any(b - a > 2 for a, b in zip(stepped, stepped[1:])):
            continue
        if any(i in stepped and i + 1 in stepped and i + 2 in stepped for i in range(n)):
            continue
        total = sum(scores[i] for i in stepped)
        best = total if best is None else max(best, total)
    return best


def test_stairs_max_score_matches_enumeration():
    rng = random.Random(3)
    for _ in range(300):
        scores = [rng.randint(1, 9) for _ in range(rng.randint(1, 10))]
        assert solution.stairs_max_score(scores) == stairs_by_enumeration(scores), scores
    assert solution.stairs_max_score([10, 20, 15, 25, 10, 20]) == 75
    assert solution.stairs_max_score([7]) == 7
    assert solution.stairs_max_score([5, 8]) == 13
    assert solution.stairs_max_score([]) == 0


def all_grid_paths(grid):
    rows, cols = len(grid), len(grid[0])

    def walk(r, c):
        if (r, c) == (rows - 1, cols - 1):
            yield [(r, c)]
            return
        for dr, dc in ((1, 0), (0, 1)):
            nr, nc = r + dr, c + dc
            if nr < rows and nc < cols:
                for rest in walk(nr, nc):
                    yield [(r, c)] + rest

    return walk(0, 0)


def test_min_path_sum_matches_all_paths():
    rng = random.Random(4)
    for _ in range(200):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        grid = [[rng.randint(0, 9) for _ in range(cols)] for _ in range(rows)]
        expected = min(sum(grid[r][c] for r, c in path) for path in all_grid_paths(grid))
        assert solution.min_path_sum(grid) == expected, grid
    assert solution.min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert solution.min_path_sum([[4]]) == 4


def test_triangle_max_path_matches_all_paths():
    rng = random.Random(5)
    for _ in range(200):
        height = rng.randint(1, 7)
        triangle = [[rng.randint(0, 9) for _ in range(r + 1)] for r in range(height)]

        def best(r, c):
            if r == height - 1:
                return triangle[r][c]
            return triangle[r][c] + max(best(r + 1, c), best(r + 1, c + 1))

        assert solution.triangle_max_path(triangle) == best(0, 0), triangle
    assert solution.triangle_max_path([[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]) == 30
    assert solution.triangle_max_path([[5]]) == 5


def test_count_paths_matches_all_paths():
    rng = random.Random(6)
    for _ in range(300):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        grid = [[1 if rng.random() < 0.25 else 0 for _ in range(cols)] for _ in range(rows)]
        expected = sum(1 for path in all_grid_paths(grid) if all(grid[r][c] == 0 for r, c in path))
        assert solution.count_paths(grid) == expected, grid
    assert solution.count_paths([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert solution.count_paths([[0] * 3 for _ in range(3)]) == 6
    assert solution.count_paths([[1, 0], [0, 0]]) == 0 and solution.count_paths([[0, 0], [0, 1]]) == 0


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("9\n-2 1 -3 4 -1 2 1 -5 4\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "6"
