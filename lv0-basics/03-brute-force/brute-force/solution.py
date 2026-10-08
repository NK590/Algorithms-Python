### Brute Force Algorithm (브루트 포스 알고리즘, 완전 탐색 알고리즘)

# 가능한 모든 방식을 전부 탐색하며 해답을 찾아내는 방식
# 거의 모든 상황에서 비효율적인 방식이지만, 별다른 기교 없이 확실하게 답을 찾을 수 있다는 점에서
# 탐색해야 될 경우의 수가 비교적 적은 경우 이용 가치가 있음
# 그 특성상 백트래킹이 혼용되어 쓰이는 경우가 종종 있음

### 예제
'''
1부터 1000 사이의 자연수 중에서, 각 자리의 숫자가 등차수열을 이루는 수의 개수를 구하시오.
'''

count = 0
for num in range(1, 1001):
    temp = set()
    w = str(num)
    for i in range(len(w)-1):
        temp.add(int(w[i+1]) - int(w[i]))
    if len(temp) in [0, 1]:
        count += 1
    
print(count)