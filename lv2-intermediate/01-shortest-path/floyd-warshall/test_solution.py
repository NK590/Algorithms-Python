"""solution.py 검증: 정점마다 벨만-포드를 돌린 결과(독립 구현)와 비교, 경로·폐쇄·최단 사이클은 직접 열거와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = solution.INF


def bellman_ford_all_pairs(n, edges):
    """정점마다 벨만-포드. 음수 사이클이 없는 그래프에서 모든 쌍의 최단 거리의 기준"""
    result = []
    for s in range(n):
        dist = [INF] * n
        dist[s] = 0
        for _ in range(n):
            for u, v, w in edges:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        result.append(dist)
    return result


def has_negative_cycle_by_bf(n, edges):
    """모든 정점에서 시작하는 벨만-포드가 n 번째 라운드에도 갱신되는가"""
    for s in range(n):
        dist = [INF] * n
        dist[s] = 0
        for _ in range(n):
            changed = False
            for u, v, w in edges:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed = True
            if not changed:
                break
        else:
            return True
    return False


def random_graph(rng, low=0, high=9):
    n = rng.randint(1, 6)
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, high)) for _ in range(rng.randint(0, 14))]
    return n, edges


README_EDGES = [(0, 1, 10), (0, 2, 2), (0, 3, 4), (1, 2, 1), (1, 3, -3), (2, 3, 2), (3, 0, 20)]


def test_readme_example():
    assert solution.floyd_warshall(4, README_EDGES) == [
        [0, 10, 2, 4],
        [17, 0, 1, -3],
        [22, 32, 0, 2],
        [20, 30, 22, 0],
    ]


def test_matches_bellman_ford_from_every_vertex():
    rng = random.Random(0)
    checked = 0
    for _ in range(800):
        n, edges = random_graph(rng, low=-3, high=9)
        dist = solution.floyd_warshall(n, edges)
        if has_negative_cycle_by_bf(n, edges):
            assert solution.has_negative_cycle(dist), (n, edges)
            continue
        assert not solution.has_negative_cycle(dist)
        assert dist == bellman_ford_all_pairs(n, edges), (n, edges)
        checked += 1
    assert checked > 300


def test_duplicate_edges_and_self_loops_keep_the_minimum():
    dist = solution.floyd_warshall(2, [(0, 1, 5), (0, 1, 2), (0, 0, 7), (1, 1, 3)])
    assert dist == [[0, 2], [INF, 0]]
    assert solution.floyd_warshall(1, []) == [[0]]
    assert solution.floyd_warshall(0, []) == []


def test_negative_cycle_with_total_exactly_minus_one():
    assert solution.has_negative_cycle(solution.floyd_warshall(1, [(0, 0, -1)]))
    assert solution.has_negative_cycle(solution.floyd_warshall(2, [(0, 1, 1), (1, 0, -2)]))


def test_negative_cycle_is_detected():
    dist = solution.floyd_warshall(3, [(0, 1, 1), (1, 2, -3), (2, 0, 1)])
    assert solution.has_negative_cycle(dist)
    assert not solution.has_negative_cycle(solution.floyd_warshall(3, [(0, 1, 1), (1, 2, -1), (2, 0, 1)]))


def test_restore_path_follows_a_shortest_path():
    rng = random.Random(1)
    for _ in range(500):
        n, edges = random_graph(rng, low=-2, high=9)
        dist, next_hop = solution.floyd_warshall_with_next(n, edges)
        if solution.has_negative_cycle(dist):
            continue
        assert dist == solution.floyd_warshall(n, edges)
        for u in range(n):
            for v in range(n):
                path = solution.restore_path(next_hop, u, v)
                if dist[u][v] == INF:
                    assert path == []
                    continue
                assert path[0] == u and path[-1] == v
                total = sum(min(w for a, b, w in edges if (a, b) == (x, y)) for x, y in zip(path, path[1:]))
                assert total == dist[u][v], (n, edges, u, v, path)


def reachable_by_dfs(n, edges, source):
    seen, stack = {source}, [source]
    while stack:
        u = stack.pop()
        for a, b in edges:
            if a == u and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen


def test_transitive_closure_matches_dfs():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
        reach = solution.transitive_closure(n, edges)
        for u in range(n):
            expected = reachable_by_dfs(n, edges, u)
            assert [v for v in range(n) if reach[u][v]] == sorted(expected), (n, edges, u)


def shortest_cycle_by_enumeration(n, edges):
    best = INF
    cheapest = {}
    for u, v, w in edges:
        cheapest[(u, v)] = min(w, cheapest.get((u, v), INF))
    for length in range(1, n + 1):
        for vertices in itertools.permutations(range(n), length):
            ok = True
            total = 0
            for a, b in zip(vertices, vertices[1:] + vertices[:1]):
                if (a, b) not in cheapest:
                    ok = False
                    break
                total += cheapest[(a, b)]
            if ok:
                best = min(best, total)
    return best


def test_shortest_cycle_matches_enumeration():
    rng = random.Random(3)
    for _ in range(300):
        n, edges = random_graph(rng, low=1, high=9)
        n = min(n, 5)
        edges = [(u, v, w) for u, v, w in edges if u < n and v < n]
        assert solution.shortest_cycle(n, edges) == shortest_cycle_by_enumeration(n, edges), (n, edges)
    assert solution.shortest_cycle(3, [(0, 1, 1), (1, 2, 1)]) == INF  # DAG 에는 사이클이 없다
    assert solution.shortest_cycle(2, [(0, 0, 4)]) == 4  # 자기 자신으로 가는 간선도 사이클


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n3\n1 2 4\n2 3 1\n1 3 10\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["0 4 5", "0 0 1", "0 0 0"]
