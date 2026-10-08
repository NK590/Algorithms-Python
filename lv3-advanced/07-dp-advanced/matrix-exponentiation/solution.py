"""행렬 거듭제곱(Matrix Exponentiation) — 선형 점화식의 n 번째 항·정해진 길이의 경로 수를 O(k³ log n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 상태 벡터 v 에서 다음 상태로 가는 규칙이 "v 의 선형 결합" 이면 v_next = M·v 로 쓸 수 있고, n 번 하면 M^n·v. M^n 은 빠른 거듭제곱(제곱을 반복)으로 O(k³ log n).
- mat_pow(A, e, mod): 정사각 행렬의 거듭제곱. mod 를 주면 모든 곱셈 뒤에 나머지를 취합니다.
- fibonacci_matrix / fibonacci_doubling: F(0)=0, F(1)=1. 같은 값을 행렬로, 그리고 행렬 없이 "두 배로 뛰기" 공식으로 구합니다.
- linear_recurrence_nth(coeffs, initial, n): a_n = c_1·a_{n-1} + … + c_k·a_{n-k} 의 n 번째 항 (초기값 a_0..a_{k-1}).
- recurrence_prefix_sum: a_0 + … + a_n — 상태에 "지금까지의 합" 을 한 칸 더 넣는 방법.
- count_walks: 인접 행렬의 거듭제곱으로 "정확히 L 개의 간선을 지나는 경로(walk)의 수".
- longest_walks: (max, +) 반환 구조로 같은 구조를 풀어 "정확히 L 개의 간선을 지나는 가장 무거운 경로".
- 직접 실행하면 n 을 받아 F(n) mod 1_000_000_007 을 출력합니다 (BOJ 11444 형식, n ≤ 10^18).
"""
import sys
from typing import Optional, Sequence

Matrix = list[list[int]]


def mat_identity(n: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def _check_square(a: Sequence[Sequence[int]]) -> int:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("정사각 행렬이어야 합니다")
    return n


def mat_mul(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], mod: Optional[int] = None) -> Matrix:
    """a·b (정사각 행렬). mod 가 있으면 각 칸을 mod 로 나눈 나머지."""
    n = _check_square(a)
    if _check_square(b) != n:
        raise ValueError("두 행렬의 크기가 같아야 합니다")
    b_columns = list(zip(*b))
    result = [[sum(x * y for x, y in zip(row, column)) for column in b_columns] for row in a]
    if mod is not None:
        result = [[value % mod for value in row] for row in result]
    return result


def mat_pow(a: Sequence[Sequence[int]], e: int, mod: Optional[int] = None) -> Matrix:
    """a^e. e = 0 이면 단위 행렬. 제곱을 반복하며 e 의 켜진 비트에서만 결과에 곱한다."""
    if e < 0:
        raise ValueError("지수는 0 이상이어야 합니다")
    n = _check_square(a)
    result = mat_identity(n)
    if mod is not None:
        result = [[value % mod for value in row] for row in result]  # mod == 1 이면 단위 행렬도 0
    base = [list(row) for row in a]
    while e:
        if e & 1:
            result = mat_mul(result, base, mod)
        base = mat_mul(base, base, mod)
        e >>= 1
    return result


def fibonacci_matrix(n: int, mod: Optional[int] = None) -> int:
    """[[1, 1], [1, 0]]^n 의 오른쪽 위 값이 F(n). n < 0 이면 mat_pow 가 ValueError."""
    return mat_pow([[1, 1], [1, 0]], n, mod)[0][1]


def fibonacci_doubling(n: int, mod: Optional[int] = None) -> int:
    """행렬 없이 F(2k) = F(k)·(2F(k+1) - F(k)),  F(2k+1) = F(k)² + F(k+1)² 로 두 배씩 뛴다. O(log n)."""
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")

    def pair(m: int) -> tuple[int, int]:  # (F(m), F(m+1))
        if m == 0:
            return 0, 1
        f, g = pair(m >> 1)
        c = f * (2 * g - f)
        d = f * f + g * g
        if mod is not None:
            c, d = c % mod, d % mod
        return (d, c + d) if m & 1 else (c, d)

    value = pair(n)[0]
    return value % mod if mod is not None else value


