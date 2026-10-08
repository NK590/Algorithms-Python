### Topological Sort (위상 정렬)

# 주어진 비순환 유향 그래프에서 각 정점을 특정 방향으로 맞춰서 정렬하는 방법
# 정의에서 알 수 있듯이 그래프 내 사이클이 존재하거나, 무향 그래프일 경우 위상 정렬이 불가능함
# 역으로, 이 성질을 이용하여 주어진 그래프 내 사이클이 존재하는지 위상 정렬로 찾아낼 수 있음

# 특정 데이터와 그 데이터 세그먼트들 사이의 '방향'이 주어졌을 때, 
# 그 데이터들을 주어진 '방향'에 맞춰서 한 줄로 '정렬'하는 경우에 사용이 됨
# 진입 차수(Indegree), 진출 차수(Outdegree)를 이용해 큐를 이용하는 BFS 구현법과
# 스택을 이용한 DFS 구현법 등이 있음

### 예시 코드 1
# BFS 구현

# 진입 차수(Indegree) : 정점에 들어오는 간선의 수
# 진출 차수(Outdegree) : 정점에서 나가는 간선의 수

from collections import deque

def Topological_Sort_1 (graph: dict):
    # 각 노드의 진입 차수의 개수 리스트
    indegree = [0 for _ in range(len(graph) + 1)]
    # 방문하는 노드 저장용
    visited = deque([])
    # 알고리즘 수행 결과 저장용
    result = []
    
    # 모든 노드의 진입 차수 갱신
    for node in graph:
        for next_node in graph[node]:
            indegree[next_node] += 1
    
    # 먼저 진입 차수가 0인 노드를 덱에 삽입
    for node in graph:
        if indegree[node] == 0:
            visited.append(node)
    
    # 덱이 빌 때까지 반복
    while visited:
        cur_node = visited.popleft()
        result.append(cur_node)
        # 해당 원소와 연결된 노드들의 진입차수 1 빼기
        for next_node in graph[cur_node]:
            indegree[next_node] -= 1
            # 새롭게 진입차수가 0이 되는 노드를 덱에 삽입
            if indegree[next_node] == 0:
                visited.append(next_node)
    
    return result

### 예시 코드 2
# DFS 구현
# BFS 구현에서 큐 대신 스택을 사용하면 손쉽게 구현 가능함
# 출력 결과가 위의 BFS 구현과 다소 달라지지만, 위상 정렬은 여러 가지 방법이 있기 때문에 둘 다 정답

def Topological_Sort_2 (graph: dict):
    indegree = [0 for _ in range(len(graph) + 1)]
    visited = []
    result = []
    
    for node in graph:
        for next_node in graph[node]:
            indegree[next_node] += 1
    
    for node in graph:
        if indegree[node] == 0:
            visited.append(node)
    
    while visited:
        cur_node = visited.pop()
        result.append(cur_node)
        for next_node in graph[cur_node]:
            indegree[next_node] -= 1
            if indegree[next_node] == 0:
                visited.append(next_node)
    
    return result

### 예시 코드 3
# 주어진 그래프에 사이클이 있는지 판별하는 방법 -> 모든 원소를 방문하기 전에 큐가 빌 경우 사이클이 존재

def Topological_Sort_3 (graph: dict):
    indegree = [0 for _ in range(len(graph) + 1)]
    visited = deque([])
    result = []
    
    for node in graph:
        for next_node in graph[node]:
            indegree[next_node] += 1
            
    for node in graph:
        if indegree[node] == 0:
            visited.append(node)
    
    while visited:
        cur_node = visited.popleft()
        result.append(cur_node)
        for next_node in graph[cur_node]:
            indegree[next_node] -= 1
            if indegree[next_node] == 0:
                visited.append(next_node)
    
    # result에 넣은 노드 개수가 그래프의 노드 개수보다 작을 시 사이클 존재
    if len(graph) == len(result):
        return True
    else:
        return False