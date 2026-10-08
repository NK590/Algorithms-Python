### Floyd-Warshall Algorithm (플로이드-워셜 알고리즘)

# 정점 V개와 그 정점들을 잇는 가중치가 있는 변 E개로 이루어진 가중 그래프가 주어졌을 떄,
# 그 그래프 내에서 최단경로를 찾는 알고리즘
# 한 번의 계산으로 모든 정점 쌍 사이의 최단 거리를 구해내고, 변이 음의 가중치일 때도 계산 가능
# 3중 반복문 DP로 구현하며, 시간복잡도는 O(V^3)로 다소 좋지 않은 편이라 상황에 따라 다른 알고리즘 도입이 필요

### 예시 코드

import sys

INF = sys.maxsize

def Floyd_Warshall(graph: list):
    n = len(graph)
    # 최단 경로를 담는 DP 배열, 초기치를 절대 나올 수 없는 최대값(INF)으로 설정
    dp = [[INF for _ in range(n)] for __ in range(n)]
    
    # DP 배열에 그래프 간선치를 대입
    for i in range(n):
        for j in range(n):
            dp[i][j] = graph[i][j]
    
    for k in range(n): # 거쳐가는 점
        for i in range(n): # 시작점
            for j in range(n): # 끝점
                # 만약 i->j로 가는 비용보다 i->k->j로 가는 비용이 적으면 dp[i][j]를 그 값으로 갱신
                if dp[i][j] > dp[i][k] + dp[k][j]:
                    dp[i][j] = dp[i][k] + dp[k][j]
    
    return dp

### 예제

graph = [
    [0, 10, 2, 4, 5], 
    [4, 0, 1, -3, 8],
    [1, 2, 0, 2, 1],
    [20, 3, 10, 0, 4],
    [1, 2, 3, 4, 0]
]

for x in Floyd_Warshall(graph):
    print(*x)