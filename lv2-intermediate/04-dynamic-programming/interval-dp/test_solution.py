"""solution.py 검증: 모든 괄호 묶음 / 모든 합치기 순서 / 모든 부분 수열 / 모든 터뜨리기 순서를 직접 열거해 비교"""
import io
import itertools
import random
from functools import lru_cache

from tools.loader import load_solution

solution = load_solution(__file__)


def chain_cost_by_enumeration(dims, i=1, j=None):
    """i..j 를 곱하는 모든 괄호 묶음을 재귀로 열거해 최소 비용 (메모 없음)"""
    if j is None:
        j = len(dims) - 1
    if i == j:
        return 0
    return min(
        chain_cost_by_enumeration(dims, i, k) + chain_cost_by_enumeration(dims, k + 1, j) + dims[i - 1] * dims[k] * dims[j]
        for k in range(i, j)
    )


def evaluate_parenthesization(expr, dims):
    """"((A1A2)A3)" 같은 식을 직접 계산해 (행, 열, 비용) 을 돌려준다"""
    pos = 0

    def parse():
        nonlocal pos
        if expr[pos] == "(":
            pos += 1
            left = parse()
            right = parse()
            assert expr[pos] == ")"
            pos += 1
            assert left[1] == right[0], "곱할 수 없는 모양"
            return (left[0], right[1], left[2] + right[2] + left[0] * left[1] * right[1])
        assert expr[pos] == "A"
        pos += 1
        start = pos
        while pos < len(expr) and expr[pos].isdigit():
            pos += 1
        index = int(expr[start:pos])
        return (dims[index - 1], dims[index], 0)

    return parse()


def test_matrix_chain_matches_enumeration_and_expression_is_valid():
    rng = random.Random(0)
    for _ in range(300):
        dims = [rng.randint(1, 9) for _ in range(rng.randint(2, 8))]
        cost, expr = solution.matrix_chain_order(dims)
        assert cost == chain_cost_by_enumeration(dims), dims
        rows, cols, spent = evaluate_parenthesization(expr, dims)
        assert (rows, cols) == (dims[0], dims[-1]) and spent == cost, (dims, expr)
    assert solution.matrix_chain_order([10, 30, 5, 60]) == (4500, "((A1A2)A3)")
    assert solution.matrix_chain_order([5]) == (0, "") and solution.matrix_chain_order([3, 4]) == (0, "A1")


def merge_cost_by_enumeration(sizes):
    @lru_cache(maxsize=None)
    def best(state):
        if len(state) == 1:
            return 0
        return min(
            state[i] + state[i + 1] + best(state[:i] + (state[i] + state[i + 1],) + state[i + 2 :])
            for i in range(len(state) - 1)
        )

    return best(tuple(sizes)) if sizes else 0


def test_merge_cost_matches_all_adjacent_merge_orders():
    rng = random.Random(1)
    for _ in range(300):
        sizes = [rng.randint(1, 20) for _ in range(rng.randint(0, 8))]
        assert solution.min_merge_cost(sizes) == merge_cost_by_enumeration(sizes), sizes
    assert solution.min_merge_cost([40, 30, 30, 50]) == 300
    assert solution.min_merge_cost([1, 21, 3, 4, 5, 35, 5, 4, 3, 5, 98, 21, 14, 17, 32]) == 864
    assert solution.min_merge_cost([7]) == 0


def test_adjacent_merging_differs_from_free_merging():
    # 인접 제한이 없으면 힙으로 가장 작은 둘을 합친다 (그리디). 인접해야 하면 구간 DP.
    sizes = [1, 100, 1, 100]
    import heapq

    heap = sizes[:]
    heapq.heapify(heap)
    free = 0
    while len(heap) > 1:
        merged = heapq.heappop(heap) + heapq.heappop(heap)
        free += merged
        heapq.heappush(heap, merged)
    assert solution.min_merge_cost(sizes) > free


def test_longest_palindromic_subsequence_matches_enumeration():
    rng = random.Random(2)
    for _ in range(400):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 11)))
        best = 0
        for mask in range(1 << len(s)):
            picked = "".join(s[i] for i in range(len(s)) if mask >> i & 1)
            if picked == picked[::-1]:
                best = max(best, len(picked))
        assert solution.longest_palindromic_subsequence(s) == best, s
    assert solution.longest_palindromic_subsequence("bbbab") == 4
    assert solution.longest_palindromic_subsequence("") == 0 and solution.longest_palindromic_subsequence("x") == 1


def test_palindrome_table_matches_direct_check():
    rng = random.Random(3)
    for _ in range(300):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 12)))
        table = solution.palindrome_table(s)
        for l in range(len(s)):
            for r in range(l, len(s)):
                assert table[l][r] == (s[l : r + 1] == s[l : r + 1][::-1]), (s, l, r)


def test_burst_balloons_matches_all_burst_orders():
    rng = random.Random(4)
    for _ in range(200):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(0, 6))]
        best = 0
        for order in itertools.permutations(range(len(nums))):
            alive = [1] + nums[:] + [1]
            idx = list(range(len(alive)))
            total = 0
            for target in order:
                p = idx.index(target + 1)
                total += alive[idx[p - 1]] * alive[idx[p]] * alive[idx[p + 1]]
                idx.pop(p)
            best = max(best, total)
        assert solution.burst_balloons(nums) == (best if nums else 0), nums
    assert solution.burst_balloons([3, 1, 5, 8]) == 167
    assert solution.burst_balloons([]) == 0 and solution.burst_balloons([7]) == 7


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("2\n4\n40 30 30 50\n15\n1 21 3 4 5 35 5 4 3 5 98 21 14 17 32\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["300", "864"]
