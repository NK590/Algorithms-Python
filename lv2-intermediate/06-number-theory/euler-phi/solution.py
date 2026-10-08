### Euler's Phi Function (오일러 피 함수, Euler's Totient Function)

# 어떤 양의 정수 N이 주어졌을 때, N 미만의 양의 정수에 대해 N과 서로소인 숫자의 개수를 세는 함수
# 단독으로 이용된다기보단 오일러 정리 등 다른 정수론 이론에 응용되어 사용됨

# N 미만의 모든 수를 N과 유클리드 호제법을 사용하여 구현할 수도 있지만 매우 비효율적이고, 
# 일반적으로 구현 시 다음 피 함수의 성질들이 이용됨

# 1. p가 소수일 때, Phi(p) = p - 1
# 2. 1.의 일반화로, p가 소수이고 k가 1 이상의 정수일 때, Phi(p^k) = p^(k) - p^(k-1)
# 3. m과 n이 서로소일 때, Phi(m*n) = Phi(m) * Phi(n)

### 예시 코드

def Phi(n):
    factor = 2
    factors = []
    while factor**2 <= n:
        while n % factor == 0:
            factors.append(factor)
            n = n // factor
        factor += 1
    if n > 1:
        factors.append(n)
    # 여기까지 소인수분해 알고리즘
    
    # 반복되는 소수를 제외하고 소수의 종류만 추려냄
    fac_list = list(set(factors))
    
    # 위 2.와 3.성질을 이용하여 답을 계산
    ans = 1
    for i in range(len(fac_list)):
        ans *= fac_list[i]**(factors.count(fac_list[i])) - fac_list[i]**(factors.count(fac_list[i])-1)
    return ans

### 예제

n1 = 5
n2 = 11111
n3 = 98234651852345744

print(Phi(n1))
print(Phi(n2))
print(Phi(n3))