# 연습문제 — 다항식 연산

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | (직접 만들어 보는 문제) 분할수, 벨 수, 카탈란 수 | 생성함수 | `partition_numbers`, `bell_numbers`, `catalan_numbers`의 결과를 DP나 닫힌 식과 비교 |
| 2 | [Library Checker - Inv of Formal Power Series](https://judge.yosupo.jp/problem/inv_of_formal_power_series) | 급수의 역수 | 뉴턴 방법의 기본 틀 (`poly_inverse`) |
| 3 | [Library Checker - Division of Polynomials](https://judge.yosupo.jp/problem/division_of_polynomials) | 다항식의 몫과 나머지 | 뒤집어서 역수로 몫 구하기 (`poly_divmod`) |
| 4 | [Library Checker - Log of Formal Power Series](https://judge.yosupo.jp/problem/log_of_formal_power_series) | 급수의 로그 | 도함수와 역수와 적분 (`poly_log`) |
| 5 | [Library Checker - Exp of Formal Power Series](https://judge.yosupo.jp/problem/exp_of_formal_power_series) | 급수의 지수 | [solution.py](solution.py)의 `main()`이 같은 형식. 뉴턴 방법 (`poly_exp`) |
| 6 | [Library Checker - Pow of Formal Power Series](https://judge.yosupo.jp/problem/pow_of_formal_power_series) | `f^k` (`k`가 매우 큼) | 앞의 0과 상수항을 따로 처리하고 `exp(k log)` (`poly_pow`) |
| 7 | [Library Checker - Sqrt of Formal Power Series](https://judge.yosupo.jp/problem/sqrt_of_formal_power_series) | 급수의 제곱근 (없으면 -1) | 모듈러 제곱근과 낮은 차수의 홀짝 (`poly_sqrt`, `mod_sqrt`) |
| 8 | [Library Checker - Multipoint Evaluation](https://judge.yosupo.jp/problem/multipoint_evaluation) | 다항식을 `n`개 점에서 평가 | 부분곱 트리와 나머지 트리 (`multipoint_evaluate`) |
| 9 | [Library Checker - Polynomial Interpolation](https://judge.yosupo.jp/problem/polynomial_interpolation) | `n`개 점을 지나는 다항식 | 라그랑주의 분모를 `P'(x_i)`로, 부분곱 트리를 올라가며 합치기 (`interpolate`) |
| 10 | [Library Checker - Polynomial Taylor Shift](https://judge.yosupo.jp/problem/polynomial_taylor_shift) | `f(x + c)` | 팩토리얼로 나누어 합성곱 한 번 (`taylor_shift`) |

## 풀이 메모

- 2~10번은 모두 입력이 `5·10⁵`입니다. 이 저장소의 구현은 파이썬이라 `n ≈ 2¹⁵` 정도까지가 현실적이어서 (README 5절의 측정) 통과용이 아니라 *구조를 이해하고 작은 입력에서 정답과 맞춰 보는* 용도입니다.
- 순서는 곱셈 → 역수 → 나눗셈 → 로그 → 지수 → 거듭제곱 → 제곱근 → 다점 계산 → 보간 순으로 쌓는 것이 자연스럽습니다. 각 단계의 테스트는 `O(n²)` 점화식으로 만든 순진한 구현과 비교합니다.
