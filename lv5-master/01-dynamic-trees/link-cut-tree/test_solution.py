"""solution.py 검증: 인접 리스트로 직접 DFS 하는 순진한 숲과 무작위 link/cut/질의 열로 비교"""
import io
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


class NaiveForest:
    def __init__(self, values):
        self.values = list(values)
        self.adj = [set() for _ in values]

    def path(self, u, v):
        """u 에서 v 로 가는 정점 목록 (연결되어 있지 않으면 None)."""
        parent = {u: None}
        stack = [u]
        while stack:
            x = stack.pop()
            for y in self.adj[x]:
                if y not in parent:
                    parent[y] = x
                    stack.append(y)
        if v not in parent:
            return None
        result = []
        while v is not None:
            result.append(v)
            v = parent[v]
        return result[::-1]

    def component(self, u):
        seen = {u}
        stack = [u]
        while stack:
            x = stack.pop()
            for y in self.adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    def lca(self, root, u, v):
        pu, pv = self.path(root, u), self.path(root, v)
        result = root
        for a, b in zip(pu, pv):
            if a != b:
                break
            result = a
        return result


def test_random_operations_match_the_naive_forest():
    rng = random.Random(0)
    for trial in range(150):
        n = rng.randint(1, 12)
        values = [rng.randint(-9, 9) for _ in range(n)]
        tree = solution.LinkCutTree(values)
        naive = NaiveForest(values)
        edges = set()
        for _ in range(120):
            op = rng.choice(["link", "link", "cut", "connected", "sum", "max", "add", "path_add", "set", "get", "lca", "root", "length", "make_root"])
            u, v = rng.randrange(n), rng.randrange(n)
            if op == "link":
                if u != v and naive.path(u, v) is None:
                    tree.link(u, v)
                    naive.adj[u].add(v)
                    naive.adj[v].add(u)
                    edges.add((min(u, v), max(u, v)))
                else:
                    with pytest.raises(ValueError):
                        tree.link(u, v)
            elif op == "cut":
                if edges and rng.random() < 0.8:
                    a, b = rng.choice(sorted(edges))
                    tree.cut(a, b) if rng.random() < 0.5 else tree.cut(b, a)
                    naive.adj[a].discard(b)
                    naive.adj[b].discard(a)
                    edges.discard((a, b))
                elif (min(u, v), max(u, v)) not in edges:
                    with pytest.raises(ValueError):
                        tree.cut(u, v)
            elif op == "connected":
                assert tree.connected(u, v) == (naive.path(u, v) is not None)
            elif op in ("sum", "max", "length", "path_add", "lca"):
                path = naive.path(u, v)
                if path is None:
                    with pytest.raises(ValueError):
                        tree.path_sum(u, v)
                    continue
                if op == "sum":
                    assert tree.path_sum(u, v) == sum(naive.values[x] for x in path)
                elif op == "max":
                    assert tree.path_max(u, v) == max(naive.values[x] for x in path)
                elif op == "length":
                    assert tree.path_length(u, v) == len(path)
                elif op == "path_add":
                    d = rng.randint(-5, 5)
                    tree.path_add(u, v, d)
                    for x in path:
                        naive.values[x] += d
                else:
                    w = rng.randrange(n)
                    if naive.path(u, w) is not None:
                        assert tree.lca(u, v, w) == naive.lca(u, v, w), (u, v, w)
            elif op == "add":
                d = rng.randint(-5, 5)
                tree.add_value(u, d)
                naive.values[u] += d
            elif op == "set":
                x = rng.randint(-9, 9)
                tree.set_value(u, x)
                naive.values[u] = x
            elif op == "get":
                assert tree.get_value(u) == naive.values[u]
            elif op == "root":
                comp = naive.component(u)
                assert tree.find_root(u) in comp
                assert len({tree.find_root(x) for x in comp}) == 1
                tree.make_root(u)
                assert all(tree.find_root(x) == u for x in comp)  # make_root 뒤에는 모든 정점의 루트가 정확히 u
            else:
                tree.make_root(u)
                assert tree.find_root(u) == u
        for u in range(n):  # 마지막에 모든 값이 일치
            assert tree.get_value(u) == naive.values[u]


