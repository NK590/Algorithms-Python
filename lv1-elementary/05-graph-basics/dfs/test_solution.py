"""solution.py 검증: 재귀·반복 버전 비교 + 도달 가능성은 느린 반복 계산과 비교 + 괄호 구조(시각)"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_adj(rng, directed):
    n = rng.randint(1, 9)
    adj = [[] for _ in range(n)]
    for _ in range(rng.randint(0, 14)):
        u, v = rng.randrange(n), rng.randrange(n)
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def closure_reachable(adj, start):
    """도달 가능한 집합이 더 늘지 않을 때까지 간선을 따라 넓히는 느린 방법"""
    seen = {start}
    changed = True
    while changed:
        changed = False
        for u in list(seen):
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    changed = True
    return seen


def test_readme_example_order():
    adj = [[1, 2], [0, 3, 4], [0, 4], [1], [1, 2]]
    assert solution.dfs_recursive(adj, 0) == [0, 1, 3, 4, 2]
    assert solution.dfs_iterative(adj, 0) == [0, 1, 3, 4, 2]


def test_recursive_and_iterative_give_the_same_order():
    rng = random.Random(0)
    for directed in (False, True):
        for _ in range(300):
            adj = random_adj(rng, directed)
            for start in range(len(adj)):
                assert solution.dfs_recursive(adj, start) == solution.dfs_iterative(adj, start)


def test_reachable_matches_closure():
    rng = random.Random(1)
    for directed in (False, True):
        for _ in range(300):
            adj = random_adj(rng, directed)
            for start in range(len(adj)):
                assert solution.reachable(adj, start) == closure_reachable(adj, start)
                assert len(solution.dfs_iterative(adj, start)) == len(set(solution.dfs_iterative(adj, start)))


def test_has_path():
    adj = [[1], [2], [], [0]]
    assert solution.has_path(adj, 0, 2)
    assert not solution.has_path(adj, 2, 0)
    assert solution.has_path(adj, 3, 2)
    assert solution.has_path(adj, 1, 1)


def test_times_form_a_parenthesis_structure():
    rng = random.Random(2)
    for directed in (False, True):
        for _ in range(300):
            adj = random_adj(rng, directed)
            disc, fin = solution.dfs_times(adj)
            n = len(adj)
            assert sorted(disc + fin) == list(range(2 * n))  # 시각은 겹치지 않고 0 ~ 2n-1 을 정확히 한 번씩 쓴다
            for u in range(n):
                assert disc[u] < fin[u]
                for v in range(n):
                    if u == v:
                        continue
                    nested = disc[u] < disc[v] < fin[v] < fin[u] or disc[v] < disc[u] < fin[u] < fin[v]
                    disjoint = fin[u] < disc[v] or fin[v] < disc[u]
                    assert nested or disjoint, (adj, u, v)


def test_times_order_matches_dfs_preorder_per_start():
    adj = [[1, 2], [3], [3], []]
    disc, _ = solution.dfs_times(adj)
    assert sorted(range(4), key=lambda v: disc[v]) == solution.dfs_iterative(adj, 0)


def test_deep_graph_needs_the_iterative_version():
    n = 50_000
    adj = [[i + 1] if i + 1 < n else [] for i in range(n)]
    assert solution.dfs_iterative(adj, 0)[-1] == n - 1
    with pytest.raises(RecursionError):
        solution.dfs_recursive(adj, 0)
    disc, fin = solution.dfs_times(adj)
    assert disc[n - 1] == n - 1


def test_main_visits_smaller_neighbors_first(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4 5 1\n1 2\n1 3\n1 4\n2 4\n3 4\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "2", "4", "3"]
