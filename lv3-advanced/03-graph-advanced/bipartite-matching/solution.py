"""이분 매칭(Bipartite Matching) — 이분 그래프에서 정점을 겹치지 않게 짝지을 수 있는 간선의 최대 개수 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 왼쪽 정점 0..left_n-1, 오른쪽 정점 0..right_n-1, adjacency[u] = u 와 이어진 오른쪽 정점들.
- kuhn_matching: 왼쪽 정점마다 "증가 경로"(짝이 없는 정점에서 시작해 매칭 아닌 간선, 매칭인 간선을 번갈아 밟아 짝 없는 오른쪽 정점에 닿는 경로)를
  DFS 로 찾아 매칭을 하나씩 키운다. O(V·E).
- hopcroft_karp: BFS 로 최단 증가 경로의 길이를 정해 같은 길이의 증가 경로를 한꺼번에 찾는다. O(E√V).
- 두 구현 모두 반복문 DFS 입니다. 최대 매칭을 알면 쾨니그의 정리(최대 매칭 = 최소 정점 덮개)로 최소 정점 덮개와 최대 독립 집합,
  DAG 의 최소 경로 덮개(n - 최대 매칭)도 구할 수 있습니다.
- 직접 실행하면 `N M` 과 N 개의 줄(각 줄은 `k` 와 k 개의 오른쪽 정점 번호, 1 부터)을 받아 최대 매칭의 크기를 출력합니다.
"""
import sys
from collections import deque

INF = float("inf")


def kuhn_matching(left_n: int, right_n: int, adjacency: list[list[int]]) -> tuple[int, list[int], list[int]]:
    """(최대 매칭 크기, match_left, match_right). match_left[u] = u 와 짝지어진 오른쪽 정점(없으면 -1)."""
    match_left = [-1] * left_n
    match_right = [-1] * right_n
    size = 0
    visited_by = [-1] * right_n  # 오른쪽 정점을 마지막으로 시도한 탐색(root)의 번호: 매번 배열을 새로 만들지 않는다
    for root in range(left_n):
        stack = [root]  # 지금 탐색 중인 경로의 왼쪽 정점들
        chosen: list[int] = []  # stack[i] 가 선택한 오른쪽 정점 (len(chosen) == len(stack) - 1 이 평소 상태)
        pointer = {root: 0}
        found = False
        while stack:
            u = stack[-1]
            if pointer[u] == len(adjacency[u]):  # u 로는 더 길을 못 찾는다: 한 칸 물러난다
                stack.pop()
                if chosen:
                    chosen.pop()
                continue
            v = adjacency[u][pointer[u]]
            pointer[u] += 1
            if visited_by[v] == root:
                continue
            visited_by[v] = root
            chosen.append(v)
            if match_right[v] == -1:  # 짝 없는 오른쪽 정점에 닿았다: 경로를 따라 매칭을 뒤집는다
                for a, b in zip(stack, chosen):
                    match_left[a] = b
                    match_right[b] = a
                found = True
                break
            nxt = match_right[v]  # v 의 현재 짝에게 다른 자리를 찾아 주도록 한 칸 더 내려간다
            pointer[nxt] = 0
            stack.append(nxt)
        if found:
            size += 1
    return size, match_left, match_right


def hopcroft_karp(left_n: int, right_n: int, adjacency: list[list[int]]) -> tuple[int, list[int], list[int]]:
    """(최대 매칭 크기, match_left, match_right). 한 단계(phase)마다 최단 증가 경로들을 동시에 찾는다."""
    match_left = [-1] * left_n
    match_right = [-1] * right_n
    size = 0
    while True:
        # BFS: 짝 없는 왼쪽 정점을 0 층으로 해서 층(거리)을 매긴다
        dist = [INF] * left_n
        queue = deque()
        for u in range(left_n):
            if match_left[u] == -1:
                dist[u] = 0
                queue.append(u)
        reachable_free = False
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                w = match_right[v]
                if w == -1:
                    reachable_free = True
                elif dist[w] == INF:
                    dist[w] = dist[u] + 1
                    queue.append(w)
        if not reachable_free:
            return size, match_left, match_right
        # DFS: 층이 정확히 1 씩 늘어나는 간선만 따라 증가 경로를 찾는다 (정점마다 포인터로 막다른 길을 건너뛴다)
        pointer = [0] * left_n
        for root in range(left_n):
            if match_left[root] != -1:
                continue
            stack = [root]
            chosen: list[int] = []
            found = False
            while stack:
                u = stack[-1]
                if pointer[u] == len(adjacency[u]):  # u 로는 더 길이 없다 (포인터가 남아 있지 않아 다시 와도 바로 물러난다)
                    stack.pop()
                    if chosen:
                        chosen.pop()
                    continue
                v = adjacency[u][pointer[u]]
                pointer[u] += 1
                w = match_right[v]
                if w == -1:
                    chosen.append(v)
                    for a, b in zip(stack, chosen):
                        match_left[a] = b
                        match_right[b] = a
                    found = True
                    break
                if dist[w] == dist[u] + 1:
                    chosen.append(v)
                    stack.append(w)
            if found:
                size += 1


def minimum_vertex_cover(left_n: int, right_n: int, adjacency: list[list[int]]) -> tuple[list[int], list[int]]:
    """쾨니그의 정리: (왼쪽 덮개 정점들, 오른쪽 덮개 정점들). 크기의 합 = 최대 매칭.

    짝 없는 왼쪽 정점에서 시작해 '왼쪽 -> 오른쪽은 아무 간선, 오른쪽 -> 왼쪽은 매칭 간선' 으로 갈 수 있는 정점의 집합 Z 를 구하면
    덮개 = (왼쪽 중 Z 에 없는 것) ∪ (오른쪽 중 Z 에 있는 것)."""
    _, match_left, match_right = hopcroft_karp(left_n, right_n, adjacency)
    in_z_left = [False] * left_n
    in_z_right = [False] * right_n
    stack = [u for u in range(left_n) if match_left[u] == -1]
    for u in stack:
        in_z_left[u] = True
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if not in_z_right[v]:
                in_z_right[v] = True
                w = match_right[v]
                if w != -1 and not in_z_left[w]:
                    in_z_left[w] = True
                    stack.append(w)
    return [u for u in range(left_n) if not in_z_left[u]], [v for v in range(right_n) if in_z_right[v]]


def maximum_independent_set(left_n: int, right_n: int, adjacency: list[list[int]]) -> tuple[list[int], list[int]]:
    """최소 정점 덮개의 여집합 = 최대 독립 집합. (왼쪽 정점들, 오른쪽 정점들)."""
    left_cover, right_cover = minimum_vertex_cover(left_n, right_n, adjacency)
    left_set, right_set = set(left_cover), set(right_cover)
    return [u for u in range(left_n) if u not in left_set], [v for v in range(right_n) if v not in right_set]


def min_path_cover(n: int, edges: list[tuple[int, int]]) -> int:
    """DAG 의 정점 서로소 경로 덮개의 최소 경로 수 = n - (u -> v 를 '왼쪽 u, 오른쪽 v' 로 둔 이분 그래프의 최대 매칭)."""
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
    return n - hopcroft_karp(n, n, adjacency)[0]


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    adjacency = []
    pos = 2
    for _ in range(n):
        k = int(data[pos])
        adjacency.append([int(x) - 1 for x in data[pos + 1 : pos + 1 + k]])
        pos += 1 + k
    print(hopcroft_karp(n, m, adjacency)[0])


if __name__ == "__main__":
    main()
