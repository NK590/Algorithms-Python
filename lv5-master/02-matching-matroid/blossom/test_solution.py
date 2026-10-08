"""solution.py 검증: 비트마스크 전수 탐색, 투테-버지 공식, 증명서(갈라이-에드먼즈의 A 집합)로 최대 매칭의 크기를 독립적으로 확인"""
import io
import itertools
import random
import time
from functools import lru_cache

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def edge_set(edges):
    return {(min(a, b), max(a, b)) for a, b in edges if a != b}


def brute_matching(n, edges):
    """비트마스크로 가장 작은 정점부터 '짝을 짓거나 건너뛰거나' 를 나열하는 최대 매칭 크기."""
    adj = [0] * n
    for a, b in edge_set(edges):
        adj[a] |= 1 << b
        adj[b] |= 1 << a

    @lru_cache(maxsize=None)
    def best(mask):
        if mask == 0:
            return 0
        v = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << v)
        result = best(rest)  # v 를 건너뛴다
        candidates = adj[v] & rest
        while candidates:
            u = (candidates & -candidates).bit_length() - 1
            candidates &= candidates - 1
            result = max(result, 1 + best(rest & ~(1 << u)))
        return result

    return best((1 << n) - 1)


def components(n, edges, removed=()):
    """removed 를 뺀 그래프의 연결 성분 (정점 집합의 목록)."""
    removed = set(removed)
    adj = {v: [] for v in range(n) if v not in removed}
    for a, b in edge_set(edges):
        if a not in removed and b not in removed:
            adj[a].append(b)
            adj[b].append(a)
    seen = set()
    result = []
    for s in adj:
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            v = stack.pop()
            comp.append(v)
            for to in adj[v]:
                if to not in seen:
                    seen.add(to)
                    stack.append(to)
        result.append(comp)
    return result


def odd_components(n, edges, removed=()):
    return sum(1 for comp in components(n, edges, removed) if len(comp) % 2 == 1)


def tutte_berge_bound(n, edges, removed):
    """투테-버지: 어떤 U 에 대해서도 최대 매칭 ≤ (n + |U| - odd(G - U)) / 2. 등호가 나오는 U 가 있으면 최적의 증명서."""
    return (n + len(removed) - odd_components(n, edges, removed)) / 2


def assert_valid(n, edges, size, mate):
    es = edge_set(edges)
    assert len(mate) == n
    pairs = 0
    for v in range(n):
        if mate[v] == -1:
            continue
        assert 0 <= mate[v] < n and mate[mate[v]] == v and mate[v] != v
        assert (min(v, mate[v]), max(v, mate[v])) in es
        pairs += 1
    assert pairs == 2 * size


def random_graph(rng, n, p):
    return [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]


def test_small_known_graphs():
    cases = [
        (0, [], 0),
        (1, [], 0),
        (2, [(0, 1)], 1),
        (3, [(0, 1), (1, 2), (2, 0)], 1),  # 삼각형: 꽃 하나
        (4, [(0, 1), (1, 2), (2, 0), (2, 3)], 2),  # 삼각형 + 꼬리
        (5, [(i, (i + 1) % 5) for i in range(5)], 2),  # 5-사이클
        (6, [(i, (i + 1) % 6) for i in range(6)], 3),
        (4, [(0, 1), (0, 2), (0, 3)], 1),  # 별
        (4, [(2, 0), (0, 1), (1, 3)], 2),  # 탐욕(작은 번호 우선) 은 0-1 을 먼저 고르지만 최적은 2-0, 1-3
    ]
    for n, edges, expected in cases:
        size, mate = solution.max_matching(n, edges)
        assert size == expected, (n, edges)
        assert_valid(n, edges, size, mate)


def test_petersen_graph_has_a_perfect_matching():
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    edges = outer + spokes + inner
    size, mate = solution.max_matching(10, edges)
    assert size == 5
    assert_valid(10, edges, size, mate)


def test_complete_graphs():
    for n in range(1, 14):
        edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
        size, mate = solution.max_matching(n, edges)
        assert size == n // 2
        assert_valid(n, edges, size, mate)


def test_odd_cycle_with_pendants_needs_a_blossom():
    # 5-사이클의 각 정점에 잎이 하나씩: 꽃을 수축하지 않으면 증가 경로를 놓치기 쉬운 모양. 잎과 짝지으면 5개
    edges = [(i, (i + 1) % 5) for i in range(5)] + [(i, 5 + i) for i in range(5)]
    size, mate = solution.max_matching(10, edges)
    assert size == 5
    assert_valid(10, edges, size, mate)


