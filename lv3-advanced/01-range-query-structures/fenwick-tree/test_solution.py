"""solution.py 검증: 리스트를 직접 갱신·합산하는 순진한 방법과 무작위 질의로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_matches_plain_list_under_random_operations():
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 20)
        values = [rng.randint(-9, 9) for _ in range(n)]
        fenwick = solution.FenwickTree(n)
        for i, v in enumerate(values):
            fenwick.add(i, v)
        for _ in range(40):
            if n and rng.random() < 0.5:
                i, d = rng.randrange(n), rng.randint(-9, 9)
                values[i] += d
                fenwick.add(i, d)
            left = rng.randint(0, n)
            right = rng.randint(left, n)
            assert fenwick.range_sum(left, right) == sum(values[left:right]), (values, left, right)
            assert fenwick.prefix_sum(right) == sum(values[:right])


def test_from_list_equals_adding_one_by_one():
    rng = random.Random(1)
    for _ in range(200):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        one_by_one = solution.FenwickTree(len(values))
        for i, v in enumerate(values):
            one_by_one.add(i, v)
        assert solution.FenwickTree.from_list(values).tree == one_by_one.tree, values


def test_tree_layout_follows_lowbit():
    fenwick = solution.FenwickTree.from_list([1] * 8)
    # tree[i] 는 i 에서 끝나는 길이 lowbit(i) 구간의 합이다
    assert fenwick.tree[1:] == [1, 2, 1, 4, 1, 2, 1, 8]


def test_set_and_point_value():
    fenwick = solution.FenwickTree.from_list([5, 5, 5])
    fenwick.set(1, 9)
    fenwick.set(1, 9)  # 같은 값으로 다시 써도 변하지 않는다
    assert [fenwick.point_value(i) for i in range(3)] == [5, 9, 5]
    assert fenwick.range_sum(0, 3) == 19


def test_find_kth_matches_linear_scan_on_counts():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 25)
        counts = [rng.randint(0, 3) for _ in range(n)]
        fenwick = solution.FenwickTree.from_list(counts)
        total = sum(counts)
        for k in range(-1, total + 3):
            expected = n
            running = 0
            for i, c in enumerate(counts):
                running += c
                if running >= k:
                    expected = i
                    break
            assert fenwick.find_kth(k) == expected, (counts, k)
    # 작은 예: 개수 [2, 0, 3] → 1~2 번째는 위치 0, 3~5 번째는 위치 2
    counts = solution.FenwickTree.from_list([2, 0, 3])
    assert [counts.find_kth(k) for k in range(1, 7)] == [0, 0, 2, 2, 2, 3]


def test_range_add_range_sum_matches_plain_list():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 20)
        values = [0] * n
        fenwick = solution.RangeAddFenwick(n)
        for _ in range(40):
            left = rng.randint(0, n)
            right = rng.randint(left, n)
            if rng.random() < 0.5:
                d = rng.randint(-9, 9)
                for i in range(left, right):
                    values[i] += d
                fenwick.range_add(left, right, d)
            assert fenwick.range_sum(left, right) == sum(values[left:right]), (left, right)
            assert fenwick.prefix_sum(right) == sum(values[:right])


def test_fenwick_2d_matches_plain_grid():
    rng = random.Random(4)
    for _ in range(100):
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        grid = [[0] * cols for _ in range(rows)]
        fenwick = solution.Fenwick2D(rows, cols)
        for _ in range(40):
            if rng.random() < 0.5:
                r, c, d = rng.randrange(rows), rng.randrange(cols), rng.randint(-9, 9)
                grid[r][c] += d
                fenwick.add(r, c, d)
            r1 = rng.randint(0, rows)
            r2 = rng.randint(r1, rows)
            c1 = rng.randint(0, cols)
            c2 = rng.randint(c1, cols)
            expected = sum(grid[r][c] for r in range(r1, r2) for c in range(c1, c2))
            assert fenwick.rect_sum(r1, c1, r2, c2) == expected, (r1, c1, r2, c2)


def test_count_inversions_matches_all_pairs():
    rng = random.Random(5)
    for _ in range(300):
        numbers = [rng.randint(-5, 5) for _ in range(rng.randint(0, 15))]
        expected = sum(1 for i in range(len(numbers)) for j in range(i + 1, len(numbers)) if numbers[i] > numbers[j])
        assert solution.count_inversions(numbers) == expected, numbers
    assert solution.count_inversions([3, 1, 2]) == 2
    assert solution.count_inversions(list(range(10))) == 0
    assert solution.count_inversions(list(range(10, 0, -1))) == 45  # 완전히 뒤집힌 수열은 n(n-1)/2


def test_count_smaller_after_matches_all_pairs():
    rng = random.Random(6)
    for _ in range(300):
        numbers = [rng.randint(-5, 5) for _ in range(rng.randint(0, 15))]
        expected = [sum(1 for j in range(i + 1, len(numbers)) if numbers[j] < numbers[i]) for i in range(len(numbers))]
        assert solution.count_smaller_after(numbers) == expected, numbers
    assert solution.count_smaller_after([5, 2, 6, 1]) == [2, 1, 1, 0]


def test_large_input_is_fast():
    rng = random.Random(7)
    n = 200_000
    fenwick = solution.FenwickTree.from_list([1] * n)
    for _ in range(100_000):
        i = rng.randrange(n)
        fenwick.add(i, 1)
        assert fenwick.range_sum(0, n) >= n
    assert fenwick.range_sum(0, n) == n + 100_000
    numbers = [rng.randint(0, 10**9) for _ in range(100_000)]
    assert 0 <= solution.count_inversions(numbers) <= 100_000 * 99_999 // 2


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"5 2 2\n1\n2\n3\n4\n5\n1 3 6\n2 2 5\n1 5 2\n2 3 5\n")))
    solution.main()
    assert capsys.readouterr().out.split() == ["17", "12"]
