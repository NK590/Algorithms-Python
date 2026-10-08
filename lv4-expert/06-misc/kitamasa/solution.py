"""키타마사(Kitamasa) — 선형 점화식 a_n = c_1·a_{n-1} + … + c_k·a_{n-k} 의 n 번째 항을 O(k² log n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 핵심: x^n 을 특성 다항식 f(x) = x^k - c_1 x^{k-1} - … - c_k 로 나눈 나머지 r(x) = r_0 + r_1 x + … + r_{k-1} x^{k-1} 을 구하면 a_n = Σ r_i · a_i (i < k).
  (x^i ↔ a_i 로 보는 선형 범함수가 점화식 때문에 f 의 배수에서 0 이 되기 때문이다.)
  x^n mod f 는 제곱하며 올라가는 거듭제곱(이진 거듭제곱): 다항식 곱은 O(k²), 나머지 계산도 O(k²) 라 전체 O(k² log n).
- kitamasa(coeffs, initial, n, mod=None): 위 방법. mod 가 None 이면 정확한 정수(파이썬 큰 정수), 있으면 mod 로 나눈 나머지.
- bostan_mori(coeffs, initial, n, mod=None): 같은 문제를 "생성 함수 P(x)/Q(x) 의 x^n 계수" 로 푼다. Q(x)Q(-x) 로 분모를 짝수 차수만 남기는 방법으로 n 을 절반씩 줄인다. 같은 O(k² log n) 지만 코드가 더 짧고
  다항식 곱셈을 NTT 로 바꾸면 O(k log k log n) 이 된다.
- matrix_power_term: 비교용 O(k³ log n) 행렬 거듭제곱. sum_of_prefix: a_0 + … + a_n (점화식에 합 항을 붙여 차수 k+1 로).
- fibonacci(n, mod): kitamasa 의 특수한 경우.
- 직접 실행하면 BOJ 13976 형식 — 정수 N (≤ 10^18) — 을 받아 3 × N 판을 2 × 1 타일로 채우는 방법의 수를 10^9+7 로 나눈 나머지로 출력합니다 (N 이 홀수면 0, 짝수면 f_k = 4 f_{k-1} - f_{k-2}, k = N/2).
"""
import sys
from itertools import accumulate
from typing import Optional, Sequence

MOD = 10**9 + 7


def _poly_mul(a: Sequence[int], b: Sequence[int], mod: Optional[int]) -> list[int]:
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                result[i + j] += x * y
    return [v % mod for v in result] if mod else result


def _reduce(poly: list[int], coeffs: Sequence[int]) -> list[int]:
    """poly 를 특성 다항식으로 나눈 나머지 (길이 k). x^k ≡ c_1 x^{k-1} + … + c_k.
    나머지를 mod 로 줄이는 일은 하지 않는다: 다음 곱(_poly_mul) 이 곱한 뒤에 줄이고, 마지막 합도 줄이므로 파이썬 정수가 잠깐 커져도 결과는 같다."""
    k = len(coeffs)
    for i in range(len(poly) - 1, k - 1, -1):  # 위 차수부터 낮춘다 (파이썬 정수는 커져도 되므로 나머지는 마지막에 한 번만)
        top = poly[i]
        if top:
            for j in range(1, k + 1):
                poly[i - j] += top * coeffs[j - 1]
        poly[i] = 0
    return poly[:k] + [0] * (k - len(poly))


def kitamasa(coeffs: Sequence[int], initial: Sequence[int], n: int, mod: Optional[int] = None) -> int:
    """a_n. coeffs = [c_1, …, c_k] (a_i = c_1 a_{i-1} + … + c_k a_{i-k}), initial = [a_0, …, a_{k-1}]. n ≥ 0."""
    k = len(coeffs)
    if len(initial) != k:
        raise ValueError("initial 의 길이는 coeffs 와 같아야 합니다")
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    if k == 0:
        return 0
    if n < k:
        return initial[n] % mod if mod else initial[n]
    result = [1] + [0] * (k - 1)  # x^0
    base = [0, 1] + [0] * (k - 2) if k >= 2 else _reduce([0, 1], coeffs)  # x^1 (k = 1 이면 한 번 줄여야 한다)
    exponent = n
    while exponent:
        if exponent & 1:
            result = _reduce(_poly_mul(result, base, mod), coeffs)
        base = _reduce(_poly_mul(base, base, mod), coeffs)
        exponent >>= 1
    total = sum(r * a for r, a in zip(result, initial))
    return total % mod if mod else total


