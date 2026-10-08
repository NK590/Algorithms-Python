"""solution.py 검증: 작은 네트워크의 모든 정수 유량을 나열하는 방법, 순열 전수 탐색과 무작위로 비교하고 유량 보존·볼록성 같은 성질을 확인"""
import io
import itertools
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
INF = float("inf")


def all_flows(n, edges, s, t):
    """(유량 값, 비용) 의 가능한 모든 쌍: 간선마다 0..용량 을 전수 탐색해 보존 법칙을 만족하는 것만."""
    results = {}
    for amounts in itertools.product(*[range(cap + 1) for _, _, cap, _ in edges]):
        balance = [0] * n
        cost = 0
        for (u, v, _, c), x in zip(edges, amounts):
            balance[u] -= x
            balance[v] += x
            cost += x * c
        if all(balance[v] == 0 for v in range(n) if v not in (s, t)):
            value = balance[t]
            if value >= 0 and (value not in results or cost < results[value]):
                results[value] = cost
    return results


def random_network(rng, dag):
    n = rng.randint(2, 5)
    edges = []
    for _ in range(rng.randint(1, 6)):
        if dag:
            u = rng.randrange(n - 1)
            v = rng.randint(u + 1, n - 1)
            cost = rng.randint(-4, 6)
        else:
            u, v = rng.randrange(n), rng.randrange(n)
            if u == v:
                continue
            cost = rng.randint(0, 6)
        edges.append((u, v, rng.randint(0, 2), cost))
    return n, edges


def build(n, edges):
    network = solution.MinCostFlow(n)
    ids = [network.add_edge(u, v, cap, c) for u, v, cap, c in edges]
    return network, ids


def test_min_cost_of_every_flow_value_matches_enumeration():
    rng = random.Random(0)
    for trial in range(400):
        n, edges = random_network(rng, dag=trial % 2 == 0)
        if not edges:
            continue
        s, t = 0, n - 1
        reference = all_flows(n, edges, s, t)
        best_value = max(reference)
        for algorithm in ("dijkstra", "spfa"):
            network, _ = build(n, edges)
            assert network.flow(s, t, algorithm=algorithm) == (best_value, reference[best_value]), (n, edges, algorithm)
            for limit in range(best_value + 1):  # 정확히 limit 만큼만 보내는 최소 비용
                network, _ = build(n, edges)
                assert network.flow(s, t, limit, algorithm) == (limit, reference[limit]), (n, edges, limit, algorithm)


def test_edge_flows_are_a_valid_flow_with_the_reported_cost():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(3, 12)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 5), rng.randint(0, 9)) for _ in range(rng.randint(3, 30))]
        edges = [e for e in edges if e[0] != e[1]]
        s, t = 0, n - 1
        network, ids = build(n, edges)
        value, cost = network.flow(s, t)
        balance = [0] * n
        total = 0
        for (u, v, cap, c), edge_id in zip(edges, ids):
            x = network.flow_on(edge_id)
            assert 0 <= x <= cap
            balance[u] -= x
            balance[v] += x
            total += x * c
        assert balance[t] == value == -balance[s] and total == cost
        assert all(balance[v] == 0 for v in range(n) if v not in (s, t))


def test_both_shortest_path_variants_agree_on_larger_graphs():
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randint(5, 25)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6), rng.randint(0, 20)) for _ in range(rng.randint(10, 80))]
        edges = [e for e in edges if e[0] != e[1]]
        results = []
        for algorithm in ("dijkstra", "spfa"):
            network, _ = build(n, edges)
            results.append(network.flow(0, n - 1, algorithm=algorithm))
        assert results[0] == results[1]


def test_negative_costs_without_a_negative_cycle():
    network = solution.MinCostFlow(4)
    network.add_edge(0, 1, 2, 5)
    network.add_edge(1, 3, 2, -3)
    network.add_edge(0, 2, 1, 1)
    network.add_edge(2, 3, 1, 1)
    assert network.flow(0, 3) == (3, 2 * 2 + 2)  # (5 - 3) * 2 + (1 + 1) * 1
    for algorithm in ("dijkstra", "spfa"):
        network = solution.MinCostFlow(3)
        network.add_edge(0, 1, 1, 4)
        network.add_edge(1, 2, 1, -9)
        assert network.flow(0, 2, algorithm=algorithm) == (1, -5)


def test_negative_cycle_is_rejected_for_both_variants():
    for algorithm in ("dijkstra", "spfa"):
        network = solution.MinCostFlow(3)
        network.add_edge(0, 1, 1, 1)
        network.add_edge(1, 2, 1, -5)
        network.add_edge(2, 1, 1, 2)
        network.add_edge(2, 0, 1, 1)
        with pytest.raises(ValueError, match="음의 사이클"):
            network.flow(0, 2, algorithm=algorithm)


def test_flow_curve_is_convex_and_matches_enumeration():
    rng = random.Random(3)
    for _ in range(300):
        n, edges = random_network(rng, dag=False)
        if not edges:
            continue
        s, t = 0, n - 1
        reference = all_flows(n, edges, s, t)
        network, _ = build(n, edges)
        network.flow(s, t)
        curve = network.flow_curve()
        assert curve[0] == (0, 0)
        slopes = [c for c, _ in network.augmentations]
        assert slopes == sorted(slopes)  # 경로 비용이 늘기만 한다: 볼록
        for (f0, c0), (f1, c1), slope in zip(curve, curve[1:], slopes):
            assert c1 - c0 == slope * (f1 - f0)
            for value in range(f0, f1 + 1):  # 조각 직선 위의 모든 정수 유량이 실제 최소 비용
                assert reference[value] == c0 + slope * (value - f0), (n, edges, value)


