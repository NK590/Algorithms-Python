"""단절점과 단절선(Articulation Points & Bridges) — 지우면 그래프가 쪼개지는 정점과 간선 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 무방향 그래프를 DFS 하면서 각 정점 v 에 방문 번호 order[v] 와 low[v](v 의 서브트리에서 간선 하나로 거슬러 올라갈 수 있는 가장 이른 방문 번호)를 구합니다.
- 간선 (p, v) 가 트리 간선이고 low[v] > order[p] 이면 v 의 서브트리가 p 위로 올라갈 길이 없으므로 (p, v) 는 단절선.
- low[v] ≥ order[p] 이면 v 의 서브트리가 p 를 거치지 않고는 위로 못 가므로 p 는 단절점 (루트는 DFS 트리의 자식이 둘 이상일 때만).
- 평행 간선(같은 두 정점을 잇는 간선이 여러 개)을 올바르게 다루려고 정점이 아니라 "간선 번호" 로 부모 간선을 건너뜁니다. 자기 루프는 무시됩니다.
- 반복문 DFS 라서 정점이 10^5 개인 사슬에서도 재귀 깊이 문제가 없습니다. 정점은 0 부터 n-1, 연결되지 않은 그래프도 됩니다.
- 직접 실행하면 `V E`, E 개의 간선 `A B` (1 부터)를 받아 단절선의 수와 단절선(각 간선은 작은 번호가 앞, 전체는 사전순)을 출력합니다.
"""
import sys


def find_cut_vertices_and_bridges(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    """(단절점 목록(오름차순), 단절선의 간선 번호 목록(오름차순)). 간선 번호는 edges 에서의 위치."""
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge_id, (a, b) in enumerate(edges):
        adjacency[a].append((b, edge_id))
        adjacency[b].append((a, edge_id))
    order = [-1] * n
    low = [0] * n
    parent_edge = [-1] * n
    next_index = [0] * n
    is_cut = [False] * n
    bridges: list[int] = []
    counter = 0
    for root in range(n):
        if order[root] != -1:
            continue
        order[root] = low[root] = counter
        counter += 1
        root_children = 0
        stack = [root]
        while stack:
            v = stack[-1]
            if next_index[v] < len(adjacency[v]):
                w, edge_id = adjacency[v][next_index[v]]
                next_index[v] += 1
                if edge_id == parent_edge[v]:
                    continue  # 올라온 그 간선으로는 되돌아가지 않는다 (같은 간선 번호만 건너뛰므로 평행 간선은 역방향으로 인정)
                if order[w] == -1:  # 트리 간선
                    parent_edge[w] = edge_id
                    order[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                else:  # 되돌아가는 간선(역방향 간선)
                    low[v] = min(low[v], order[w])
            else:
                stack.pop()
                if stack:
                    p = stack[-1]
                    low[p] = min(low[p], low[v])
                    if low[v] > order[p]:
                        bridges.append(parent_edge[v])
                    if p == root:
                        root_children += 1
                    elif low[v] >= order[p]:
                        is_cut[p] = True
        if root_children >= 2:
            is_cut[root] = True
    return [v for v in range(n) if is_cut[v]], sorted(bridges)


def bridge_pairs(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """단절선을 (작은 정점, 큰 정점) 쌍의 사전순 목록으로."""
    _, bridge_ids = find_cut_vertices_and_bridges(n, edges)
    return sorted((min(edges[i]), max(edges[i])) for i in bridge_ids)


def two_edge_connected_components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """단절선을 모두 지운 뒤의 연결 요소 번호(0 부터, 작은 정점 번호 순). 같은 요소에 속한 두 정점은 서로 다른 두 경로로 연결돼 있다."""
    _, bridge_ids = find_cut_vertices_and_bridges(n, edges)
    removed = set(bridge_ids)
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for edge_id, (a, b) in enumerate(edges):
        if edge_id not in removed:
            adjacency[a].append(b)
            adjacency[b].append(a)
    component = [-1] * n
    count = 0
    for start in range(n):
        if component[start] != -1:
            continue
        component[start] = count
        stack = [start]
        while stack:
            v = stack.pop()
            for w in adjacency[v]:
                if component[w] == -1:
                    component[w] = count
                    stack.append(w)
        count += 1
    return component


def bridge_tree(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[tuple[int, int]]]:
    """(정점별 2-edge-connected 요소 번호, 요소들을 잇는 단절선들). 요소를 한 정점으로 줄이면 숲이 된다."""
    component = two_edge_connected_components(n, edges)
    _, bridge_ids = find_cut_vertices_and_bridges(n, edges)
    links = []
    for i in bridge_ids:
        a, b = edges[i]
        links.append((min(component[a], component[b]), max(component[a], component[b])))
    return component, sorted(links)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    v, e = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]) - 1) for i in range(e)]
    pairs = bridge_pairs(v, edges)
    out = [str(len(pairs))]
    out.extend(f"{a + 1} {b + 1}" for a, b in pairs)
    print("\n".join(out))


if __name__ == "__main__":
    main()
