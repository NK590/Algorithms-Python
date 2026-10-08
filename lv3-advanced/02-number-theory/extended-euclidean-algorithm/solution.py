### Extended Euclidean Algorithm (확장 유클리드 호제법)

# 주어진 두 정수의 최대공약수를 찾아내는 유클리드 호제법의 확장형으로,
# 세 정수 a, b, c에 대해 ax + by = c를 만족하는 정수쌍 x, y를 찾아내는 알고리즘
# 이 방정식의 해가 존재하려면 c가 gcd(a, b)의 배수여야 하고, 특별히 c = 1일 때
# ax + by = 1의 형태로 자주 사용됨

### 예시 코드

def Extended_GCD(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    
    while b:
        n, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - n * x1
        y0, y1 = y1, y0 - n * y1
    
    return [x0, y0, a]