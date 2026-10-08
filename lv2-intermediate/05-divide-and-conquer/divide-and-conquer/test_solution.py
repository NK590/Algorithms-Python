"""solution.py 검증: 느리지만 확실한 O(n²) / 전수 열거 방법과 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_max_subarray_matches_all_subarrays():
    rng = random.Random(0)
    for _ in range(500):
        numbers = [rng.randint(-9, 9) for _ in range(rng.randint(1, 20))]
        expected = max(sum(numbers[i:j]) for i in range(len(numbers)) for j in range(i + 1, len(numbers) + 1))
        assert solution.max_subarray_dc(numbers) == expected, numbers
    assert solution.max_subarray_dc([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solution.max_subarray_dc([-3, -1, -2]) == -1 and solution.max_subarray_dc([5]) == 5


def test_count_inversions_matches_pairwise_count():
    rng = random.Random(1)
    for _ in range(500):
        numbers = [rng.randint(0, 9) for _ in range(rng.randint(0, 25))]
        expected = sum(1 for i, j in itertools.combinations(range(len(numbers)), 2) if numbers[i] > numbers[j])
        assert solution.count_inversions_dc(numbers) == expected, numbers
    assert solution.count_inversions_dc([2, 4, 1, 3, 5]) == 3
    assert solution.count_inversions_dc(list(range(10, 0, -1))) == 45  # 완전히 뒤집힘: n(n-1)/2
    assert solution.count_inversions_dc([]) == 0 and solution.count_inversions_dc([3, 3]) == 0  # 같은 값은 역전이 아니다


def test_count_inversions_does_not_modify_input_and_is_fast():
    numbers = list(range(50_000, 0, -1))
    copy = numbers[:]
    assert solution.count_inversions_dc(numbers) == 50_000 * 49_999 // 2
    assert numbers == copy


def test_closest_pair_matches_all_pairs():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(2, 30)
        points = [(rng.randint(0, 40), rng.randint(0, 40)) for _ in range(n)]
        expected = min((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in itertools.combinations(points, 2))
        assert solution.closest_pair_squared(points) == expected, points
    assert solution.closest_pair_squared([(0, 0), (3, 4)]) == 25
    assert solution.closest_pair_squared([(1, 1), (1, 1), (5, 5)]) == 0  # 같은 점이 두 번


def test_closest_pair_large_input():
    rng = random.Random(3)
    points = [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(20_000)]
    result = solution.closest_pair_squared(points)
    # 격자로 나눠 가까운 후보만 비교하는 독립적인 방법
    cell = 5000
    grid = {}
    for p in points:
        grid.setdefault((p[0] // cell, p[1] // cell), []).append(p)
    best = None
    for (gx, gy), pts in grid.items():
        near = [q for dx in (-1, 0, 1) for dy in (-1, 0, 1) for q in grid.get((gx + dx, gy + dy), [])]
        for p in pts:
            for q in near:
                if p is not q:
                    d = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
                    best = d if best is None else min(best, d)
    assert result == best


def z_order_by_enumeration(n):
    """2ⁿ × 2ⁿ 의 방문 순서를 재귀로 직접 펼친 표"""
    order = {}
    counter = 0

    def visit(r, c, size):
        nonlocal counter
        if size == 1:
            order[(r, c)] = counter
            counter += 1
            return
        half = size // 2
        for dr, dc in ((0, 0), (0, 1), (1, 0), (1, 1)):
            visit(r + dr * half, c + dc * half, half)

    visit(0, 0, 1 << n)
    return order


def test_z_order_matches_full_enumeration():
    for n in range(0, 6):
        order = z_order_by_enumeration(n)
        for (r, c), index in order.items():
            assert solution.z_order_index(n, r, c) == index, (n, r, c)
    assert solution.z_order_index(2, 3, 1) == 11 and solution.z_order_index(3, 7, 7) == 63
    assert solution.z_order_index(10, 511, 511) == 262143


def test_quad_tree_compression():
    assert solution.quad_tree(["0"]) == "0"
    assert solution.quad_tree(["11", "11"]) == "1"
    assert solution.quad_tree(["01", "11"]) == "(0111)"
    image = ["11110000", "11110000", "00011100", "00011100", "11110000", "11110000", "11110011", "11110011"]
    assert solution.quad_tree(image) == "((110(0101))(0010)1(0001))"
    assert solution.quad_tree([]) == ""


def decompress(code, size):
    """quad_tree 의 역: 괄호 문자열을 다시 영상으로 되돌려 왕복이 맞는지 본다"""
    grid = [["?"] * size for _ in range(size)]
    pos = 0

    def parse(r, c, s):
        nonlocal pos
        if code[pos] != "(":
            ch = code[pos]
            pos += 1
            for i in range(r, r + s):
                for j in range(c, c + s):
                    grid[i][j] = ch
            return
        pos += 1
        h = s // 2
        for dr, dc in ((0, 0), (0, 1), (1, 0), (1, 1)):
            parse(r + dr * h, c + dc * h, h)
        assert code[pos] == ")"
        pos += 1

    parse(0, 0, size)
    return ["".join(row) for row in grid]


def test_quad_tree_round_trips():
    rng = random.Random(4)
    for _ in range(100):
        size = rng.choice([1, 2, 4, 8])
        grid = ["".join(rng.choice("0011") for _ in range(size)) for _ in range(size)]
        assert decompress(solution.quad_tree(grid), size) == grid, grid


def test_count_uniform_regions():
    grid = [[0, 0, 0, 1, 1, 1, -1, -1, -1]] * 3 + [[1, 1, 1, 0, 0, 0, 0, 0, 0]] * 3 + [[0, 1, -1, 0, 1, -1, 0, 1, -1]] * 3
    counts = solution.count_uniform_regions(grid)
    assert counts == {0: 12, 1: 11, -1: 10}
    assert solution.count_uniform_regions([[5]]) == {5: 1}
    assert solution.count_uniform_regions([]) == {}


def test_count_uniform_regions_matches_independent_count():
    rng = random.Random(5)
    for _ in range(100):
        size = rng.choice([1, 3, 9])
        grid = [[rng.choice([-1, 0, 1]) for _ in range(size)] for _ in range(size)]

        def count(r, c, s):
            cells = [grid[i][j] for i in range(r, r + s) for j in range(c, c + s)]
            if len(set(cells)) == 1:
                return {cells[0]: 1}
            total = {}
            t = s // 3
            for dr in range(3):
                for dc in range(3):
                    for k, v in count(r + dr * t, c + dc * t, t).items():
                        total[k] = total.get(k, 0) + v
            return total

        assert solution.count_uniform_regions(grid) == count(0, 0, size)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 7 7\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "63"
