"""solution.py 검증: 서로 다른 방법끼리, 그리고 전수 열거·BFS 와 비교"""
import io
import itertools
import time
from collections import deque

from tools.loader import load_solution

solution = load_solution(__file__)

FIB = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]


def test_fibonacci_versions_agree():
    for n in range(0, 22):
        assert solution.fib_naive(n) == solution.fib_memo(n) == solution.fib_table(n)[n] == solution.fib_fast(n), n
    assert [solution.fib_fast(i) for i in range(16)] == FIB
    assert solution.fib_table(0) == [0] and solution.fib_table(1) == [0, 1]
    assert solution.fib_fast(90) == 2880067194370816120


def test_naive_call_count_formula_and_speed():
    for n in range(0, 20):
        assert solution.fib_naive_calls(n) == 2 * solution.fib_fast(n + 1) - 1, n
    assert solution.fib_naive_calls(30) == 2692537
    # 메모이제이션은 같은 n 을 즉시 푼다 (재귀 깊이가 n 이라 작은 n 으로)
    start = time.perf_counter()
    assert solution.fib_memo(400) == solution.fib_fast(400)
    assert time.perf_counter() - start < 1


def test_fib_memo_does_not_share_state_between_calls():
    assert solution.fib_memo(10) == 55
    assert solution.fib_memo(5) == 5
    memo = {}
    solution.fib_memo(20, memo)
    assert memo[20] == 6765 and len(memo) == 19  # 2..20


def compositions(n, parts=(1, 2)):
    if n == 0:
        return 1
    return sum(compositions(n - p, parts) for p in parts if p <= n)


def test_climb_stairs_matches_enumeration():
    for n in range(0, 16):
        assert solution.climb_stairs(n) == compositions(n), n
    assert [solution.climb_stairs(n) for n in range(1, 7)] == [1, 2, 3, 5, 8, 13]


def count_tilings(n):
    """2×n 격자를 칸 단위로 채우는 백트래킹 (독립 구현)"""
    grid = [[False] * n for _ in range(2)]

    def first_empty():
        for c in range(n):
            for r in range(2):
                if not grid[r][c]:
                    return r, c
        return None

    def fill():
        cell = first_empty()
        if cell is None:
            return 1
        r, c = cell
        total = 0
        # 세로 타일 (이 열을 한 장으로)
        if r == 0 and not grid[1][c]:
            grid[0][c] = grid[1][c] = True
            total += fill()
            grid[0][c] = grid[1][c] = False
        # 가로 타일 (오른쪽 칸과 함께)
        if c + 1 < n and not grid[r][c + 1]:
            grid[r][c] = grid[r][c + 1] = True
            total += fill()
            grid[r][c] = grid[r][c + 1] = False
        return total

    return fill()


def test_tile_2xn_matches_enumeration_and_mod():
    for n in range(1, 11):
        assert solution.tile_2xn(n, mod=10**9) == count_tilings(n), n
    assert solution.tile_2xn(1) == 1 and solution.tile_2xn(2) == 2 and solution.tile_2xn(9) == 55
    assert solution.tile_2xn(1000, mod=10007) == solution.fib_fast(1001) % 10007
    assert solution.tile_2xn(0) == 1


def test_tile_2xn_applies_mod_each_step_so_large_n_is_fast():
    start = time.perf_counter()
    result = solution.tile_2xn(10**6, mod=10007)
    assert time.perf_counter() - start < 5  # 중간에 나머지를 구하지 않으면 수가 수십만 자리가 되어 매우 느리다
    assert 0 <= result < 10007


def bfs_steps(n):
    dist = {n: 0}
    queue = deque([n])
    while queue:
        x = queue.popleft()
        if x == 1:
            return dist[x]
        nexts = [x - 1] + ([x // 2] if x % 2 == 0 else []) + ([x // 3] if x % 3 == 0 else [])
        for y in nexts:
            if y >= 1 and y not in dist:
                dist[y] = dist[x] + 1
                queue.append(y)


def test_min_steps_to_one_matches_bfs_and_path_is_valid():
    for n in range(1, 400):
        steps, path = solution.min_steps_to_one(n)
        assert steps == bfs_steps(n), n
        assert path[0] == n and path[-1] == 1 and len(path) == steps + 1
        for a, b in zip(path, path[1:]):
            assert b == a - 1 or (a % 2 == 0 and b == a // 2) or (a % 3 == 0 and b == a // 3)
    assert solution.min_steps_to_one(10) == (3, [10, 9, 3, 1])
    assert solution.min_steps_to_one(1) == (0, [1])


def test_greedy_is_not_enough_for_min_steps():
    # 나눠지면 무조건 ÷3 → ÷2 → −1 순으로 하는 그리디는 10 에서 4 번 (10→5→4→2→1) 이지만 최적은 3 번
    def greedy(n):
        steps = 0
        while n > 1:
            n = n // 3 if n % 3 == 0 else n // 2 if n % 2 == 0 else n - 1
            steps += 1
        return steps

    assert greedy(10) == 4 and solution.min_steps_to_one(10)[0] == 3


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("10\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
