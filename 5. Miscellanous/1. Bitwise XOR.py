### Bitwise XOR (XOR 비트 연산, 배타적논리합)

# XOR(Exclusive OR) 연산은 주어진 두 수를 2진수로 변환하여 각 자리수를 비교하여,
# 각 자리수 값이 같으면 0을, 다르면 1을 계산하는 연산

### 예제 1

# a = 5, b = 7 일 때 a = 0b101, b = 0b111 이므로 a ^ b = 0b010 = 2 가 된다.
a = 5
b = 7
print(a ^ b)

# 정의에서 알 수 있는 XOR 연산의 자명한 성질은 다음과 같음
# 1. x ^ 0 = x
# 2. x ^ x = 0
# 3. (x ^ y) ^ z = x ^ (y ^ z)

# 위 