def test_nested_blossoms():
    # 삼각형 세 개를 꼭짓점 하나씩 공유하며 이어 붙인 뒤(바깥 삼각형의 꼭짓점이 안쪽 꽃) 꼬리를 단다
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2), (4, 5), (5, 6), (6, 4), (6, 7)]
    n = 8
    size, mate = solution.max_matching(n, edges)
    assert size == brute_matching(n, edges) == 4
    assert_valid(n, edges, size, mate)


def test_matches_brute_force_on_random_graphs():
    rng = random.Random(0)
    for _ in range(1500):
        n = rng.randint(0, 11)
        p = rng.choice([0.1, 0.2, 0.3, 0.5, 0.8])
        edges = random_graph(rng, n, p)
        rng.shuffle(edges)
        edges = [(b, a) if rng.random() < 0.5 else (a, b) for a, b in edges]
        size, mate = solution.max_matching(n, edges)
        assert size == brute_matching(n, edges), (n, edges)
        assert_valid(n, edges, size, mate)


def test_matches_tutte_berge_formula_by_subset_enumeration():
    """투테-버지 공식 ν = min_U (n + |U| - odd(G - U)) / 2 를 모든 U 로 계산해 비교 (비트마스크 탐색과 별개의 길)."""
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 9)
        edges = random_graph(rng, n, rng.choice([0.15, 0.3, 0.5]))
        expected = min(
            tutte_berge_bound(n, edges, subset)
            for r in range(n + 1)
            for subset in itertools.combinations(range(n), r)
        )
        size, _ = solution.max_matching(n, edges)
        assert size == expected, (n, edges)


def test_edges_in_any_form_give_the_same_size():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(2, 10)
        edges = random_graph(rng, n, 0.3)
        noisy = edges + [(b, a) for a, b in edges[:3]] + [(v, v) for v in range(n)] + edges[:2]
        assert solution.max_matching(n, noisy)[0] == brute_matching(n, edges)


def test_invalid_vertex_is_rejected():
    with pytest.raises(ValueError, match="범위"):
        solution.max_matching(3, [(0, 3)])
    with pytest.raises(ValueError, match="범위"):
        solution.max_matching(3, [(-1, 2)])


def test_gallai_edmonds_decomposition_matches_definition():
    rng = random.Random(3)
    for _ in range(600):
        n = rng.randint(1, 10)
        edges = random_graph(rng, n, rng.choice([0.1, 0.2, 0.35, 0.6]))
        info = solution.gallai_edmonds(n, edges)
        nu = brute_matching(n, edges)
        assert info["size"] == nu
        assert_valid(n, edges, info["size"], info["mate"])
        # 정의: D = 어떤 최대 매칭에서 짝이 없을 수 있는 정점 = 지워도 ν 가 줄지 않는 정점
        keep = [v for v in range(n)]
        expected_d = []
        for v in range(n):
            rest = [u for u in keep if u != v]
            relabel = {u: i for i, u in enumerate(rest)}
            sub = [(relabel[a], relabel[b]) for a, b in edge_set(edges) if a != v and b != v]
            if brute_matching(n - 1, sub) == nu:
                expected_d.append(v)
        assert info["D"] == expected_d, (n, edges)
        d_set = set(info["D"])
        a_set = {to for a, b in edge_set(edges) for v, to in ((a, b), (b, a)) if v in d_set and to not in d_set}
        assert info["A"] == sorted(a_set)
        assert info["C"] == sorted(set(range(n)) - d_set - a_set)
        # 투테-버지 증명서: n - 2ν = odd(G - A) - |A|
        assert n - 2 * nu == odd_components(n, edges, info["A"]) - len(info["A"])


