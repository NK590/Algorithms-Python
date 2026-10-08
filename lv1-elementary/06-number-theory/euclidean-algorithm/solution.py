"""유클리드 호제법 — 두 수의 최대공약수(GCD)를 나머지 연산으로 빠르게 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 핵심 성질: gcd(a, b) = gcd(b, a mod b), 그리고 gcd(a, 0) = a.
- 최소공배수는 lcm(a, b) = a / gcd(a, b) × b 입니다.
- 직접 실행하면 두 수 `A B` 를 받아 최대공약수와 최소공배수를 한 줄씩 출력합니다.
"""
import sys


def gcd(a: int, b: int) -> int:
    """최대공약수. 나머지가 0 이 될 때까지 (a, b) → (b, a mod b) 를 반복한다. O(log min(a, b))"""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def gcd_recursive(a: int, b: int) -> int:
    """같은 계산을 재귀로. 깊이는 O(log min(a, b)) 라서 깊이 제한 걱정이 없다."""
    return abs(a) if b == 0 else gcd_recursive(b, a % b)


def gcd_steps(a: int, b: int) -> int:
    """나머지 연산을 몇 번 했는지. 입력이 연속한 피보나치 수일 때 가장 많다."""
    steps = 0
    while b != 0:
        a, b = b, a % b
        steps += 1
    return steps


def lcm(a: int, b: int) -> int:
    """최소공배수. 먼저 나눈 뒤 곱하면 중간 값이 작다. (다른 언어에서는 오버플로를 피하는 순서이기도 하다)"""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)


def gcd_of_list(numbers: list) -> int:
    """여러 수의 최대공약수. 앞에서부터 하나씩 gcd 를 이어 간다."""
    result = 0
    for x in numbers:
        result = gcd(result, x)
    return result


def main() -> None:
    a, b = map(int, sys.stdin.readline().split())
    print(gcd(a, b))
    print(lcm(a, b))


if __name__ == "__main__":
    main()
