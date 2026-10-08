"""solution.py 검증: 전이적 폐쇄(모든 쌍의 도달 가능성)로 정의대로 SCC 를 구한 결과와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def reachability(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for a, b in edges:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return reach


def brute_force_partition(n, edges):
    reach = reachability(n, edges)
    return sorted(sorted(j for j in range(n) if reach[i][j] and reach[j][i]) for i in range(n) if all(not (reach[i][j] and reach[j][i]) for j in range(i)))


def partition(components):
    return sorted(sorted(c) for c in components)


def random_graph(rng, n, density):
    return [(a, b) for a in range(n) for b in range(n) if a != b and rng.random() < density]


def test_both_algorithms_match_definition():
    rng = random.Random(0)
    for _ in range(600):
        n = rng.randint(0, 9)
        edges = random_graph(rng, n, rng.choice([0.05, 0.15, 0.3]))
        expected = brute_force_partition(n, edges)
        assert partition(solution.tarjan_scc(n, edges)) == expected, (n, edges)
        assert partition(solution.kosaraju_scc(n, edges)) == expected, (n, edges)


def test_self_loops_and_parallel_edges_do_not_matter():
    edges = [(0, 0), (0, 1), (0, 1), (1, 1), (1, 2), (2, 0), (2, 3), (3, 3)]
    for algorithm in (solution.tarjan_scc, solution.kosaraju_scc):
        assert partition(algorithm(4, edges)) == [[0, 1, 2], [3]]


def test_output_order_is_reverse_topological_for_tarjan_and_topological_for_kosaraju():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 10)
        edges = random_graph(rng, n, 0.15)
        tarjan = solution.tarjan_scc(n, edges)
        kosaraju = solution.kosaraju_scc(n, edges)
        tarjan_ids = solution.component_ids(n, tarjan)
        kosaraju_ids = solution.component_ids(n, kosaraju)
        for a, b in edges:
            if tarjan_ids[a] != tarjan_ids[b]:
                assert tarjan_ids[a] > tarjan_ids[b], (n, edges)
            if kosaraju_ids[a] != kosaraju_ids[b]:
                assert kosaraju_ids[a] < kosaraju_ids[b], (n, edges)


def test_condensation_is_a_forward_dag():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 10)
        edges = random_graph(rng, n, 0.2)
        ids, dag = solution.condensation(n, edges)
        assert len(dag) == len(set(ids))
        for source, targets in enumerate(dag):
            assert all(target > source for target in targets)
        for a, b in edges:
            assert ids[a] == ids[b] or ids[b] in dag[ids[a]]


def strongly_connected(n, edges):
    reach = reachability(n, edges)
    return all(reach[i][j] for i in range(n) for j in range(n))


def test_min_edges_to_make_strongly_connected_matches_brute_force():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(1, 4)
        edges = random_graph(rng, n, rng.choice([0.1, 0.3]))
        candidates = [(a, b) for a in range(n) for b in range(n) if a != b]
        expected = None
        for k in range(0, 5):
            if any(strongly_connected(n, edges + list(extra)) for extra in itertools.combinations(candidates, k)):
                expected = k
                break
        assert solution.min_edges_to_make_strongly_connected(n, edges) == expected, (n, edges)
    assert solution.min_edges_to_make_strongly_connected(0, []) == 0


def test_deep_graphs_do_not_recurse():
    n = 100_000
    chain = [(i, i + 1) for i in range(n - 1)]
    assert len(solution.tarjan_scc(n, chain)) == n and len(solution.kosaraju_scc(n, chain)) == n
    cycle = chain + [(n - 1, 0)]
    assert len(solution.tarjan_scc(n, cycle)) == 1 and len(solution.kosaraju_scc(n, cycle)) == 1


def test_large_random_graph_agreement():
    rng = random.Random(4)
    n, m = 50_000, 120_000
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
    assert partition(solution.tarjan_scc(n, edges)) == partition(solution.kosaraju_scc(n, edges))


def test_main(monkeypatch, capsys):
    text = "7 9\n1 4\n4 5\n5 1\n1 6\n6 7\n2 5\n7 2\n3 7\n3 6\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["2", "1 2 4 5 6 7 -1", "3 -1"]
    text = "4 4\n1 2\n2 1\n3 4\n4 3\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["2", "1 2 -1", "3 4 -1"]
    # 타잔은 싱크 쪽 SCC 를 먼저 찾지만 출력은 가장 작은 정점 번호 순이다
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"2 1\n1 2\n")))
    solution.main()
    assert capsys.readouterr().out.strip().splitlines() == ["2", "1 -1", "2 -1"]
