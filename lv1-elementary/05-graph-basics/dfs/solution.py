"""DFS (깊이 우선 탐색) — 갈 수 있는 데까지 깊이 들어갔다가, 막히면 돌아와 다른 길을 가는 탐색

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 그래프는 인접 리스트 `adj[u] = [이웃, ...]` 이고 정점은 0 ~ n-1 번입니다. 이웃은 리스트에 적힌 순서대로 방문합니다.
- dfs_recursive 와 dfs_iterative 는 같은 방문 순서를 냅니다. 재귀는 깊이 제한(기본 1000)에 걸리므로 깊은 그래프에는 반복문 버전을 씁니다.
- 직접 실행하면 `V E S` 와 E 개의 `u v` 를 받아, 정점 S 에서 시작한 DFS 방문 순서를 출력합니다. (번호는 1부터, 작은 이웃부터)
"""
import sys


def dfs_recursive(adj: list, start: int) -> list:
    """start 에서 갈 수 있는 정점을 DFS 방문 순서(전위 순서)대로 반환한다."""
    visited = [False] * len(adj)
    order = []

    def visit(u: int) -> None:
        visited[u] = True
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visit(v)

    visit(start)
    return order


def dfs_iterative(adj: list, start: int) -> list:
    """직접 만든 스택으로 같은 순서의 DFS. 재귀 깊이 제한이 없다."""
    visited = [False] * len(adj)
    order = []
    stack = [start]
    while stack:
        u = stack.pop()
        if visited[u]:  # 스택에 같은 정점이 여러 번 들어갈 수 있으니 꺼낼 때 확인한다
            continue
        visited[u] = True
        order.append(u)
        for v in reversed(adj[u]):  # 스택은 나중에 넣은 것이 먼저 나오므로, 첫 이웃이 마지막에 들어가게 뒤집어 넣는다
            if not visited[v]:
                stack.append(v)
    return order


def dfs_times(adj: list) -> tuple:
    """모든 정점을 DFS 로 훑으며 (발견 시각, 종료 시각) 리스트를 반환한다. 시각은 발견·종료마다 1 씩 늘어난다.

    v 가 u 의 후손이면 discovered[u] < discovered[v] < finished[v] < finished[u] 이다.
    """
    n = len(adj)
    discovered = [-1] * n
    finished = [-1] * n
    time = 0
    for root in range(n):
        if discovered[root] != -1:
            continue
        discovered[root] = time
        time += 1
        stack = [(root, 0)]  # (정점, 다음에 볼 이웃의 인덱스)
        while stack:
            u, i = stack.pop()
            if i < len(adj[u]):
                stack.append((u, i + 1))
                v = adj[u][i]
                if discovered[v] == -1:
                    discovered[v] = time
                    time += 1
                    stack.append((v, 0))
            else:
                finished[u] = time
                time += 1
    return discovered, finished


def reachable(adj: list, start: int) -> set:
    """start 에서 갈 수 있는 정점의 집합."""
    return set(dfs_iterative(adj, start))


def has_path(adj: list, source: int, target: int) -> bool:
    return target in reachable(adj, source)


def main() -> None:
    input = sys.stdin.readline
    n, m, start = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u - 1].append(v - 1)
        adj[v - 1].append(u - 1)
    for neighbors in adj:
        neighbors.sort()
    print(*(u + 1 for u in dfs_iterative(adj, start - 1)))


if __name__ == "__main__":
    main()
