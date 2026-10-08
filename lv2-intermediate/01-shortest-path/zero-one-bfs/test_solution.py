"""solution.py 검증: 힙을 쓰는 다익스트라(독립 구현)와 랜덤 비교"""
import heapq
import io
import random
from collections import deque

from tools.loader import load_solution

solution = load_solution(__file__)
INF = solution.INF


def dijkstra(graph, start):
    dist = [INF] * len(graph)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist


def random_graph(rng):
    n = rng.randint(1, 9)
    graph = [[] for _ in range(n)]
    for _ in range(rng.randint(0, 25)):
        graph[rng.randrange(n)].append((rng.randrange(n), rng.choice([0, 1])))
    return graph


def test_matches_dijkstra_on_random_graphs():
    rng = random.Random(0)
    for _ in range(1500):
        graph = random_graph(rng)
        start = rng.randrange(len(graph))
        assert solution.zero_one_bfs(graph, start) == dijkstra(graph, start), (graph, start)


class CountingDeque(deque):
    pops = 0

    def popleft(self):
        CountingDeque.pops += 1
        return super().popleft()


def test_each_vertex_is_taken_out_at_most_twice(monkeypatch):
    # 0 간선은 앞, 1 간선은 뒤에 넣는 규칙이 지켜지면 한 정점의 거리는 많아야 두 번(d+1 → d) 정해진다.
    # 규칙이 깨져도 답은 맞게 나오지만 이 상한(O(V+E))은 깨진다.
    monkeypatch.setattr(solution, "deque", CountingDeque)
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(2, 30)
        graph = [[] for _ in range(n)]
        for _ in range(rng.randint(n, 6 * n)):
            graph[rng.randrange(n)].append((rng.randrange(n), rng.choice([0, 1])))
        CountingDeque.pops = 0
        solution.zero_one_bfs(graph, 0)
        assert CountingDeque.pops <= 2 * n, (graph, CountingDeque.pops)


def test_grid_version_takes_each_cell_out_at_most_twice(monkeypatch):
    # 격자가 클수록 규칙이 깨졌을 때의 낭비가 눈에 띈다 (평범한 큐로 바꾸면 칸마다 3번 넘게 처리하는 경우가 생긴다)
    monkeypatch.setattr(solution, "deque", CountingDeque)
    rng = random.Random(6)
    for _ in range(20):
        size = 30
        grid = ["".join(rng.choice("01") for _ in range(size)) for _ in range(size)]
        CountingDeque.pops = 0
        solution.grid_min_walls(grid)
        assert CountingDeque.pops <= 2 * size * size, CountingDeque.pops


def test_zero_weight_cycle_and_unreachable():
    graph = [[(1, 0)], [(0, 0), (2, 1)], [], [(0, 0)]]
    assert solution.zero_one_bfs(graph, 0) == [0, 0, 1, INF]
    assert solution.zero_one_bfs([[]], 0) == [0]


def test_a_vertex_improved_after_being_queued_is_handled():
    # 0 → 1 (1), 0 → 2 (0), 2 → 1 (0): 1 은 먼저 거리 1 로 큐에 들어가지만 0 으로 줄어든다
    graph = [[(1, 1), (2, 0)], [(3, 1)], [(1, 0)], []]
    assert solution.zero_one_bfs(graph, 0) == [0, 0, 0, 1]


def grid_by_dijkstra(grid):
    rows, cols = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    heap = [(0, 0, 0)]
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > dist[(r, c)]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nd = d + int(grid[nr][nc])
                if nd < dist.get((nr, nc), INF):
                    dist[(nr, nc)] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return dist[(rows - 1, cols - 1)]


def test_grid_min_walls_matches_dijkstra():
    rng = random.Random(1)
    for _ in range(500):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        grid = ["".join(rng.choice("0011") for _ in range(cols)) for _ in range(rows)]
        grid[0] = "0" + grid[0][1:]
        grid[-1] = grid[-1][:-1] + "0"
        assert solution.grid_min_walls(grid) == grid_by_dijkstra(grid), grid
    assert solution.grid_min_walls(["0"]) == 0


def test_grid_examples():
    assert solution.grid_min_walls(["00000", "00000"]) == 0
    assert solution.grid_min_walls(["0111", "1111", "1110"]) == 4  # 모든 길에 벽이 4 개 이상


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 3\n011\n111\n110\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