def linear_recurrence_nth(coeffs: Sequence[int], initial: Sequence[int], n: int, mod: Optional[int] = None) -> int:
    """a_n = coeffs[0]·a_{n-1} + coeffs[1]·a_{n-2} + … + coeffs[k-1]·a_{n-k},  a_0..a_{k-1} = initial."""
    k = len(coeffs)
    if k == 0 or len(initial) != k:
        raise ValueError("초기값의 개수는 계수의 개수와 같고 0 이 아니어야 합니다")
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    if n < k:
        return initial[n] % mod if mod is not None else initial[n]
    # 상태 벡터 (a_m, a_{m-1}, …, a_{m-k+1}) 에 companion 행렬을 곱하면 m 이 하나 늘어난다
    companion = [list(coeffs)] + [[1 if j == i else 0 for j in range(k)] for i in range(k - 1)]
    power = mat_pow(companion, n - (k - 1), mod)
    state = list(reversed(initial))  # (a_{k-1}, …, a_0)
    value = sum(power[0][j] * state[j] for j in range(k))
    return value % mod if mod is not None else value


def recurrence_prefix_sum(coeffs: Sequence[int], initial: Sequence[int], n: int, mod: Optional[int] = None) -> int:
    """a_0 + a_1 + … + a_n. 상태 벡터에 S_m = a_0 + … + a_m 을 한 칸 더해 (k + 1) 차 행렬로 만든다."""
    k = len(coeffs)
    if k == 0 or len(initial) != k:
        raise ValueError("초기값의 개수는 계수의 개수와 같고 0 이 아니어야 합니다")
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    if n < k:
        total = sum(initial[: n + 1])
        return total % mod if mod is not None else total
    # 상태 (S_m, a_m, a_{m-1}, …, a_{m-k+1}):  S_{m+1} = S_m + a_{m+1} = S_m + Σ c_i·a_{m+1-i}
    size = k + 1
    step = [[0] * size for _ in range(size)]
    step[0][0] = 1
    for j in range(k):
        step[0][1 + j] = coeffs[j]
    step[1] = list(step[0])  # a_{m+1} 도 같은 식(S 칸은 0)
    step[1][0] = 0
    for i in range(1, k):
        step[1 + i][i] = 1
    state = [sum(initial)] + list(reversed(initial))  # m = k-1 일 때의 상태
    power = mat_pow(step, n - (k - 1), mod)
    value = sum(power[0][j] * state[j] for j in range(size))
    return value % mod if mod is not None else value


def count_walks(adj: Sequence[Sequence[int]], length: int, mod: Optional[int] = None) -> Matrix:
    """결과[i][j] = i 에서 j 까지 정확히 length 개의 간선을 지나는 경로(같은 정점·간선 반복 허용)의 수. adj[i][j] = i→j 간선 수."""
    return mat_pow(adj, length, mod)


def longest_walks(weights: Sequence[Sequence[Optional[int]]], length: int) -> list[list[Optional[int]]]:
    """(max, +) 거듭제곱: 결과[i][j] = i 에서 j 까지 정확히 length 개의 간선을 지나는 경로의 최대 가중치 합. 없으면 None.
    weights[i][j] = 간선 i→j 의 가중치 (없으면 None)."""
    if length < 0:
        raise ValueError("길이는 0 이상이어야 합니다")
    n = _check_square(weights)

    def multiply(a, b):
        result = [[None] * n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if a[i][k] is None:
                    continue
                for j in range(n):
                    if b[k][j] is None:
                        continue
                    candidate = a[i][k] + b[k][j]
                    if result[i][j] is None or candidate > result[i][j]:
                        result[i][j] = candidate
        return result

    result = [[0 if i == j else None for j in range(n)] for i in range(n)]  # (max, +) 의 단위 원: 대각선 0, 나머지 -inf
    base = [list(row) for row in weights]
    e = length
    while e:
        if e & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        e >>= 1
    return result


def main() -> None:
    n = int(sys.stdin.readline())
    print(fibonacci_matrix(n, 1_000_000_007))


if __name__ == "__main__":
    main()
