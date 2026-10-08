### Relatively Prime (서로소, Coprime)

# 두 수가 주어졌을 때, 두 수의 공약수가 1 이외에 없을 경우 두 수는 서로소라고 함
# 두 수가 주어졌을 떄, 두 수의 최소공배수가 두 수의 곱일 경우와 동치임
# 유클리드 호제법을 이용하여 최대공약수가 1임을 확인함으로서 찾을 수 있음

### 예제
'''
주어진 두 수가 서로소이면 JA, 아니면 NEIN을 출력하시오
'''

import sys

def GCD(n, m):
    while m:
        n, m = m, n % m
    return n

n, m = map(int, sys.stdin.readline().split())

if GCD(n, m) == 1:
    print('JA')
else:
    print('NEIN')