def test_long_chains_do_not_recurse_and_stay_fast():
    n = 100000
    tree = solution.LinkCutTree([1] * n)
    started = time.perf_counter()
    for i in range(n - 1):
        tree.link(i, i + 1)
    assert tree.path_sum(0, n - 1) == n and tree.path_length(0, n - 1) == n
    tree.cut(n // 2, n // 2 + 1)
    assert not tree.connected(0, n - 1) and tree.path_sum(0, n // 2) == n // 2 + 1
    tree.link(n // 2, n - 1)  # 한가운데를 끝에 붙여 다시 연결
    assert tree.connected(0, n - 1)
    assert time.perf_counter() - started < 60


def test_many_random_operations_on_a_larger_forest_are_fast_and_consistent():
    rng = random.Random(1)
    n = 3000
    values = [rng.randint(-100, 100) for _ in range(n)]
    tree = solution.LinkCutTree(values)
    naive = NaiveForest(values)
    edges = []
    started = time.perf_counter()
    for _ in range(6000):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and not tree.connected(u, v):
            tree.link(u, v)
            naive.adj[u].add(v)
            naive.adj[v].add(u)
            edges.append((u, v))
        if edges and rng.random() < 0.3:
            a, b = edges.pop(rng.randrange(len(edges)))
            tree.cut(a, b)
            naive.adj[a].discard(b)
            naive.adj[b].discard(a)
    assert time.perf_counter() - started < 60
    for _ in range(30):
        u, v = rng.randrange(n), rng.randrange(n)
        path = naive.path(u, v)
        assert tree.connected(u, v) == (path is not None)
        if path is not None:
            assert tree.path_sum(u, v) == sum(values[x] for x in path)


def test_cut_distinguishes_an_edge_from_a_longer_path_and_invalid_arguments():
    tree = solution.LinkCutTree([1, 2, 3, 4])
    tree.link(0, 1)
    tree.link(1, 2)
    with pytest.raises(ValueError, match="간선이 없"):
        tree.cut(0, 2)  # 경로는 있지만 간선은 아니다
    with pytest.raises(ValueError, match="간선이 없"):
        tree.cut(0, 3)  # 다른 트리
    with pytest.raises(ValueError, match="간선이 없"):
        tree.cut(1, 1)
    with pytest.raises(ValueError, match="연결"):
        tree.link(0, 2)
    with pytest.raises(ValueError, match="연결"):
        tree.link(1, 1)
    with pytest.raises(IndexError, match="정점"):
        tree.link(0, 4)
    with pytest.raises(IndexError, match="정점"):
        tree.path_sum(-1, 0)
    with pytest.raises(IndexError, match="정점"):
        tree.get_value(4)
    with pytest.raises(ValueError, match="트리"):
        tree.path_sum(0, 3)
    with pytest.raises(ValueError, match="트리"):
        tree.lca(0, 1, 3)
    tree.cut(1, 0)
    tree.link(0, 3)
    assert tree.connected(0, 3) and not tree.connected(0, 1) and tree.path_sum(0, 3) == 1 + 4 and tree.path_sum(1, 2) == 2 + 3


def splay_height(tree, root):
    best, stack = 0, [(root, 1)]
    while stack:
        x, d = stack.pop()
        best = max(best, d)
        tree._push(x)
        for child in (tree.left[x], tree.right[x]):
            if child:
                stack.append((child, d + 1))
    return best


def test_splay_halves_the_depth_of_a_long_chain():
    # 사슬을 이으면 정점마다 자기 스플레이 트리를 갖고 경로 부모로만 이어진다. access 가 한 줄로 이어 붙이면 오른쪽으로만 기운 깊이 n 의 스플레이 트리가 되는데,
    # 마지막 splay 가 zig-zig 를 올바르게 쓰면 깊이가 약 절반으로 줄고, zig-zag 만 쓰면 줄지 않는다.
    n = 2000
    tree = solution.LinkCutTree([1] * n)
    for i in range(n - 1):
        tree.link(i, i + 1)
    tree.make_root(0)
    root = n  # 정점 n - 1 의 내부 번호 (내부 번호는 정점 번호 + 1)
    tree._access(root)
    assert tree.parent[root] == 0  # 루트 경로 전체가 하나의 스플레이 트리이고 root 가 그 루트
    assert splay_height(tree, root) <= n // 2 + 10


def test_root_changes_with_make_root_and_lca_depends_on_the_root():
    tree = solution.LinkCutTree([0] * 7)
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]:
        tree.link(a, b)
    assert tree.lca(0, 3, 4) == 1 and tree.lca(0, 3, 5) == 0 and tree.lca(0, 4, 4) == 4
    assert tree.lca(3, 4, 5) == 1 and tree.lca(3, 5, 6) == 2 and tree.lca(5, 3, 4) == 1
    assert tree.lca(3, 0, 2) == 0 and tree.lca(5, 0, 2) == 2  # 루트를 바꾸면 같은 두 정점의 LCA 가 달라진다 (3 이 루트면 0 이 2 의 조상, 5 가 루트면 2 가 0 의 조상)
    tree.make_root(6)
    assert tree.find_root(0) == 6


def test_values_and_path_updates():
    tree = solution.LinkCutTree([5, 1, 4, 2])
    for a, b in [(0, 1), (1, 2), (2, 3)]:
        tree.link(a, b)
    assert tree.path_sum(0, 3) == 12 and tree.path_max(0, 3) == 5 and tree.path_max(1, 2) == 4
    tree.path_add(1, 3, 10)
    assert tree.path_sum(0, 3) == 5 + 11 + 14 + 12 and tree.get_value(0) == 5 and tree.get_value(3) == 12
    tree.set_value(2, -7)
    assert tree.path_sum(0, 3) == 5 + 11 - 7 + 12 and tree.path_max(0, 3) == 12


def test_main_dynamic_tree_vertex_add_path_sum_format(monkeypatch, capsys):
    text = "5 6\n1 2 3 4 5\n0 1\n1 2\n2 3\n3 4\n2 0 4\n1 2 10\n2 0 4\n0 1 2 0 4\n2 0 3\n2 3 4\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    # 경로 0-1-2-3-4: 합 15; 정점 2 에 +10 → 25; 간선 (1,2) 를 끊고 (0,4) 를 잇는다 → 3-2 쪽과 0-1, 0-4 가 이어진 구조:
    # 경로 0 … 3: 0-4-3 → 1 + 5 + 4 = 10, 경로 3-4: 4 + 5 = 9
    assert capsys.readouterr().out == "15\n25\n10\n9\n"