def bostan_mori(coeffs: Sequence[int], initial: Sequence[int], n: int, mod: Optional[int] = None) -> int:
    """a_n 을 생성 함수 P(x) / Q(x) 의 x^n 계수로 구한다. Q = 1 - c_1 x - … - c_k x^k, P = (A(x) Q(x)) 의 앞 k 항."""
    k = len(coeffs)
    if len(initial) != k:
        raise ValueError("initial 의 길이는 coeffs 와 같아야 합니다")
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    if k == 0:
        return 0
    denominator = [1] + [-c for c in coeffs]
    numerator = _poly_mul(list(initial), denominator, None)[:k]
    if mod:
        denominator = [v % mod for v in denominator]
        numerator = [v % mod for v in numerator]
    while n:
        negated = [v if i % 2 == 0 else (-v % mod if mod else -v) for i, v in enumerate(denominator)]  # Q(-x)
        numerator = _poly_mul(numerator, negated, mod)
        denominator = _poly_mul(denominator, negated, mod)  # Q(x) Q(-x) 는 x 의 짝수 차수만 남는다
        numerator = numerator[n % 2 :: 2]  # n 이 홀수면 홀수 차수, 짝수면 짝수 차수
        denominator = denominator[::2]
        n //= 2
    value = numerator[0] if numerator else 0  # Q(0) = 1 이라 x^0 계수는 P(0)
    return value % mod if mod else value


def matrix_power_term(coeffs: Sequence[int], initial: Sequence[int], n: int, mod: Optional[int] = None) -> int:
    """비교용: 동반 행렬의 거듭제곱 O(k³ log n)."""
    k = len(coeffs)
    if n < k:
        return initial[n] % mod if mod else initial[n]

    def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
        product = [[sum(a[i][t] * b[t][j] for t in range(k)) for j in range(k)] for i in range(k)]
        return [[v % mod for v in row] for row in product] if mod else product

    companion = [list(coeffs)] + [[1 if j == i else 0 for j in range(k)] for i in range(k - 1)]
    result = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    exponent = n - (k - 1)
    while exponent:
        if exponent & 1:
            result = multiply(result, companion)
        companion = multiply(companion, companion)
        exponent >>= 1
    state = list(reversed(initial))  # [a_{k-1}, …, a_0]
    value = sum(result[0][j] * state[j] for j in range(k))
    return value % mod if mod else value


def sum_of_prefix(coeffs: Sequence[int], initial: Sequence[int], n: int, mod: Optional[int] = None) -> int:
    """a_0 + a_1 + … + a_n. 부분합 S_i 도 선형 점화식을 만족한다 (차수 k + 1):
    S_i = (1 + c_1) S_{i-1} + (c_2 - c_1) S_{i-2} + … + (c_k - c_{k-1}) S_{i-k} - c_k S_{i-k-1}  (a_i = S_i - S_{i-1} 을 점화식에 넣으면 나온다)."""
    k = len(coeffs)
    if k == 0:
        return 0
    extended = [1 + coeffs[0]] + [coeffs[j] - coeffs[j - 1] for j in range(1, k)] + [-coeffs[-1]]
    a_k = sum(c * initial[k - 1 - j] for j, c in enumerate(coeffs))  # S_0 … S_k 가 시작값으로 필요하다
    return kitamasa(extended, list(accumulate(list(initial) + [a_k])), n, mod)


def fibonacci(n: int, mod: Optional[int] = None) -> int:
    return kitamasa([1, 1], [0, 1], n, mod)


def main() -> None:
    n = int(sys.stdin.readline())
    if n % 2:
        print(0)
        return
    print(kitamasa([4, MOD - 1], [1, 3], n // 2, MOD))


if __name__ == "__main__":
    main()
