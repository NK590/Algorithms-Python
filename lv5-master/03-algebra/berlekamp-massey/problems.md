# 연습문제 — 벌레캠프–매시

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | (직접 만들어 보는 문제) 피보나치, 루카스, `n²`, `n³`, 3×2n 타일 수 | 수열의 앞부분 → 점화식 | 어떤 수열이 어떤 길이의 점화식을 가지는지 `berlekamp_massey`로 확인. 다항식 수열 `nᵈ`은 길이 `d+1` (README 7절), 분할수는 `L ≈ n/2` |
| 2 | [BOJ 13976 타일 채우기 2](https://www.acmicpc.net/problem/13976) | 3 × N 판을 2 × 1 타일로 채우는 수 (`N ≤ 10¹⁸`) | 점화식을 직접 세우지 말고 작은 `N`을 DP로 구한 뒤 이 알고리즘으로 점화식을 추정하고 `nth_term`으로 `10¹⁸`번째 항. [키타마사](../../../lv4-expert/06-misc/kitamasa/)의 `main()`과 같은 답이 나와야 한다 |
| 3 | [Library Checker - Find Linear Recurrence](https://judge.yosupo.jp/problem/find_linear_recurrence) | 수열의 최소 선형 점화식 | [solution.py](solution.py)의 `main()`이 같은 형식 (`mod = 998244353`). 항이 많으면 `O(n²)`가 파이썬에서 느리다 |
| 4 | [Library Checker - Sparse Matrix Determinant](https://judge.yosupo.jp/problem/sparse_matrix_det) | 희소 행렬의 행렬식 | Wiedemann: 무작위 벡터로 `uᵀ Mᵏ v` 수열을 만들고 BM으로 최소 다항식을 구해 상수항에서 행렬식. 이 저장소 범위를 넘는 응용이지만 BM의 대표적인 쓰임 |

## 풀이 메모

- 1번에서 항의 개수를 `2L`보다 적게 주면 다른 점화식이 나오는 것을 직접 확인하세요 (README 2절).
- 2번은 `N`이 홀수면 0, 짝수면 점화식이 `f_k = 4 f_{k−1} − f_{k−2}`임이 알려져 있습니다 (실행으로 `[0, 4, 0, −1]`을 확인). 그래도 *모르는 척* 하고 BM으로 구해 보는 것이 연습입니다.
- 4번은 `mod p` 위에서 하므로 행렬식도 `mod p` 값이며, 확률적 알고리즘이라 실패 확률을 줄이려면 같은 입력에 여러 번 시도합니다.
