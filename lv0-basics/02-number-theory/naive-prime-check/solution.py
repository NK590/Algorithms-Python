### Naive Prime Number Check (단순 소수 판별)

# 어떤 주어진 수 a가 소수인지 판별하는 가장 단순한 방법은, 2에서 a-1까지 모든 수로 나눠보면서
# 나누어 떨어지는 수가 있는지 알아보고, 나누어 떨어지는 수가 하나라도 있으면 소수가 아니고,
# 하나도 없으면 소수라고 할 수 있음
# 여기서, 만약 a가 i로 나누어 떨어진다면 a는 a/i로도 나누어 떨어진다는 점을 생각해보면,
# 2부터 sqrt(a)까지의 수만 체크해보면 됨

### 예시 코드

from math import sqrt

def isPrime(n: int):
    if n == 1:
        return False
    
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    
    return True

### 예제

a = 2
b = 101
c = 1892674

print(a, isPrime(a))
print(b, isPrime(b))
print(c, isPrime(c))
