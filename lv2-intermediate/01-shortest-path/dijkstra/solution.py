### Dijkstra's Algorithm (다익스트라 알고리즘)

# 정점 V개와 그 정점들을 잇는 가중치가 있는 변 E개로 이루어진 가중 그래프가 주어졌을 떄,
# 그 그래프 내에서 특정 정점에서 다른 정점까지의 최단경로를 찾는 알고리즘
# 시작 정점에서부터 인접한 정점을 하나씩 확인하여 해당 정점까지의 거리를 갱신해 나가며
# 경로를 찾는 알고리즘으로, 벨만-포드 알고리즘의 특수한 버전이라고 볼 수 있음
# 음의 가중치 간선이 있을 때는 사용이 불가능하지만, 플로이드-워셜이나 벨만-포드 알고리즘에 비해
# 매우 빠른 알고리즘이라 자주 사용됨
# 구현 시 우선순위 큐를 사용하고, 시간 복잡도는 일반적으로 O((V+E)logV)임

### 예시 코드

# 우선순위 큐를 사용하기 위한 heapq 함수 호출
import heapq
import sys

INF = sys.maxsize

def Dijkstra(graph: dict, start: str):
    # 시작점으로부터 거리를 저장할 딕셔너리를 생성 후 초기값을 무한대로 설정
    dist = {node: INF for node in graph}
    dist[start] = 0
    
    # 모든 정점을 거리가 작은 순으로 저장할 우선순위 큐 생성
    queue = []
    heapq.heappush(queue, [dist[start], start])
    
    # 우선순위 큐에 정점이 없어질 때까지 반복
    while queue:
        # 우선순위 큐에서 가장 가까운 정점을 꺼내, 인근 간선의 가중치 확인 후 거리 수정
        cur_dist, cur_node = heapq.heappop(queue)
        
        # 이미 구한 거리 배열보다 현재까지 거리가 크다면 더 이상 고려할 필요 없이 되돌아감
        if dist[cur_node] < cur_dist:
            continue
        
        for edge, weight in graph[cur_node].items():
            # 현재 정점까지 거리 + 다음 인접한 정점까지 거리
            distance = cur_dist + weight
            
            # 인접한 정점까지 거리가 시작점에서 바로 갔을 때보다 현재 정점을 거쳤을 때 더 가깝다면
            # 그 값으로 최단거리 갱신
            if distance < dist[edge]:
                dist[edge] = distance
                heapq.heappush(queue, [distance, edge])
    
    return dist

### 예제

graph = {
    'A': {'B': 8, 'C': 1, 'D': 2},
    'B': {},
    'C': {'B': 5, 'D': 2},
    'D': {'E': 3, 'F': 5},
    'E': {'F': 1},
    'F': {'A': 5}
}

print(Dijkstra(graph, 'A'))