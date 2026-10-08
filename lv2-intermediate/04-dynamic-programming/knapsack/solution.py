### Knapsack Problem (배낭 문제)
# 담을 수 있는 최대 무게가 정해진 배낭과 함께 각각의 무게와 가치가 주어진 물건들이 주어졌을 때,
# 배낭에 남은 아이템들의 가치의 합이 최대가 되도록 하는 아이템의 조합을 찾는 문제

### 분할 가능한 배낭 문제
# 각 물건의 일부분을 분할해서 배낭에 넣을 수 있는 경우
# 그리디 알고리즘으로 비교적 간단하게 풀이 가능

### 0-1 배낭 문제
# 각 물건을 분할할 수 없고, 그 물건을 넣거나 안 넣거나 두 가지의 경우만 존재하는 경우
# 대표적인 NP-완전 문제로, DP, 백트래킹 등의 조합 최적화 풀이법으로 풀어야 함

### 0-1 배낭 문제 예제
# 여행에 필요하다고 생각하는 N개의 물건이 있다. 
# 각 물건은 무게 W와 가치 V를 가지는데, 해당 물건을 배낭에 넣어서 가면 V만큼 즐길 수 있다. 
# 최대 K만큼의 무게만을 넣을 수 있는 배낭만 들고 다닐 수 있다. 
# 배낭에 넣을 수 있는 물건들의 가치의 최댓값은?

# 예시 코드

import sys

input = sys.stdin.readline

n, k = map(int, input().split())
# knapsack : 0 ~ k까지의 무게에 0 ~ n개의 물건을 넣을 때의 최대 가치 2차원 DP
knapsack = [[0 for _ in range(k+1)] for __ in range(n+1)]

# knapsack 리스트와 인덱스를 맞추기 위해 stuff 리스트에 [0, 0]을 넣고 시작
stuff = [[0, 0]]
for _ in range(n):
    stuff.append(list(map(int, input().split())))

for i in range(1, n+1):
    for j in range(1, k+1):
        weight, value = stuff[i]
        if j < weight:
            knapsack[i][j] = knapsack[i-1][j]
        else:
            knapsack[i][j] = max(value + knapsack[i-1][j-weight], knapsack[i-1][j])

print(knapsack[n][k])