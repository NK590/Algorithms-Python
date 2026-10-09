# 연습문제 — 다항식 연산

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Inv of Formal Power Series](https://judge.yosupo.jp/problem/inv_of_formal_power_series) | 핵심 연습 | 정밀도를 두 배로 늘리는 뉴턴 역수를 구현한다 |
| 2 | [Library Checker — Exp of Formal Power Series](https://judge.yosupo.jp/problem/exp_of_formal_power_series) | 핵심 연습 | 로그와 역수를 결합해 형식적 지수 급수를 구한다 |
| 3 | [Library Checker - Division of Polynomials](https://judge.yosupo.jp/problem/division_of_polynomials) | 다항식의 몫과 나머지 | 뒤집어서 역수로 몫 구하기 (`poly_divmod`) |
| 4 | [Library Checker - Log of Formal Power Series](https://judge.yosupo.jp/problem/log_of_formal_power_series) | 급수의 로그 | 도함수와 역수와 적분 (`poly_log`) |
| 5 | [Library Checker - Pow of Formal Power Series](https://judge.yosupo.jp/problem/pow_of_formal_power_series) | `f^k` (`k`가 매우 큼) | 앞의 0과 상수항을 따로 처리하고 `exp(k log)` (`poly_pow`) |
| 6 | [Library Checker - Sqrt of Formal Power Series](https://judge.yosupo.jp/problem/sqrt_of_formal_power_series) | 급수의 제곱근 (없으면 -1) | 모듈러 제곱근과 낮은 차수의 홀짝 (`poly_sqrt`, `mod_sqrt`) |
| 7 | [Library Checker - Multipoint Evaluation](https://judge.yosupo.jp/problem/multipoint_evaluation) | 다항식을 `n`개 점에서 평가 | 부분곱 트리와 나머지 트리 (`multipoint_evaluate`) |
| 8 | [Library Checker - Polynomial Interpolation](https://judge.yosupo.jp/problem/polynomial_interpolation) | `n`개 점을 지나는 다항식 | 라그랑주의 분모를 `P'(x_i)`로, 부분곱 트리를 올라가며 합치기 (`interpolate`) |
| 9 | [Library Checker - Polynomial Taylor Shift](https://judge.yosupo.jp/problem/polynomial_taylor_shift) | `f(x + c)` | 팩토리얼로 나누어 합성곱 한 번 (`taylor_shift`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