def test_gallai_edmonds_structure_theorem():
    """D 의 성분은 홀수 크기의 인수-임계 그래프, C 는 완전 매칭을 가지고, 최대 매칭은 A 를 D 의 서로 다른 성분과 하나씩 짝짓는다."""
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(2, 10)
        edges = random_graph(rng, n, rng.choice([0.15, 0.3, 0.5]))
        info = solution.gallai_edmonds(n, edges)
        d_set, a_set, c_set = set(info["D"]), set(info["A"]), set(info["C"])
        es = edge_set(edges)

        def induced(vertices):
            vs = sorted(vertices)
            relabel = {u: i for i, u in enumerate(vs)}
            return len(vs), [(relabel[a], relabel[b]) for a, b in es if a in relabel and b in relabel]

        d_components = components(n, [(a, b) for a, b in es if a in d_set and b in d_set], removed=set(range(n)) - d_set)
        for comp in d_components:
            assert len(comp) % 2 == 1
            m, sub = induced(comp)
            for drop in range(m):  # 인수-임계: 어느 정점을 지워도 완전 매칭
                rest = [u for u in range(m) if u != drop]
                relabel = {u: i for i, u in enumerate(rest)}
                sub2 = [(relabel[a], relabel[b]) for a, b in sub if a != drop and b != drop]
                assert brute_matching(m - 1, sub2) == (m - 1) // 2
        if c_set:
            m, sub = induced(c_set)
            assert brute_matching(m, sub) * 2 == m
        # 최대 매칭: A 의 정점은 모두 D 와 짝, C 안에서는 완전 매칭
        mate = info["mate"]
        assert all(mate[v] in d_set for v in a_set)
        comp_of = {v: i for i, comp in enumerate(d_components) for v in comp}
        partners = [comp_of[mate[a]] for a in a_set]
        assert len(set(partners)) == len(partners)  # A 의 정점들은 D 의 서로 다른 성분과 짝
        for i, comp in enumerate(d_components):  # 각 성분은 한 정점만 빼고 성분 안에서 완전 매칭, 그 한 정점은 A 와 짝이거나 짝이 없다
            outside = [v for v in comp if mate[v] not in comp]
            assert len(outside) == 1
            assert (mate[outside[0]] in a_set) == (i in partners)
            assert (mate[outside[0]] == -1) == (i not in partners)
        assert all(mate[v] in c_set for v in c_set)
        assert all(mate[v] != -1 for v in a_set | c_set)


def alternating_path_exists(adj, mate, root):
    """root(짝 없음) 에서 시작해 '매칭에 없는 간선, 있는 간선, …' 을 번갈아 밟아 짝 없는 정점에 닿는 단순 경로가 있는가 (전수 탐색)."""

    def extend(v, visited):
        for u in adj[v]:
            if u in visited or mate[v] == u:
                continue
            if mate[u] == -1:
                return True
            w = mate[u]
            if w not in visited and extend(w, visited | {u, w}):
                return True
        return False

    return extend(root, {root})


