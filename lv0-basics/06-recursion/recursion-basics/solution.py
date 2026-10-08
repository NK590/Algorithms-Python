"""재귀 함수의 구조 — 자기 자신을 호출하는 함수의 기저 조건과 재귀 호출

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 재귀 함수에는 (1) 더 이상 호출하지 않고 답을 바로 주는 기저 조건, (2) 더 작은 문제로 자신을 호출하는 부분이 있어야 합니다.
- 직접 실행하면 N 을 받아 N! 을 출력합니다.
"""
import sys


def factorial(n: int) -> int:
    """n! = n × (n-1)!  기저 조건: 0! = 1"""
    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """F(n) = F(n-1) + F(n-2). 같은 값을 계속 다시 계산해서 호출 횟수가 지수적으로 늘어난다."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_call_count(n: int) -> int:
    """fibonacci(n) 이 부르는 함수 호출의 총 횟수 (자기 자신 포함)."""
    if n < 2:
        return 1
    return 1 + fibonacci_call_count(n - 1) + fibonacci_call_count(n - 2)


def fibonacci_memo(n: int, memo: dict | None = None) -> int:
    """한 번 구한 값을 기억해 두면 각 n 을 한 번씩만 계산한다. O(n)."""
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def sum_of_digits(n: int) -> int:
    """자릿수의 합. 마지막 자리를 떼어 내고 나머지로 같은 문제를 푼다."""
    if n < 10:
        return n
    return n % 10 + sum_of_digits(n // 10)


def reverse_string(s: str) -> str:
    """문자열을 뒤집는다. 첫 글자를 떼어 뒤로 보낸다."""
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]


def sum_to_recursive(n: int) -> int:
    """1 + 2 + ... + n 을 재귀로. n 이 크면 파이썬의 재귀 깊이 제한(기본 1000)에 걸린다."""
    if n == 0:
        return 0
    return n + sum_to_recursive(n - 1)


def sum_to_iterative(n: int) -> int:
    """같은 값을 반복문으로. 깊이 제한이 없다."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def cantor_string(n: int) -> str:
    """칸토어 집합 문자열: 길이 3^n 의 `-` 에서 가운데 1/3 을 공백으로 바꾸는 일을 n 번 반복한다."""
    if n == 0:
        return "-"
    left = cantor_string(n - 1)
    return left + " " * len(left) + left


def main() -> None:
    print(factorial(int(sys.stdin.readline())))


if __name__ == "__main__":
    main()
