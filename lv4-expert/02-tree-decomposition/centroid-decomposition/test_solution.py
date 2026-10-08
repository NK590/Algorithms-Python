"""solution.py 검증: 모든 정점에서 BFS 로 구한 거리, 칠한 정점을 모두 훑는 순진한 방법과 무작위 트리로 비교"""
import io
import random
import time
from collections import deque

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_tree(rng, n, shape=None):
    shape = shape or rng.choice(["random", "chain", "star", "binary"])
    edges = []
    for v in range(1, n):
        p = {"random": rng.randrange(v), "chain": v - 1, "star": 0, "binary": (v - 1) // 2}[shape]
        edges.append((p, v) if rng.random() < 0.5 else (v, p))
    return edges


def all_distances(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    table = []
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
        table.append(dist)
    return table


def test_centroid_tree_structure():
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(1, 60)
        edges = random_tree(rng, n)
        cd = solution.CentroidDecomposition(n, edges)
        assert cd.parent.count(-1) == 1 and cd.parent[cd.root] == -1 and cd.level[cd.root] == 0
        assert max(cd.level) <= n.bit_length() - 1  # 조각의 크기가 레벨마다 절반 이하로 줄어 깊이 ≤ ⌊log₂ n⌋
        for v in range(n):
            chain = cd.ancestors(v)
            assert chain[0] == cd.root and chain[-1] == v and len(chain) == cd.level[v] + 1
            assert len(cd.dist[v]) == cd.level[v] + 1 and cd.dist[v][-1] == 0
            if cd.parent[v] != -1:
                assert cd.level[v] == cd.level[cd.parent[v]] + 1


def test_distances_to_centroid_ancestors_and_distance_formula():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(1, 50)
        edges = random_tree(rng, n)
        table = all_distances(n, edges)
        cd = solution.CentroidDecomposition(n, edges)
        for v in range(n):
            for i, a in enumerate(cd.ancestors(v)):
                assert cd.dist[v][i] == table[v][a], (edges, v, a)
        for u in range(n):
            for v in range(n):
                assert cd.distance(u, v) == table[u][v], (edges, u, v)


def test_each_centroid_splits_its_piece_into_halves():
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(2, 60)
        cd = solution.CentroidDecomposition(n, random_tree(rng, n))
        # 센트로이드 c 의 자식 조각 크기(= group 의 길이) 는 조각 전체의 절반 이하
        for c in range(n):
            groups = cd.group_distances[c]
            total = 1 + sum(len(g) for g in groups)
            assert all(len(g) * 2 <= total for g in groups), (c, total, [len(g) for g in groups])


def test_nearest_marked_matches_scanning_all_marked_vertices():
    rng = random.Random(3)
    for _ in range(80):
        n = rng.randint(1, 40)
        edges = random_tree(rng, n)
        table = all_distances(n, edges)
        structure = solution.NearestMarked(solution.CentroidDecomposition(n, edges))
        marked = []
        assert structure.nearest(0) == solution.INF
        for _ in range(60):
            if rng.random() < 0.4:
                v = rng.randrange(n)
                structure.mark(v)
                marked.append(v)
            else:
                v = rng.randrange(n)
                expected = min((table[v][m] for m in marked), default=solution.INF)
                assert structure.nearest(v) == expected, (edges, marked, v)


def test_path_counts_with_bounded_and_exact_length():
    rng = random.Random(4)
    for _ in range(80):
        n = rng.randint(1, 40)
        edges = random_tree(rng, n)
        table = all_distances(n, edges)
        cd = solution.CentroidDecomposition(n, edges)
        for k in range(0, n + 2):
            at_most = sum(1 for u in range(n) for v in range(u + 1, n) if table[u][v] <= k)
            exact = sum(1 for u in range(n) for v in range(u + 1, n) if table[u][v] == k)
            assert cd.count_paths_at_most(k) == at_most, (edges, k)
            assert cd.count_paths_with_length(k) == exact, (edges, k)


def test_invalid_input():
    with pytest.raises(ValueError, match="트리가 아닙니다"):
        solution.CentroidDecomposition(4, [(0, 1), (1, 2)])


def test_chain_of_100000_vertices_has_logarithmic_depth_and_runs_fast():
    n = 100000
    started = time.perf_counter()
    cd = solution.CentroidDecomposition(n, [(i, i + 1) for i in range(n - 1)])
    assert max(cd.level) <= 17
    structure = solution.NearestMarked(cd)
    structure.mark(0)
    structure.mark(n - 1)
    assert structure.nearest(10) == 10 and structure.nearest(n - 5) == 4
    assert structure.nearest(n // 2) == min(n // 2, n - 1 - n // 2)
    assert time.perf_counter() - started < 30


def test_star_graph_and_single_vertex():
    cd = solution.CentroidDecomposition(1, [])
    assert cd.root == 0 and cd.level == [0] and cd.count_paths_at_most(5) == 0
    star = solution.CentroidDecomposition(6, [(0, i) for i in range(1, 6)])
    assert star.root == 0 and max(star.level) == 1
    assert star.count_paths_with_length(1) == 5 and star.count_paths_with_length(2) == 10


def test_main(monkeypatch, capsys):
    # 1-2-3-4-5 사슬. 정점 1 은 처음부터 빨강
    text = "5 6\n1 2\n2 3\n3 4\n4 5\n2 5\n1 5\n2 4\n2 5\n1 3\n2 4\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "4\n1\n0\n1\n"  # 5 까지 4, (5 를 칠함) 4 까지 1, 5 는 0, (3 을 칠함) 4 까지 1
