### Sieve of Eratosthenes (에라토스테네스의 체)

# 특정 수 범위 내의 소수를 구하는 알고리즘
# 작은 수부터 차근차근 그 수의 배수들을 지워나가는 모습이 마치 체로 숫자를 걸러내는 듯하여 이런 이름이 붙음
# 시간 복잡도는 일반적으로 O(nlogn)이나, 조금 더 개선된 알고리즘이 존재함

### 예시 코드

def Sieve(n: list):
    sieve = [True for _ in range(n)]
    
    sqrt = int((n)**0.5)
    for i in range(2, sqrt + 1):
        if sieve[i] == True:
            for j in range(2*i, n, i):
                sieve[j] = False
    
    return [x for x in range(2, n) if sieve[x] == True]

### 예제

n = 1000
print(Sieve(n))