def test_degenerate_inputs():
    network = solution.MinCostFlow(3)
    network.add_edge(0, 1, 5, 2)
    assert network.flow(0, 2) == (0, 0)  # sink 에 닿을 수 없다
    assert network.flow_curve() == [(0, 0)]
    network = solution.MinCostFlow(2)
    network.add_edge(0, 1, 0, 1)
    assert network.flow(0, 1) == (0, 0)
    network = solution.MinCostFlow(2)
    network.add_edge(0, 1, 3, 4)
    network.add_edge(0, 1, 2, 1)  # 평행 간선: 싼 것부터
    assert network.flow(0, 1, 4) == (4, 2 * 1 + 2 * 4)
    network = solution.MinCostFlow(2)
    network.add_edge(0, 1, 3, 4)
    assert network.flow(0, 1, 0) == (0, 0)


def test_potentials_keep_every_residual_reduced_cost_non_negative():
    # 다익스트라는 줄인 비용 cost + h[u] - h[v] >= 0 이 모든 잔여 간선에서 성립할 때만 맞다 (음수여도 재삽입 때문에 답은 우연히 맞을 수 있어서 불변식을 직접 확인한다)
    rng = random.Random(6)
    for _ in range(150):
        n = rng.randint(3, 10)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 4), rng.randint(0, 9)) for _ in range(rng.randint(4, 25))]
        edges = [e for e in edges if e[0] != e[1]]
        network, _ = build(n, edges)
        for v in range(1, n):  # s 에서 모든 정점에 닿도록 (퍼텐셜이 모든 정점에서 의미를 갖게)
            network.add_edge(0, v, 1000, 1000)
        network.flow(0, n - 1, rng.randint(1, 8))
        h = network.potential
        for u in range(n):
            for e in network.adjacency[u]:
                if network.capacity[e] > 0:
                    assert network.cost[e] + h[u] - h[network.to[e]] >= 0, (n, edges, u, e)


def test_flow_can_be_called_again_and_the_curve_describes_only_the_last_call():
    network = solution.MinCostFlow(3)
    network.add_edge(0, 1, 2, 1)
    network.add_edge(1, 2, 2, 1)
    network.add_edge(0, 2, 2, 5)
    assert network.flow(0, 2, 1) == (1, 2)
    assert network.flow_curve() == [(0, 0), (1, 2)]
    assert network.flow(0, 2) == (3, 2 + 5 * 2)  # 앞서 보낸 1 은 그대로 두고 나머지 (싼 경로 1 + 비싼 경로 2) 를 보냄
    assert network.augmentations == [(2, 1), (5, 2)] and network.flow_curve() == [(0, 0), (1, 2), (3, 12)]


def test_invalid_input():
    network = solution.MinCostFlow(3)
    with pytest.raises(IndexError, match="정점"):
        network.add_edge(0, 3, 1, 1)
    with pytest.raises(IndexError, match="정점"):
        network.add_edge(-1, 1, 1, 1)
    with pytest.raises(IndexError, match="정점"):
        network.add_edge(3, 0, 1, 1)
    with pytest.raises(ValueError, match="용량"):
        network.add_edge(0, 1, -1, 1)
    with pytest.raises(ValueError, match="같습니다"):
        network.flow(1, 1)
    with pytest.raises(ValueError, match="algorithm"):
        network.flow(0, 1, algorithm="floyd")


def test_assignment_by_flow_matches_permutations():
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(1, 5)
        m = rng.randint(n, 6)
        cost = [[rng.randint(-5, 20) for _ in range(m)] for _ in range(n)]
        best = min(sum(cost[i][columns[i]] for i in range(n)) for columns in itertools.permutations(range(m), n))
        total, assignment = solution.assignment_by_flow(cost)
        assert total == best == sum(cost[i][assignment[i]] for i in range(n)) and len(set(assignment)) == n
    with pytest.raises(ValueError, match="행 수"):
        solution.assignment_by_flow([[1], [2]])
    assert solution.assignment_by_flow([]) == (0, [])


def test_large_random_network_is_fast():
    rng = random.Random(5)
    n = 1500
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 20), rng.randint(0, 50)) for _ in range(9000)]
    edges = [e for e in edges if e[0] != e[1]]
    results = []
    started = time.perf_counter()
    for algorithm in ("dijkstra", "spfa"):
        network, _ = build(n, edges)
        results.append(network.flow(0, n - 1, algorithm=algorithm))
    assert time.perf_counter() - started < 60
    assert results[0] == results[1] and results[0][0] > 0


def test_main_hot_blooded_workers_format(monkeypatch, capsys):
    text = "4 4\n2 1 3 2 1\n2 1 2 3 4\n2 2 2 4 1\n1 3 5\n"
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(text.encode())))
    solution.main()
    assert capsys.readouterr().out == "4\n9\n"