def test_search_from_arbitrary_matchings_matches_path_enumeration():
    """탐욕으로 시작한 매칭만이 아니라 임의의 (최대가 아닌) 매칭에서 시작해도, 뿌리마다 증가 경로의 존재를 정확히 판정하고 뒤집은 결과가 유효해야 한다."""
    rng = random.Random(14)
    checked = 0
    for _ in range(2500):
        n = rng.randint(5, 13)
        edges = random_graph(rng, n, rng.choice([0.15, 0.2, 0.3, 0.4]))
        shuffled = edges[:]
        rng.shuffle(shuffled)
        mate = [-1] * n
        for a, b in shuffled:
            if mate[a] == -1 and mate[b] == -1 and rng.random() < 0.8:
                mate[a], mate[b] = b, a
        adj = solution._adjacency(n, edges)
        for root in range(n):
            if mate[root] != -1:
                continue
            matcher = solution._Matcher(n, adj)
            matcher.mate = list(mate)
            found = matcher.augment_from(root)
            assert found == alternating_path_exists(adj, mate, root), (n, edges, mate, root)
            if found:
                assert_valid(n, edges, sum(1 for x in mate if x != -1) // 2 + 1, matcher.mate)
            else:
                assert matcher.mate == mate
            checked += 1
    assert checked > 3000


REGRESSION_SEARCHES = [
    # (정점 수, 간선, 시작 매칭, 뿌리): 꽃을 수축할 때 홀수였던 정점의 소속(base)과 두 방향의 표시가 모두 필요했던 입력
    (8, [(0, 2), (0, 4), (0, 6), (1, 5), (1, 7), (3, 4), (3, 7), (4, 7), (5, 6)], [4, 5, -1, 7, 0, 1, -1, 3], 6),
    (
        13,
        [(0, 8), (1, 2), (1, 3), (1, 5), (1, 8), (2, 5), (2, 8), (2, 12), (3, 7), (3, 12), (4, 8), (4, 11), (5, 6),
         (5, 7), (5, 9), (6, 7), (6, 11), (7, 12), (8, 11), (8, 12), (9, 11)],
        [-1, 8, 12, 7, -1, 6, 5, 3, 1, 11, -1, 9, 2],
        4,
    ),
]


@pytest.mark.parametrize("n, edges, mate, root", REGRESSION_SEARCHES)
def test_searches_that_need_every_part_of_the_contraction(n, edges, mate, root):
    adj = solution._adjacency(n, edges)
    matcher = solution._Matcher(n, adj)
    matcher.mate = list(mate)
    assert alternating_path_exists(adj, mate, root)
    assert matcher.augment_from(root)
    assert_valid(n, edges, sum(1 for x in mate if x != -1) // 2 + 1, matcher.mate)


def test_each_contraction_merges_two_blossoms():
    """한 번의 탐색에서 꽃 수축은 서로 다른 꽃 둘을 합치므로 n - 1 번을 넘지 않는다 (같은 꽃 안의 간선에서 다시 수축하면 O(n²) 으로 늘어난다)."""
    for n in (9, 15, 21):
        edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
        matcher = solution._Matcher(n, solution._adjacency(n, edges))
        for a in range(1, n - 1, 2):
            matcher.mate[a], matcher.mate[a + 1] = a + 1, a  # 0 만 짝이 없다
        calls = []
        original = matcher._lca
        matcher._lca = lambda a, b: (calls.append((a, b)), original(a, b))[1]
        assert matcher.search([0]) == -1  # 완전 그래프 K_n (n 홀수) 에 증가 경로는 없다
        assert 1 <= len(calls) <= n - 1


def test_certificate_proves_optimality_on_large_random_graphs():
    """큰 그래프는 전수 탐색이 불가능하므로 증명서(유효한 매칭 + 같은 크기를 주는 투테-버지의 U) 로 최적성을 확인한다."""
    rng = random.Random(5)
    for n, p in [(40, 0.03), (60, 0.04), (80, 0.025), (120, 0.02), (150, 0.015), (200, 0.012), (60, 0.5)]:
        edges = random_graph(rng, n, p)
        info = solution.gallai_edmonds(n, edges)
        assert_valid(n, edges, info["size"], info["mate"])
        assert info["size"] == tutte_berge_bound(n, edges, info["A"]), (n, p)


def odd_cactus(rng, cycles):
    """홀수 사이클들을 서로 한 정점씩 공유하게 이어 붙인 선인장 (꽃 속의 꽃) 에 잎과 무작위 간선을 더한다."""
    edges, count = [], 1
    for _ in range(cycles):
        length = rng.choice([3, 5, 7])
        anchor = rng.randrange(count)
        ring = [anchor] + list(range(count, count + length - 1))
        count += length - 1
        edges += [(ring[i], ring[(i + 1) % length]) for i in range(length)]
    return count, edges


def test_nested_blossoms_on_cacti_certified():
    rng = random.Random(6)
    for _ in range(120):
        n, edges = odd_cactus(rng, rng.randint(2, 12))
        for _ in range(rng.randint(0, 3)):
            a, b = rng.randrange(n), rng.randrange(n)
            edges.append((a, b))
        order = list(range(n))
        rng.shuffle(order)
        relabeled = [(order[a], order[b]) for a, b in edges]
        info = solution.gallai_edmonds(n, relabeled)
        assert_valid(n, relabeled, info["size"], info["mate"])
        assert info["size"] == tutte_berge_bound(n, relabeled, info["A"])


def test_small_cacti_match_brute_force():
    rng = random.Random(7)
    for _ in range(300):
        n, edges = odd_cactus(rng, rng.randint(1, 4))
        if n > 14:
            continue
        order = list(range(n))
        rng.shuffle(order)
        relabeled = [(order[a], order[b]) for a, b in edges]
        assert solution.max_matching(n, relabeled)[0] == brute_matching(n, relabeled)


def test_bipartite_graphs_agree_with_kuhn():
    rng = random.Random(8)

    def kuhn(left, right, es):
        adj = [[] for _ in range(left)]
        for a, b in es:
            adj[a].append(b)
        match_right = [-1] * right

        def try_(v, seen):
            for to in adj[v]:
                if to in seen:
                    continue
                seen.add(to)
                if match_right[to] == -1 or try_(match_right[to], seen):
                    match_right[to] = v
                    return True
            return False

        return sum(try_(v, set()) for v in range(left))

    for _ in range(300):
        left, right = rng.randint(1, 25), rng.randint(1, 25)
        es = [(a, b) for a in range(left) for b in range(right) if rng.random() < 0.12]
        edges = [(a, left + b) for a, b in es]
        assert solution.max_matching(left + right, edges)[0] == kuhn(left, right, es)


def test_search_is_cubic_but_fast_enough_for_a_few_hundred_vertices():
    rng = random.Random(9)
    n = 300
    edges = random_graph(rng, n, 0.02)
    start = time.perf_counter()
    info = solution.gallai_edmonds(n, edges)
    assert time.perf_counter() - start < 20
    assert info["size"] == tutte_berge_bound(n, edges, info["A"])


def test_main_prints_size_and_pairs(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 5\n0 1\n1 2\n2 0\n2 3\n3 4\n"))
    solution.main()
    lines = capsys.readouterr().out.split("\n")
    assert lines[0] == "2"
    pairs = [tuple(map(int, line.split())) for line in lines[1:] if line]
    assert len(pairs) == 2
    es = edge_set([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)])
    used = [v for p in pairs for v in p]
    assert len(set(used)) == 4 and all((min(p), max(p)) in es for p in pairs)
