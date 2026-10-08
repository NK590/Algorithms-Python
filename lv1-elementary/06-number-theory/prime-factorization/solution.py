### Prime Factorization (소인수분해)

# 주어진 자연수를 소수의 곱으로 분해하는 과정
# 소인수분해를 하는 방법은 여러 가지가 있는데, 여기서는 그 중 하나를 작성함

### 예시 코드

def Factorize(n):
    factor = 2 
    factors = []
    # 2부터 시작하는 소수로 주어진 수를 나누어 떨어지지 않을 떄까지 계속 나눠서 그 소수를 모아 출력함
    while factor**2 <= n:
        while n % factor == 0:
            factors.append(factor)
            n = n // factor
        # factor가 소수가 아닐 때는 이미 주어진 수를 factor의 소인수로 전부 분해했으므로 고려할 필요 없음
        factor += 1
    if n > 1:
        factors.append(n)
    return factors

### 예제

n1 = 30
n2 = 111111111
n3 = 89216345789123

print(Factorize(n1))
print(Factorize(n2))
print(Factorize(n3))
