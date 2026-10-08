### Euclidean Algorithm (유클리드 호제법)

# 두 양의 정수의 최대공약수(Great Common Divisor, GCD)를 구하는 알고리즘
# a, b를 각각 두 양의 정수라 하고, a = bq + r (0 <= r < b)라 하면,
# a, b의 최대공약수는 b, r의 최대공약수와 같은 성질을 이용, 두 수를 바꿔가며 서로를 나눠서
# 최대공약수를 구하는 방식으로 사용됨

### 예시 코드

def GCD(a: int, b: int):
    # b가 0이 될 떄까지, a와 b를 번갈아가면서 나누면서 그 나머지를 치환
    while b:
        a, b = b, a % b
    return a

# 또한, 두 수의 곱을 두 수의 최대공약수로 나누면 두 수의 최소공배수(Least Common Multiple, LCM)
# 를 구할 수 있음

def LCM(a: int, b: int):
    return a * b // GCD(a, b)

### 예제

a, b = 18, 30
print("a =", a, "b =", b)
print("GCD is", GCD(a, b))
print("LCM is", LCM(a, b))