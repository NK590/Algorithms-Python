"""solution.py 검증: 간선의 모든 부분집합을 나열하는 브루트포스와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def components_of(n, edge_subset):
    """간선 부분집합이 만드는 연결 요소 수. (사이클이 있으면 None)"""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    comps = n
    for u, v, _ in edge_subset:
        ru, rv = find(u), find(v)
        if ru == rv:
            return None
        parent[ru] = rv
        comps -= 1
    return comps


def brute_force_forest(n, edges, maximize=False):
    """사이클이 없는 간선 부분집합 중 연결 요소 수가 원래 그래프와 같은(= 신장 숲인) 것의 최적 가중치 합"""
    original = components_of_graph(n, edges)
    best = None
    for size in range(0, n):
        for subset in itertools.combinations(edges, size):
            if components_of(n, subset) == original:
                total = sum(w for _, _, w in subset)
                if best is None or (total > best if maximize else total < best):
                    best = total
    return best


def components_of_graph(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    comps = n
    for u, v, _ in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            comps -= 1
    return comps


def random_graph(rng, low=1):
    n = rng.randint(1, 6)
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(rng.randint(0, 9))]
    return n, edges


def test_readme_example():
    edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)]
    total, chosen = solution.kruskal(6, edges)
    assert total == 13
    assert chosen == [(0, 2, 1), (1, 2, 2), (3, 4, 2), (4, 5, 3), (1, 3, 5)]


def test_matches_brute_force_minimum_spanning_forest():
    rng = random.Random(0)
    for _ in range(600):
        n, edges = random_graph(rng, low=-3)
        total, chosen = solution.kruskal(n, edges)
        assert total == brute_force_forest(n, edges), (n, edges)
        assert total == sum(w for _, _, w in chosen)
        assert components_of(n, chosen) == components_of_graph(n, edges)  # 사이클 없이 같은 연결 요소를 이었는가


def test_matches_brute_force_maximum_spanning_forest():
    rng = random.Random(1)
    for _ in range(400):
        n, edges = random_graph(rng)
        total, _ = solution.kruskal(n, edges, maximize=True)
        assert total == brute_force_forest(n, edges, maximize=True), (n, edges)


def test_special_cases():
    assert solution.kruskal(1, []) == (0, [])
    assert solution.kruskal(3, [(0, 0, 5), (1, 1, 5)]) == (0, [])  # 자기 자신으로 가는 간선은 쓰이지 않는다
    assert solution.kruskal(2, [(0, 1, 5), (0, 1, 3), (1, 0, 4)]) == (3, [(0, 1, 3)])  # 평행 간선은 가장 싼 것
    total, chosen = solution.kruskal(4, [(0, 1, 7), (2, 3, 2)])  # 연결되지 않은 그래프
    assert (total, len(chosen)) == (9, 2)


def test_early_exit_does_not_change_the_result():
    # 연결된 그래프에서 n-1 개를 채택하면 멈추는 최적화가 있어도 결과는 같다
    edges = [(i, i + 1, 1) for i in range(99)] + [(i, i + 2, 5) for i in range(98)]
    assert solution.kruskal(100, edges)[0] == 99


def brute_force_clusters(n, edges, k):
    """연결 요소가 k 개 이하가 되도록 사이클 없이 고른 간선 합의 최솟값"""
    best = None
    for size in range(0, n):
        for subset in itertools.combinations(edges, size):
            comps = components_of(n, subset)
            if comps is not None and comps <= k:
                total = sum(w for _, _, w in subset)
                best = total if best is None else min(best, total)
    return best


def test_kruskal_until_components_matches_brute_force():
    rng = random.Random(2)
    for _ in range(400):
        n, edges = random_graph(rng)
        k = rng.randint(1, n)
        assert solution.kruskal_until_components(n, edges, k) == brute_force_clusters(n, edges, k), (n, edges, k)
    # 연결 요소 2개로 나누기 = MST 에서 가장 비싼 간선 하나를 빼기
    edges = [(0, 1, 1), (1, 2, 2), (2, 3, 6), (3, 4, 3), (0, 4, 9)]
    total, chosen = solution.kruskal(5, edges)
    assert solution.kruskal_until_components(5, edges, 2) == total - max(w for _, _, w in chosen)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 3\n1 2 1\n2 3 2\n1 3 3\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
