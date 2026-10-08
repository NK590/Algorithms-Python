"""solution.py 검증: 플로이드-워셜(모든 쌍 최단 거리)과의 랜덤 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = float("inf")


def random_adj(rng, directed):
    n = rng.randint(1, 9)
    adj = [[] for _ in range(n)]
    for _ in range(rng.randint(0, 14)):
        u, v = rng.randrange(n), rng.randrange(n)
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj


def floyd_warshall(adj):
    n = len(adj)
    dist = [[INF] * n for _ in range(n)]
    for u in range(n):
        dist[u][u] = 0
        for v in adj[u]:
            dist[u][v] = min(dist[u][v], 1)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


def test_readme_example():
    adj = [[1, 2], [0, 3, 4], [0, 4], [1], [1, 2]]
    assert solution.bfs_order(adj, 0) == [0, 1, 2, 3, 4]
    assert solution.bfs_distances(adj, 0) == [0, 1, 1, 2, 2]
    assert solution.bfs_levels(adj, 0) == [[0], [1, 2], [3, 4]]
    assert solution.bfs_shortest_path(adj, 3, 2) in ([3, 1, 0, 2], [3, 1, 4, 2])


def test_distances_match_floyd_warshall():
    rng = random.Random(0)
    for directed in (False, True):
        for _ in range(300):
            adj = random_adj(rng, directed)
            expected = floyd_warshall(adj)
            for start in range(len(adj)):
                got = solution.bfs_distances(adj, start)
                assert got == [-1 if d == INF else d for d in expected[start]], (adj, start)


def test_order_is_sorted_by_distance_and_has_no_repeats():
    rng = random.Random(1)
    for directed in (False, True):
        for _ in range(300):
            adj = random_adj(rng, directed)
            for start in range(len(adj)):
                order = solution.bfs_order(adj, start)
                dist = solution.bfs_distances(adj, start)
                assert len(order) == len(set(order)) == sum(d != -1 for d in dist)
                assert [dist[v] for v in order] == sorted(dist[v] for v in order)


def test_shortest_path_is_valid_and_shortest():
    rng = random.Random(2)
    for directed in (False, True):
        for _ in range(300):
            adj = random_adj(rng, directed)
            for s in range(len(adj)):
                dist = solution.bfs_distances(adj, s)
                for t in range(len(adj)):
                    path = solution.bfs_shortest_path(adj, s, t)
                    if dist[t] == -1:
                        assert path is None
                    else:
                        assert path[0] == s and path[-1] == t and len(path) - 1 == dist[t]
                        assert all(b in adj[a] for a, b in zip(path, path[1:]))


def test_levels_match_distances():
    adj = [[1], [2], [3], [], [0]]
    assert solution.bfs_levels(adj, 0) == [[0], [1], [2], [3]]


def test_large_path_graph():
    n = 100_000
    adj = [[i + 1] if i + 1 < n else [] for i in range(n)]
    assert solution.bfs_distances(adj, 0)[-1] == n - 1


def test_main_prints_distances(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 4 1\n1 2\n2 3\n3 4\n1 3\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["0", "1", "1", "2", "-1"]
