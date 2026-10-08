"""강한 연결 요소(SCC, Strongly Connected Components) — 방향 그래프에서 서로 오갈 수 있는 정점들의 묶음 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 두 정점 u, v 가 같은 SCC ⟺ u 에서 v 로도, v 에서 u 로도 갈 수 있다. SCC 를 한 정점으로 줄이면(축약) 사이클이 없는 DAG 가 됩니다.
- tarjan_scc: DFS 한 번. 각 정점의 low-link(자기 서브트리에서 스택에 있는 정점으로 거슬러 올라갈 수 있는 가장 이른 방문 번호)가
  자기 방문 번호와 같으면 그 정점이 SCC 의 루트. 결과는 위상 정렬의 거꾸로(도착하는 쪽이 먼저) 입니다.
- kosaraju_scc: DFS 두 번. 원래 그래프에서 끝난 순서를 기록하고, 뒤집은 그래프를 그 역순으로 DFS. 결과는 위상 정렬 순서(출발하는 쪽이 먼저).
- 둘 다 반복문으로 구현해 정점이 10^5 개인 사슬에서도 재귀 깊이 문제가 없습니다. 정점은 0 부터 n-1, 간선은 (u, v) = u -> v.
- 직접 실행하면 `V E`, E 개의 간선 `A B` (1 부터)를 받아 SCC 의 수와, 각 SCC 의 정점(오름차순)을 한 줄에 하나씩 -1 로 끝내서 출력합니다.
  SCC 들은 가장 작은 정점 번호 순으로 출력합니다.
"""
import sys


def tarjan_scc(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """SCC 목록. 각 SCC 는 정점의 리스트이고, SCC 들은 위상 정렬의 역순(싱크 쪽이 먼저)으로 나온다."""
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
    order = [-1] * n  # 방문 번호
    low = [0] * n
    on_stack = [False] * n
    stack: list[int] = []
    components: list[list[int]] = []
    counter = 0
    for start in range(n):
        if order[start] != -1:
            continue
        order[start] = low[start] = counter
        counter += 1
        stack.append(start)
        on_stack[start] = True
        call_stack = [(start, 0)]  # (정점, 다음에 볼 이웃의 인덱스)
        while call_stack:
            v, i = call_stack.pop()
            if i < len(adjacency[v]):
                call_stack.append((v, i + 1))
                w = adjacency[v][i]
                if order[w] == -1:  # 트리 간선: 자식으로 내려간다
                    order[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack[w] = True
                    call_stack.append((w, 0))
                elif on_stack[w]:  # 스택에 있는 정점으로 가는 간선: 거슬러 올라갈 수 있다
                    low[v] = min(low[v], order[w])
            else:  # v 의 이웃을 모두 봤다
                if low[v] == order[v]:  # v 가 SCC 의 루트: 스택에서 v 까지 꺼낸다
                    component = []
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        component.append(w)
                        if w == v:
                            break
                    components.append(component)
                if call_stack:  # 부모의 low 에 반영
                    parent = call_stack[-1][0]
                    low[parent] = min(low[parent], low[v])
    return components


def kosaraju_scc(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """SCC 목록. SCC 들은 위상 정렬 순서(소스 쪽이 먼저)로 나온다."""
    forward: list[list[int]] = [[] for _ in range(n)]
    backward: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        forward[a].append(b)
        backward[b].append(a)
    visited = [False] * n
    finish_order: list[int] = []
    for start in range(n):  # 1 단계: 원래 그래프에서 DFS 가 끝난 순서를 기록
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, 0)]
        while stack:
            v, i = stack.pop()
            if i < len(forward[v]):
                stack.append((v, i + 1))
                w = forward[v][i]
                if not visited[w]:
                    visited[w] = True
                    stack.append((w, 0))
            else:
                finish_order.append(v)
    assigned = [False] * n
    components: list[list[int]] = []
    for start in reversed(finish_order):  # 2 단계: 뒤집은 그래프를 끝난 순서의 역순으로 DFS
        if assigned[start]:
            continue
        assigned[start] = True
        component = [start]
        stack = [start]
        while stack:
            v = stack.pop()
            for w in backward[v]:
                if not assigned[w]:
                    assigned[w] = True
                    component.append(w)
                    stack.append(w)
        components.append(component)
    return components


def component_ids(n: int, components: list[list[int]]) -> list[int]:
    """각 정점이 속한 SCC 의 번호."""
    ids = [-1] * n
    for index, component in enumerate(components):
        for v in component:
            ids[v] = index
    return ids


def condensation(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[set[int]]]:
    """(정점별 SCC 번호, 축약 그래프의 인접 집합). SCC 번호는 위상 정렬 순서(소스가 먼저)이므로 간선은 항상 작은 번호에서 큰 번호로 간다."""
    components = kosaraju_scc(n, edges)
    ids = component_ids(n, components)
    dag: list[set[int]] = [set() for _ in components]
    for a, b in edges:
        if ids[a] != ids[b]:
            dag[ids[a]].add(ids[b])
    return ids, dag


def min_edges_to_make_strongly_connected(n: int, edges: list[tuple[int, int]]) -> int:
    """간선을 최소 몇 개 더하면 전체가 하나의 SCC 가 되는가. 이미 하나뿐이면 0, 아니면 max(진입 차수 0 인 SCC 수, 진출 차수 0 인 SCC 수)."""
    if n == 0:
        return 0
    ids, dag = condensation(n, edges)
    count = len(dag)
    if count == 1:
        return 0
    has_in = [False] * count
    for targets in dag:
        for t in targets:
            has_in[t] = True
    sources = sum(1 for c in range(count) if not has_in[c])
    sinks = sum(1 for c in range(count) if not dag[c])
    return max(sources, sinks)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    v, e = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]) - 1) for i in range(e)]
    components = sorted(sorted(c) for c in tarjan_scc(v, edges))
    out = [str(len(components))]
    for component in components:
        out.append(" ".join(str(x + 1) for x in component) + " -1")
    print("\n".join(out))


if __name__ == "__main__":
    main()
