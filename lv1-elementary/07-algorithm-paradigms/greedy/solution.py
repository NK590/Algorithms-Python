### Greedy Algorithm (그리디 알고리즘, 탐욕적 기법)

# 문제를 푸는 과정에서 각 단계별로 가장 득이 되는 해법을 선택하여 풀어가는 방법
# 단, 각 단계별로 최적의 방법을 선택하여 풀었어도 그 답을 모아서 전체적으로 봤을 때
# 최적의 해법이 아닐 수도 있으므로, 사용 용도는 한정적

### 예제
'''
캠핑장을 연속하는 P일 중, L일동안만 사용할 수 있다. 총 휴가가 V일이라고 했을 때, 휴가 V일 동안
캠핑장을 이용할 수 있는 최대 일수를 구하시오.
'''
import sys

l, p, v = map(int, sys.stdin.readline().split())
count = l * (v // p)
if v % p < l:
    count += v % p
else:
    count += l
print(count)