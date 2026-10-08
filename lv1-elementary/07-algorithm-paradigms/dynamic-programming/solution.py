"""다이나믹 프로그래밍(DP) — 같은 부분 문제를 한 번만 풀고 저장해 두었다가 다시 쓰기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 풀이 순서: ① 상태 정의 ② 점화식 ③ 초기값 ④ 계산 순서.
- 피보나치를 (느린 재귀 → 메모이제이션 → 표 채우기 → 변수 두 개) 로 고쳐 가며 DP 가 빨라지는 이유를 보여 줍니다.
- 직접 실행하면 `N` 을 받아 N 을 1 로 만드는 연산(÷3, ÷2, −1)의 최소 횟수를 출력합니다.
"""
import sys


def fib_naive(n: int) -> int:
    """정의 그대로의 재귀. 같은 값을 계속 다시 계산해서 O(φⁿ) (φ ≈ 1.618) 으로 느리다."""
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)


def fib_naive_calls(n: int) -> int:
    """fib_naive(n) 이 함수를 몇 번 호출하는가. 호출 횟수 = 2·F(n+1) − 1 이다."""
    return 1 if n < 2 else 1 + fib_naive_calls(n - 1) + fib_naive_calls(n - 2)


def fib_memo(n: int, memo: dict = None) -> int:
    """위에서 아래로(top-down): 같은 재귀지만 한 번 구한 값을 memo 에 저장한다. O(n) 시간, 재귀 깊이도 n."""
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def fib_table(n: int) -> list:
    """아래에서 위로(bottom-up): 작은 것부터 표를 채운다. 반환값[i] = F(i)."""
    dp = [0] * (n + 1)
    if n >= 1:
        dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp


def fib_fast(n: int) -> int:
    """표에서 직전 두 값만 쓰므로 변수 두 개면 된다. O(n) 시간, O(1) 공간."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def climb_stairs(n: int) -> int:
    """한 번에 1칸 또는 2칸씩 올라 n 칸을 오르는 방법의 수. 마지막 걸음이 1칸 또는 2칸이므로 f(n) = f(n−1) + f(n−2)."""
    a, b = 1, 1  # f(0) = 1 (제자리), f(1) = 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b if n >= 1 else 1


def tile_2xn(n: int, mod: int = 10007) -> int:
    """2×n 직사각형을 2×1, 1×2 타일로 채우는 방법의 수 (mod 로 나눈 나머지). 맨 왼쪽을 세로 1장 / 가로 2장으로 시작한다."""
    a, b = 1, 1  # t(0) = 1, t(1) = 1
    for _ in range(n - 1):
        a, b = b, (a + b) % mod
    return (b if n >= 1 else 1) % mod


def min_steps_to_one(n: int) -> tuple:
    """n 에 (n % 3 == 0 이면 ÷3, n % 2 == 0 이면 ÷2, −1) 연산을 써서 1 로 만드는 최소 횟수와 그때의 경로를 반환한다.

    dp[i] = i 를 1 로 만드는 최소 횟수. 점화식: dp[i] = 1 + min(dp[i−1], dp[i/2], dp[i/3]).
    parent[i] 에 어디서 왔는지 적어 두면 경로를 복원할 수 있다. 경로는 [n, …, 1]."""
    dp = [0] * (n + 1)
    parent = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + 1
        parent[i] = i - 1
        if i % 2 == 0 and dp[i // 2] + 1 < dp[i]:
            dp[i] = dp[i // 2] + 1
            parent[i] = i // 2
        if i % 3 == 0 and dp[i // 3] + 1 < dp[i]:
            dp[i] = dp[i // 3] + 1
            parent[i] = i // 3
    path = [n]
    while path[-1] != 1:
        path.append(parent[path[-1]])
    return dp[n], path


def main() -> None:
    n = int(sys.stdin.readline())
    print(min_steps_to_one(n)[0])


if __name__ == "__main__":
    main()
