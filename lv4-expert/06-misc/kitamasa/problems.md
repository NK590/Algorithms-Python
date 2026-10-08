# 연습문제 — 키타마사

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2749 피보나치 수 3](https://www.acmicpc.net/problem/2749) | `F(n) mod 10⁶`, `n ≤ 10¹⁵` | `fibonacci(n, 10**6)` 한 줄. 피사노 주기로도 풀리니 두 방법 비교 |
| 2 | [백준 11444 피보나치 수 6](https://www.acmicpc.net/problem/11444) | `F(n) mod 10⁹+7`, `n ≤ 10¹⁸` | 키타마사/행렬 거듭제곱의 기본형 |
| 3 | [백준 2133 타일 채우기](https://www.acmicpc.net/problem/2133) | `3 × N` 판을 `2 × 1` 타일로, `N ≤ 30` | 작은 `N`의 점화식 DP. 아래 4번의 점화식을 직접 유도하는 연습 |
| 4 | [백준 13976 타일 채우기 2](https://www.acmicpc.net/problem/13976) | 위와 같은 문제, `N ≤ 10¹⁸` | [solution.py](solution.py)의 `main()`이 같은 형태. `f_k = 4f_{k−1} − f_{k−2}` (`N = 2k`)를 `kitamasa`로. `N`이 홀수면 0 |
| 5 | [Library Checker - Nth Term of Linear Recurrence Sequence](https://judge.yosupo.jp/problem/nth_term_of_linear_recurrence_sequence) | 차수 `d ≤ 3·10⁴`, `n ≤ 10¹⁸`, 모듈러 998244353 | 차수가 커서 이 구현의 `O(k²)`은 느리다. 보스탄-모리 + NTT가 필요한 규모 (다항식 곱을 NTT로 바꿔 보기) |
| 6 | [Project Euler 258 - A lagged Fibonacci sequence](https://projecteuler.net/problem=258) | 차수 2000인 점화식의 `n = 10¹⁸` 번째 항 (모듈러 20092010) | `k = 2000`이면 `O(k² log n) ≈ 2.4·10⁸`번의 곱셈이라 파이썬에서 무겁다 (추정 수 분). 모듈러 20092010이 소수가 아니라 NTT를 바로 쓸 수 없다는 점도 걸림돌 |

## 풀이 메모

- 1번과 2번은 [행렬 거듭제곱](../../../lv3-advanced/07-dp-advanced/matrix-exponentiation/)과 키타마사로 모두 풀립니다. 3×3 이하의 작은 `k`에서는 행렬이 간단하고, `k`가 커질수록 키타마사가 유리합니다 (README의 측정표).
- 3번에서 `3 × 2` 판의 방법 수는 3이고, `N`이 2 늘 때마다 "새로 생기는 막힌 구조" 때문에 `f_N = 3f_{N−2} + 2(f_{N−4} + f_{N−6} + …)`가 됩니다. 이것을 한 번 정리하면 `f_N = 4f_{N−2} − f_{N−4}`가 되고, 4번이 바로 이 선형 점화식입니다.
- 4번은 `N = 2k`로 놓고 `f_0 = 1`, `f_1 = 3`, `f_k = 4f_{k−1} − f_{k−2}`. 홀수 `N`은 칸 수가 홀수라 타일을 못 놓으므로 0.
- 5번을 이 구현으로 풀면 시간 초과입니다. 두 번째 목표는 "곱을 NTT로 바꾸면 얼마나 빨라지는가" 를 확인하는 것: [FFT / NTT](../../01-number-theory/fft-ntt/)의 `convolution`을 `_poly_mul` 자리에 끼우면 보스탄-모리가 `O(k log k log n)`이 됩니다.
- 6번은 차수가 크면서 모듈러가 소수가 아니라는 두 번째 함정이 있습니다. 문제의 의도는 키타마사(또는 다항식 거듭제곱)입니다.
