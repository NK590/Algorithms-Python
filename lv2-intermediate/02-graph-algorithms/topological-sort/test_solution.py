"""solution.py 검증: 모든 순열을 시도하는 브루트포스와 비교 (순서의 유효성, 사이클 판정, 사전순 최소, 최장 경로)"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def is_valid_order(n, edges, order):
    position = {v: i for i, v in enumerate(order)}
    return sorted(order) == list(range(n)) and all(position[u] < position[v] for u, v in edges)


def all_valid_orders(n, edges):
    return [p for p in itertools.permutations(range(n)) if is_valid_order(n, edges, p)]


def random_graph(rng, acyclic=None):
    n = rng.randint(0, 6)
    edges = []
    if n:
        for _ in range(rng.randint(0, 9)):
            u, v = rng.randrange(n), rng.randrange(n)
            if acyclic and u >= v:
                continue
            edges.append((u, v))
    return n, edges


def test_both_algorithms_agree_with_brute_force():
    rng = random.Random(0)
    cyclic = acyclic = 0
    for _ in range(1000):
        n, edges = random_graph(rng)
        valid = all_valid_orders(n, edges)
        for func in (solution.topological_sort, solution.topological_sort_dfs):
            order = func(n, edges)
            if valid:
                assert order is not None and is_valid_order(n, edges, order), (func.__name__, n, edges, order)
            else:
                assert order is None, (func.__name__, n, edges)
        assert solution.has_cycle(n, edges) == (not valid)
        cyclic += not valid
        acyclic += bool(valid)
    assert cyclic > 100 and acyclic > 100  # 두 경우를 모두 충분히 시험했는지


def test_cycle_special_cases():
    assert solution.topological_sort(1, [(0, 0)]) is None  # 자기 자신으로 가는 간선
    assert solution.topological_sort_dfs(1, [(0, 0)]) is None
    assert solution.topological_sort(2, [(0, 1), (1, 0)]) is None
    assert solution.topological_sort(0, []) == [] and solution.topological_sort_dfs(0, []) == []
    # 사이클 뒤에 매달린 정점은 꺼내지지 않는다
    assert solution.topological_sort(4, [(0, 1), (1, 0), (1, 2), (3, 2)]) is None
    assert solution.topological_sort(3, [(0, 1), (0, 1), (1, 2)]) == [0, 1, 2]  # 중복 간선


def test_a_long_chain_does_not_recurse():
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]
    assert solution.topological_sort_dfs(n, edges) == list(range(n))
    assert solution.topological_sort(n, edges) == list(range(n))


def test_readme_example():
    # 옷 입기: 0 속옷, 1 바지, 2 신발, 3 양말, 4 셔츠, 5 넥타이, 6 재킷
    edges = [(0, 1), (1, 2), (3, 2), (4, 5), (5, 6), (1, 6)]
    for func in (solution.topological_sort, solution.topological_sort_dfs, solution.smallest_topological_order):
        order = func(7, edges)
        assert is_valid_order(7, edges, order)
    assert solution.topological_sort(7, edges) == [0, 3, 4, 1, 5, 2, 6]
    assert solution.smallest_topological_order(7, edges) == [0, 1, 3, 2, 4, 5, 6]  # 신발(2)은 양말(3) 뒤


def test_smallest_order_matches_lexicographic_minimum():
    rng = random.Random(1)
    for _ in range(500):
        n, edges = random_graph(rng)
        valid = all_valid_orders(n, edges)
        result = solution.smallest_topological_order(n, edges)
        assert result == (list(min(valid)) if valid else None), (n, edges)


def longest_finish_by_recursion(durations, edges):
    n = len(durations)
    preds = [[] for _ in range(n)]
    for u, v in edges:
        preds[v].append(u)
    memo = {}

    def finish(v):
        if v not in memo:
            memo[v] = durations[v] + max((finish(u) for u in preds[v]), default=0)
        return memo[v]

    return [finish(v) for v in range(n)]


def test_earliest_finish_times_matches_recursive_longest_path():
    rng = random.Random(2)
    for _ in range(500):
        n, edges = random_graph(rng, acyclic=True)
        durations = [rng.randint(1, 9) for _ in range(n)]
        assert solution.earliest_finish_times(durations, edges) == longest_finish_by_recursion(durations, edges), (n, edges)
    assert solution.earliest_finish_times([1, 1], [(0, 1), (1, 0)]) is None
    assert solution.earliest_finish_times([5], []) == [5]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 2\n1 3\n2 3\n"))
    solution.main()
    order = list(map(int, capsys.readouterr().out.split()))
    assert is_valid_order(3, [(0, 2), (1, 2)], [v - 1 for v in order])
    monkeypatch.setattr("sys.stdin", io.StringIO("2 2\n1 2\n2 1\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "-1"
