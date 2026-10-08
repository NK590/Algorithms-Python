### Bellman-Ford Algorithm (벨만-포드 알고리즘)

# 정점 V개와 그 정점들을 잇는 가중치가 있는 변 E개로 이루어진 가중 그래프가 주어졌을 떄,
# 그 그래프 내에서 특정 정점에서 다른 정점까지의 최단경로를 찾는 알고리즘
# 변이 음의 가중치를 가지고 있을 때도 사용이 가능하고, 응용해서 음의 사이클을 찾아내는 데 응용이 가능
# 인접 간선을 검사하고 가중치 합을 갱신하는 과정을 제한하여, 특정 회수 이상 반복 시에도 루프가 발생하면
# 음의 사이클이 존재한다고 판정
# 모든 정점에 대해 그 정점에서 나오는 간선을 전부 검사하는 이중 반복문으로 구현되고, 시간복잡도는 O(VE)

### 예시 코드

import sys

INF = sys.maxsize

def Bellman_Ford(graph: dict, start: int):
    # start 점에서 시작하는 거리 딕셔너리. 초기값을 INF로 설정
    distance = {}
    for node in graph:
        distance[node] = INF
    
    distance[start] = 0
    
    # V-1회만큼 갱신 반복
    for _ in range(len(graph) - 1):
        for node in graph:
            # 각 정점마다 모든 인접 정점들을 탐색
            for neighbor in graph[node]:
                # 기존 인접 정점까지 거리 > 기존 현재 정점까지 거리 + 현재 정점부터 인접 정점까지 거리
                # 일 때 거리 갱신
                if distance[neighbor] > distance[node] + graph[node][neighbor]:
                    distance[neighbor] = distance[node] + graph[node][neighbor]
    
    # V-1회만큼 갱신 반복 후에도 갱신할 거리 값이 존재한다면 음수 사이클 존재 -> -1 리턴 후 종료
    for node in graph:
        for neighbor in graph[node]:
            if distance[neighbor] > distance[node] + graph[node][neighbor]:
                return -1
    
    return distance

### 예제

# 음의 사이클이 없는 경우
graph = {
    'A': {'B': -1, 'C':  4},
    'B': {'C':  3, 'D':  2, 'E':  2},
    'C': {},
    'D': {'B':  1, 'C':  5},
    'E': {'D': -3}
}

print(Bellman_Ford(graph, start='A'))

# 음의 사이클이 있는 경우
graph2 = {
    'A': {'B': -1, 'C':  4},
    'B': {'C':  3, 'D':  2, 'E':  2},
    'C': {'A': -5},
    'D': {'B':  1, 'C':  5},
    'E': {'D': -3}
}

print(Bellman_Ford(graph2, start='A'))