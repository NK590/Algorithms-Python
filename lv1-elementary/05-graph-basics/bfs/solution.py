### BFS (Breadth-First Search, 너비 우선 탐색)

# 주어진 트리에서, 루트로부터 같은 레벨만큼 떨어져 있는 노드들을 순차적으로 탐색하는 알고리즘
# DFS에 비해 사이클이 있는 그래프의 경우도 안정적으로 탐색이 가능하고, 순차적으로 탐색하는 특성 덕분에
# 시작점과 끝 점 사이의 최단 경로를 찾는 데 응용할 수 있음

### 예시 코드
# 큐를 이용한 구현. DFS 스택 구현에서 스택을 큐로만 바꿔주면 됨

# 파이썬에서 큐를 구현할 때는 일반적으로 collections 라이브러리의 deque 함수를 이용
from collections import deque

def BFS(graph: dict, root: int):
    visited = []
    queue = deque([root])
    
    # DFS 스택 구현과의 차이점은, DFS 스택 구현은 스택에 push한 마지막 노드를 pop하여 끝까지 탐색하지만,
    # BFS는 제일 먼저 push한 노드를 pop하므로 같은 레벨의 노드들을 순차적으로 탐색한다.
    while queue != deque([]):
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])

    return visited

### 예제

graph = {'A':['B','C'],
        'B':['A','D','E'],
        'C':['A','G','H'],
        'D':['B'],
        'E':['B','F'],
        'F':['E'],
        'G':['C'],
        'H':['C']}

print(BFS(graph, 'A'))