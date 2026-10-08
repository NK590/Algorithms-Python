### Prefix Sum (구간 합)

# 일반적으로 주어진 리스트의 특정 연속된 구간의 합을 구하는 데에 걸리는 시간 복잡도는 O(n)이지만,
# 리스트의 첫번째 원소부터 i번째 원소까지의 합을 DP를 이용하여 미리 구해놓는 전처리 작업을 해두면
# 임의의 연속된 구간의 합을 이 합 리스트의 두 원소를 빼는 식으로 O(1)만에 구할 수 있음
# 쿼리가 많아지면 많아질수록 효율적이고, 이와 같은 아이디어는 다양한 분야에 응용됨

### 예제
'''
임의의 수 n개가 주어졌을 때, 여기서 x번째 수부터 y번째 수까지의 합을 구하시오 (0 <= x <= y < n)
'''
import sys

li = list(map(int, sys.stdin.readline().split()))
x, y = map(int, sys.stdin.readline().split())

# x == 0 일 때도 일반화를 시키기 위해 dp[0] = 0으로 두고, dp[1]부터 li의 0번째 합을 계산
dp = [0 for _ in range(len(li) + 1)]
dp[1] = li[0]

for i in range(2, len(li) + 1):
    dp[i] = dp[i-1] + li[i-1]

print(dp[y+1] - dp[x])