### DFS (Depth-First Search, 깊이 우선 탐색)

# 주어진 트리에서, 루트에서부터 제일 말단 노드까지 탐색 후, 더 이상 자식 노드가 없을 시
# 다른 자식 노드가 있을 떄까지 돌아와서 다시 다른 노드를 따라 말단까지 반복해서 탐색하는 방식
# 트리가 아닌 사이클이 존재하는 그래프에서도 알고리즘을 개량하여 사용이 가능함
# 단순 검색보단 모든 데이터를 순회하는 경우에 유리하며, 백트래킹 등에 자주 응용됨

### 예시 코드 1
# 재귀를 이용한 구현

def DFS(graph: dict, root: int, visited: list = []):
    # 방문한 노드들을 저장하는 리스트. 먼저 시작점인 root를 넣고 시작
    visited.append(root)
    
    # root의 자식 노드들에 대해, 만약 visited에 없다면 재귀적으로 DFS를 실행
    for node in graph[root]:
        if node not in visited:
            DFS(graph, node, visited)
    
    return visited

### 예시 코드 2
# 스택을 이용한 구현

def DFS_2(graph: dict, root: int):
    # 방문한 노드들을 저장하는 리스트
    visited = []
    stack = [root]
    
    # 스택에 남은 노드가 없을 떄까지 반복
    while stack:
        # 현재 선택한 노드
        node = stack.pop()
        # 현재 노드를 방문한 적이 없으면 visited에 추가하고, 그 자식 노드들을 스택에 넣음
        if node not in visited:
            visited.append(node)
            stack.extend(graph[node])

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

print(DFS(graph, 'A'))
print(DFS_2(graph, 'A'))