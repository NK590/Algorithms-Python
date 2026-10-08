### Dynamic Programming (다이나믹 프로그래밍, 동적 계획법)

# 기존의 해법을 이용하여 새로운 문제를 해결하는 패러다임
# 같은 풀이를 지속적으로 사용하여 다른 문제를 해결해야 하는 상황에서, 기존의 데이터를 재활용하여
# 새로운 문제에 접목시켜 푸는 시간을 줄일 수 있음
# 주로 하위 문제의 답 데이터를 따로 저장하여, 같은 문제를 반복해서 풀지 않고 필요할 때마다 
# 그 데이터를 참조하여 상위 문제를 푸는 형식으로 응용

### 예제
'''
n번째 피보나치 수열을 구하시오 (n >= 2)
'''

import sys

n = int(sys.stdin.readline())

dp = [0 for _ in range(n+1)]
dp[0] = 0
dp[1] = 1

for i in range(2, n+1):
    dp[i] = dp[i-1] + dp[i-2]

print(dp[n])

### 예제 2
'''
수열이 주어질 떄, 그 수열에서 가장 긴 증가하는 부분 수열의 길이를 구하시오 (LIS 문제)
'''

n = int(sys.stdin.readline())
li = list(map(int, sys.stdin.readline().split()))

# dp[i] == 주어진 수열에서 i번째 수를 마지막 수로 갖는 LIS의 길이 
dp = [0 for _ in range(n)]

for i in range(n):
    for j in range(i):
        # i에 대해 0 ~ i-1 번째의 수를 탐색하면서, i번째 수가 j번째 수보다 클 시
        # 해당 dp[j] + 1과 현재 dp[i]를 비교하여 둘 중에 큰 수로 갱신
        if li[i] > li[j]:
            dp[i] = max(dp[i], dp[j] + 1)

# 각각의 원소가 그 수를 마지막으로 갖는 LIS 길이 정보를 담고 있으므로, 그 중 최대값을 출력
print(max(dp))