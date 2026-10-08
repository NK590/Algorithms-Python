### Devide and Conquer (분할 정복)

# 주어진 문제를 보다 작은 문제로 쪼개서, 그 작은 문제들을 해결하여 합쳐서 주어진 문제를 해결하는 패러다임
# 일반적으로 원래 문제와 구조는 동일하고, 더 풀기 쉬운 작은 문제로 분할하여 재귀적으로 풀어나감
# 병합 정렬, 퀵 정렬의 구현에서도 분할 정복 해법이 사용됨

### 예제
'''
자연수 A를 B번 곱한 수를 C로 나눈 결과를 출력하시오. 단, A, B, C는 매우 큰 수일 수 있음.
'''

import sys

def product(a, b, c):
    if b == 1:
        return a % c
    
    x = product(a, b//2, c)
    
    if b % 2 == 1:
        return x**2 * a % c
    else:
        return x**2 % c

a, b, c = map(int, sys.stdin.readline().split())

print(product(a, b, c))