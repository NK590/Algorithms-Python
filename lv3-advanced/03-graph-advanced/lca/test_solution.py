"""solution.py 검증: 부모를 하나씩 따라 올라가는 순진한 방법과 무작위 트리에서 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, n, shape="random"):
    """정점 0 이 루트가 아닐 수도 있게 정점 번호를 섞어서 (간선 목록, 정답 계산용 부모 배열(루트 0 기준 아님)) 를 만든다."""
    labels = list(range(n))
    rng.shuffle(labels)
    edges = []
    for i in range(1, n):
        if shape == "chain":
            parent = i - 1
        elif shape == "star":
            parent = 0
        else:
            parent = rng.randrange(i)
        edges.append((labels[i], labels[parent]))
    return edges


def naive_parents(n, edges, root):
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    parent = [-1] * n
    depth = [0] * n
    stack = [root]
    seen = {root}
    while stack:
        v = stack.pop()
        for w in adjacency[v]:
            if w not in seen:
                seen.add(w)
                parent[w] = v
                depth[w] = depth[v] + 1
                stack.append(w)
    return parent, depth


def naive_lca(parent, depth, u, v):
    while depth[u] > depth[v]:
        u = parent[u]
    while depth[v] > depth[u]:
        v = parent[v]
    while u != v:
        u, v = parent[u], parent[v]
    return u


def test_both_implementations_match_naive_on_every_pair():
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(1, 25)
        shape = rng.choice(["random", "chain", "star"])
        edges = random_tree(rng, n, shape)
        root = rng.randrange(n)
        parent, depth = naive_parents(n, edges, root)
        lifting = solution.BinaryLiftingLCA(n, edges, root)
        euler = solution.EulerTourLCA(n, edges, root)
        assert lifting.depth == depth and euler.depth == depth
        for u in range(n):
            for v in range(n):
                expected = naive_lca(parent, depth, u, v)
                assert lifting.lca(u, v) == expected, (edges, root, u, v)
                assert euler.lca(u, v) == expected, (edges, root, u, v)
                assert lifting.distance(u, v) == euler.distance(u, v) == depth[u] + depth[v] - 2 * depth[expected]


def test_kth_ancestor_and_is_ancestor():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(1, 25)
        edges = random_tree(rng, n)
        root = rng.randrange(n)
        parent, depth = naive_parents(n, edges, root)
        lifting = solution.BinaryLiftingLCA(n, edges, root)
        for v in range(n):
            expected = v
            for k in range(0, n + 3):
                assert lifting.kth_ancestor(v, k) == expected, (edges, root, v, k)
                if expected != root:
                    expected = parent[expected]
            for u in range(n):
                path = set()
                x = v
                while x != -1:
                    path.add(x)
                    x = parent[x]
                assert lifting.is_ancestor(u, v) == (u in path)
    with pytest.raises(ValueError):
        solution.BinaryLiftingLCA(2, [(0, 1)]).kth_ancestor(1, -1)


def test_small_examples():
    #        0
    #      / | \
    #     1  2  3
    #    / \     \
    #   4   5     6
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (3, 6)]
    for impl in (solution.BinaryLiftingLCA, solution.EulerTourLCA):
        tree = impl(7, edges)
        assert tree.lca(4, 5) == 1 and tree.lca(4, 6) == 0 and tree.lca(4, 1) == 1 and tree.lca(2, 2) == 2
        assert tree.distance(4, 6) == 4 and tree.distance(4, 5) == 2 and tree.distance(0, 0) == 0
    assert solution.BinaryLiftingLCA(1, []).lca(0, 0) == 0
    assert solution.EulerTourLCA(1, []).lca(0, 0) == 0


def test_euler_tour_has_two_n_minus_one_entries():
    rng = random.Random(2)
    for _ in range(50):
        n = rng.randint(1, 30)
        tree = solution.EulerTourLCA(n, random_tree(rng, n))
        assert len(tree.tour) == 2 * n - 1
        assert all(abs(tree.depth[a] - tree.depth[b]) == 1 for a, b in zip(tree.tour, tree.tour[1:]))


def test_deep_chain_does_not_recurse():
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]
    lifting = solution.BinaryLiftingLCA(n, edges)
    euler = solution.EulerTourLCA(n, edges)
    assert lifting.lca(n - 1, n // 2) == n // 2 and euler.lca(n - 1, n // 2) == n // 2
    assert lifting.distance(0, n - 1) == n - 1 and euler.distance(0, n - 1) == n - 1
    assert lifting.kth_ancestor(n - 1, 12345) == n - 1 - 12345


def test_large_random_tree_is_fast_and_consistent():
    rng = random.Random(3)
    n = 100_000
    edges = [(i, rng.randrange(i)) for i in range(1, n)]
    lifting = solution.BinaryLiftingLCA(n, edges)
    euler = solution.EulerTourLCA(n, edges)
    for _ in range(20_000):
        u, v = rng.randrange(n), rng.randrange(n)
        assert lifting.lca(u, v) == euler.lca(u, v)


def test_main(monkeypatch, capsys):
    text = "15\n1 2\n1 3\n2 4\n3 7\n6 2\n3 8\n4 9\n2 5\n5 11\n7 13\n10 4\n11 15\n12 5\n14 7\n6\n6 11\n10 9\n2 6\n7 6\n8 13\n8 15\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.split() == ["2", "4", "2", "1", "3", "1"]
