"""solution.py 검증: 세 가지 표현이 같은 그래프를 나타내는지 서로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = solution.INF


def random_simple_graph(rng, directed):
    n = rng.randint(1, 8)
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (directed or u < v)]
    edges = [p for p in pairs if rng.random() < 0.4]
    return n, edges


def test_readme_example_undirected():
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    assert solution.build_adjacency_list(4, edges) == [[1, 2], [0, 2], [0, 1, 3], [2]]
    assert solution.build_adjacency_matrix(4, edges) == [
        [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]]


def test_readme_example_directed_and_weighted():
    edges = [(0, 1, 5), (1, 2, 3), (2, 0, 4)]
    assert solution.build_weighted_adjacency_list(3, edges, directed=True) == [[(1, 5)], [(2, 3)], [(0, 4)]]
    matrix = solution.build_adjacency_matrix(3, edges, directed=True, no_edge=INF)
    assert matrix[0][1] == 5 and matrix[1][0] == INF and matrix[2][0] == 4


def test_matrix_and_list_describe_the_same_graph():
    rng = random.Random(0)
    for directed in (False, True):
        for _ in range(200):
            n, edges = random_simple_graph(rng, directed)
            matrix = solution.build_adjacency_matrix(n, edges, directed)
            adj = solution.build_adjacency_list(n, edges, directed)
            assert [sorted(row) for row in adj] == solution.matrix_to_list(matrix)
            assert solution.list_to_matrix(adj) == matrix
            for u in range(n):
                for v in range(n):
                    assert solution.has_edge_matrix(matrix, u, v) == solution.has_edge_list(adj, u, v)


def test_undirected_matrix_is_symmetric():
    rng = random.Random(1)
    for _ in range(100):
        n, edges = random_simple_graph(rng, False)
        matrix = solution.build_adjacency_matrix(n, edges)
        assert all(matrix[u][v] == matrix[v][u] for u in range(n) for v in range(n))


def test_degree_sums():
    rng = random.Random(2)
    for _ in range(200):
        n, edges = random_simple_graph(rng, False)
        assert sum(solution.degrees(solution.build_adjacency_list(n, edges))) == 2 * len(edges)
        n, edges = random_simple_graph(rng, True)
        indeg, outdeg = solution.degrees(solution.build_adjacency_list(n, edges, True), directed=True)
        assert sum(indeg) == sum(outdeg) == len(edges)


def test_self_loop_and_parallel_edges():
    assert solution.build_adjacency_list(2, [(0, 0)]) == [[0], []]  # 무방향 자기 간선은 한 번만
    assert solution.build_adjacency_list(2, [(0, 1), (0, 1)]) == [[1, 1], [0, 0]]  # 중복 간선은 그대로 쌓인다
    matrix = solution.build_adjacency_matrix(2, [(0, 1, 3), (0, 1, 7)])
    assert matrix[0][1] == 7  # 행렬에는 마지막 가중치만 남는다


def test_zero_weight_needs_a_different_no_edge_value():
    matrix = solution.build_adjacency_matrix(2, [(0, 1, 0)], no_edge=INF)
    assert solution.has_edge_matrix(matrix, 0, 1, no_edge=INF)
    plain = solution.build_adjacency_matrix(2, [(0, 1, 0)])  # no_edge=0 이면 가중치 0 간선이 "없음"과 구분되지 않는다
    assert not solution.has_edge_matrix(plain, 0, 1)


def test_main_prints_neighbors_one_based(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4 3\n1 2\n1 3\n3 4\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["1 : 2 3", "2 : 1", "3 : 1 4", "4 : 3"]
