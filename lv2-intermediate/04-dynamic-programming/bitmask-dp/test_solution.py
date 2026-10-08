"""solution.py 검증: 모든 방문 순서(순열)를 시도하는 브루트포스와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)
INF = solution.INF


def tour_cost(dist, route):
    total = 0
    for a, b in zip(route, route[1:]):
        total += dist[a][b]
    return total


def brute_force_tsp(dist):
    n = len(dist)
    if n <= 1:
        return 0
    best = INF
    for perm in itertools.permutations(range(1, n)):
        route = [0, *perm, 0]
        best = min(best, tour_cost(dist, route))
    return best


def random_dist(rng, n, hole=0.0):
    return [
        [0 if i == j else (INF if rng.random() < hole else rng.randint(1, 20)) for j in range(n)]
        for i in range(n)
    ]


def test_tsp_matches_all_permutations():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 7)
        dist = random_dist(rng, n, hole=0.25)  # 일부 길은 없다(비대칭도 가능)
        assert solution.tsp(dist) == brute_force_tsp(dist), dist


def test_tsp_with_path_gives_a_real_optimal_tour():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 7)
        dist = random_dist(rng, n, hole=0.2)
        cost, route = solution.tsp_with_path(dist)
        assert cost == brute_force_tsp(dist), dist
        if cost == INF:
            assert route == []
            continue
        if n == 1:
            assert route == [0, 0]
            continue
        assert route[0] == 0 and route[-1] == 0 and sorted(route[:-1]) == list(range(n))
        assert tour_cost(dist, route) == cost


def test_readme_example():
    dist = [[0, 10, 15, 20], [5, 0, 9, 10], [6, 13, 0, 12], [8, 8, 9, 0]]
    assert solution.tsp(dist) == 35
    cost, route = solution.tsp_with_path(dist)
    assert cost == 35 and route[0] == route[-1] == 0 and sorted(route[:-1]) == [0, 1, 2, 3]
    assert tour_cost(dist, route) == 35


def test_tsp_special_cases():
    assert solution.tsp([]) == 0 and solution.tsp([[0]]) == 0
    assert solution.tsp([[0, 3], [4, 0]]) == 7
    assert solution.tsp([[0, 3], [INF, 0]]) == INF  # 돌아오는 길이 없다
    assert solution.tsp_with_path([[0, 3], [INF, 0]]) == (INF, [])


def test_assignment_matches_all_permutations():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(0, 7)
        cost = [[rng.randint(1, 30) for _ in range(n)] for _ in range(n)]
        expected = min((sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n))), default=0)
        assert solution.assignment_min_cost(cost) == expected, cost
    # 각 사람이 가장 싼 일을 고르는 그리디는 틀린다
    assert solution.assignment_min_cost([[1, 2], [1, 100]]) == 3


def test_hamiltonian_paths_match_all_permutations():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(0, 6)
        adj = [[1 if i != j and rng.random() < 0.5 else 0 for j in range(n)] for i in range(n)]
        expected = 0
        if n:
            for p in itertools.permutations(range(n)):
                if all(adj[a][b] for a, b in zip(p, p[1:])):
                    expected += 1
        assert solution.count_hamiltonian_paths(adj) == expected, adj
    complete = [[1 if i != j else 0 for j in range(5)] for i in range(5)]
    assert solution.count_hamiltonian_paths(complete) == 120  # 5!


def test_main_treats_zero_as_no_road(monkeypatch, capsys):
    # 0 → 1 → 2 → 0 (각 10) 만 길이 있다. 0 을 비용 0 인 길로 읽으면 0 → 2 → 1 → 0 이 공짜가 되어 틀린다
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n0 10 0\n0 0 10\n10 0 0\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "30"


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n0 10 15 20\n5 0 9 10\n6 13 0 12\n8 8 9 0\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "35"
