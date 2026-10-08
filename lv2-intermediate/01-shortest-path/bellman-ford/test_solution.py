"""solution.py 검증: README 예제 + 플로이드-워셜(전혀 다른 방식)과 랜덤 비교, 사이클 탐지는 직접 검증"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = solution.INF


def floyd_warshall(n, edges):
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[k][j] != INF and dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def reachable_negative_cycle(n, edges, start):
    """start 에서 닿을 수 있는 정점 중 dist[v][v] < 0 인 정점이 있는가 (플로이드-워셜 기준)"""
    fw = floyd_warshall(n, edges)
    return any(fw[start][v] != INF and fw[v][v] < 0 for v in range(n))


def any_negative_cycle(n, edges):
    fw = floyd_warshall(n, edges)
    return any(fw[v][v] < 0 for v in range(n))


def build(n, edges):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph


# README 의 예제: A=0, B=1, C=2, D=3, E=4
README_EDGES = [(0, 1, -1), (0, 2, 4), (1, 2, 3), (1, 3, 2), (1, 4, 2), (3, 1, 1), (3, 2, 5), (4, 3, -3)]
README_CYCLE_EDGES = README_EDGES + [(2, 0, -5)]


def test_readme_example_without_negative_cycle():
    dist, cycle = solution.bellman_ford(5, README_EDGES, 0)
    assert (dist, cycle) == ([0, -1, 2, -2, 1], False)


def test_readme_example_with_negative_cycle():
    _, cycle = solution.bellman_ford(5, README_CYCLE_EDGES, 0)
    assert cycle is True


def random_graph(rng, low=-4):
    n = rng.randint(1, 6)
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(rng.randint(0, 14))]
    return n, edges


def test_matches_floyd_warshall_when_no_negative_cycle_is_reachable():
    rng = random.Random(0)
    checked = 0
    for _ in range(1500):
        n, edges = random_graph(rng)
        start = rng.randrange(n)
        dist, cycle = solution.bellman_ford(n, edges, start)
        assert cycle == reachable_negative_cycle(n, edges, start), (n, edges, start)
        if not cycle:
            assert dist == floyd_warshall(n, edges)[start], (n, edges, start)
            checked += 1
    assert checked > 300  # 음수 사이클이 없는 경우를 충분히 시험했는지


def test_unreachable_vertices_stay_inf_even_with_negative_edges():
    # 2 → 1 (-5) 는 0 에서 닿지 않는 정점 2 에서 출발하므로 1 의 거리에 영향을 주지 못한다
    dist, cycle = solution.bellman_ford(3, [(0, 1, 4), (2, 1, -5)], 0)
    assert (dist, cycle) == ([0, 4, INF], False)


def test_negative_cycle_unreachable_from_start_is_not_reported():
    dist, cycle = solution.bellman_ford(4, [(0, 1, 1), (2, 3, -1), (3, 2, -1)], 0)
    assert cycle is False and dist == [0, 1, INF, INF]


def test_negative_self_loop_and_zero_cycle():
    assert solution.bellman_ford(1, [(0, 0, -1)], 0)[1] is True
    assert solution.bellman_ford(2, [(0, 1, 2), (1, 0, -2)], 0)[1] is False  # 합이 0 인 사이클은 괜찮다
    assert solution.bellman_ford(1, [], 0) == ([0], False)


def test_with_prev_gives_valid_shortest_paths():
    rng = random.Random(1)
    for _ in range(500):
        n, edges = random_graph(rng)
        start = rng.randrange(n)
        dist, prev, cycle = solution.bellman_ford_with_prev(n, edges, start)
        if cycle:
            continue
        for target in range(n):
            path = solution.restore_path(prev, start, target)
            if dist[target] == INF:
                assert path == []
                continue
            assert path[0] == start and path[-1] == target
            total = 0
            for a, b in zip(path, path[1:]):
                total += min(w for u, v, w in edges if (u, v) == (a, b))
            assert total == dist[target], (n, edges, start, target, path)


def test_find_negative_cycle_returns_a_real_negative_cycle():
    rng = random.Random(2)
    found = 0
    for _ in range(1000):
        n, edges = random_graph(rng)
        cycle = solution.find_negative_cycle(n, edges)
        assert (cycle is not None) == any_negative_cycle(n, edges), (n, edges)
        if cycle is not None:
            found += 1
            total = 0
            for a, b in zip(cycle, cycle[1:] + cycle[:1]):  # 마지막에서 처음으로 돌아오는 간선까지
                candidates = [w for u, v, w in edges if (u, v) == (a, b)]
                assert candidates, (n, edges, cycle)
                total += min(candidates)
            assert total < 0, (n, edges, cycle)
            assert len(set(cycle)) == len(cycle)
    assert found > 100


def test_find_negative_cycle_readme_graph():
    assert solution.find_negative_cycle(5, README_EDGES) is None
    cycle = solution.find_negative_cycle(5, README_CYCLE_EDGES)
    assert sorted(cycle) == [0, 1, 2]


def test_spfa_matches_bellman_ford():
    rng = random.Random(3)
    for _ in range(1000):
        n, edges = random_graph(rng)
        start = rng.randrange(n)
        expected_dist, expected_cycle = solution.bellman_ford(n, edges, start)
        dist, cycle = solution.spfa(build(n, edges), start)
        assert cycle == expected_cycle, (n, edges, start)
        if not cycle:
            assert dist == expected_dist, (n, edges, start)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 4\n1 2 4\n1 3 3\n2 3 -1\n3 1 -5\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "-1"
    monkeypatch.setattr("sys.stdin", io.StringIO("3 2\n1 2 4\n2 3 -1\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["4", "3"]
    monkeypatch.setattr("sys.stdin", io.StringIO("3 1\n1 2 4\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["4", "-1"]
