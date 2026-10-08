"""solution.py 검증: 손으로 따라간 예제 + 플로이드-워셜(브루트 포스)과의 랜덤 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = solution.INF


def build(n: int, edges: list[tuple[int, int, int]]) -> list[list[tuple[int, int]]]:
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph


def floyd_warshall(n: int, edges: list[tuple[int, int, int]]) -> list[list[float]]:
    """다익스트라와 전혀 다른 방식으로 모든 쌍의 최단 거리를 구하는, 느리지만 확실한 기준"""
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def random_graph(rng: random.Random) -> tuple[int, list[tuple[int, int, int]]]:
    n = rng.randint(1, 8)
    # 자기 자신으로 가는 간선, 같은 쌍의 중복 간선, 가중치 0 이 모두 나올 수 있게 한다
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 10)) for _ in range(rng.randint(0, 20))]
    return n, edges


# README "손으로 따라가기"의 그래프: A=0, B=1, C=2, D=3, E=4
README_EDGES = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (2, 3, 8), (1, 3, 5), (3, 4, 3)]


def test_readme_example():
    assert solution.dijkstra(build(5, README_EDGES), 0) == [0, 3, 1, 8, 11]


def test_unreachable_vertices_are_inf():
    graph = build(4, [(0, 1, 5), (2, 3, 1)])
    assert solution.dijkstra(graph, 0) == [0, 5, INF, INF]


def test_edges_are_directed():
    graph = build(2, [(0, 1, 3)])
    assert solution.dijkstra(graph, 0) == [0, 3]
    assert solution.dijkstra(graph, 1) == [INF, 0]


def test_single_vertex():
    assert solution.dijkstra([[]], 0) == [0]


def test_zero_weights_cycles_self_loops_and_parallel_edges():
    edges = [(0, 0, 4), (0, 1, 0), (1, 0, 0), (1, 2, 7), (1, 2, 3), (2, 1, 0)]
    assert solution.dijkstra(build(3, edges), 0) == [0, 0, 3]


def test_long_chain_is_handled_without_recursion():
    n = 50_000
    graph = build(n, [(i, i + 1, 1) for i in range(n - 1)])
    assert solution.dijkstra(graph, 0)[-1] == n - 1


def test_matches_floyd_warshall_on_random_graphs():
    rng = random.Random(0)  # 시드를 고정해 실패를 재현할 수 있게 한다
    for _ in range(500):
        n, edges = random_graph(rng)
        graph = build(n, edges)
        expected = floyd_warshall(n, edges)
        for start in range(n):
            assert solution.dijkstra(graph, start) == expected[start], (n, edges, start)


def test_with_prev_gives_same_distances_and_valid_paths():
    rng = random.Random(1)
    for _ in range(300):
        n, edges = random_graph(rng)
        graph = build(n, edges)
        cheapest = {}  # 같은 (u, v) 간선이 여럿이면 가장 싼 것만 쓰이므로 그 가중치로 경로 비용을 계산한다
        for u, v, w in edges:
            cheapest[(u, v)] = min(w, cheapest.get((u, v), INF))
        for start in range(n):
            dist, prev = solution.dijkstra_with_prev(graph, start)
            assert dist == solution.dijkstra(graph, start)
            for target in range(n):
                path = solution.restore_path(prev, start, target)
                if dist[target] == INF:
                    assert path is None
                    continue
                assert path[0] == start and path[-1] == target
                assert sum(cheapest[(a, b)] for a, b in zip(path, path[1:])) == dist[target]


def test_restore_path_to_start_is_just_start():
    _, prev = solution.dijkstra_with_prev(build(3, [(0, 1, 1)]), 0)
    assert solution.restore_path(prev, 0, 0) == [0]
    assert solution.restore_path(prev, 0, 1) == [0, 1]
    assert solution.restore_path(prev, 0, 2) is None


def test_readme_negative_edge_example():
    # s=0, a=1, b=2 : s→a 3, s→b 4, b→a -2.  진짜 최단 거리는 a = 2 (s→b→a).
    # 이 구현은 낡은 항목만 건너뛰고 "확정" 표시를 하지 않아 이 예에서는 맞지만,
    # 음수 간선에서는 시간 복잡도 보장이 없으니 쓰면 안 된다. (README 참고)
    assert solution.dijkstra(build(3, [(0, 1, 3), (0, 2, 4), (2, 1, -2)]), 0) == [0, 2, 4]


def test_main_reads_stdin_and_prints_inf(monkeypatch, capsys):
    stdin = "5 4\n1\n1 2 5\n1 3 2\n3 2 1\n2 4 1\n"  # 5번 정점은 도달할 수 없다
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
    solution.main()
    assert capsys.readouterr().out.split() == ["0", "3", "2", "4", "INF"]
