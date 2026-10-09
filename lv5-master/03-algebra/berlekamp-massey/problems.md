# 연습문제 — 벌레캠프–매시

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Find Linear Recurrence](https://judge.yosupo.jp/problem/find_linear_recurrence) | 핵심 연습 | 오차를 없애며 최소 점화식을 복원한다 |
| 2 | [Library Checker — K-th Term of Linearly Recurrent Sequence](https://judge.yosupo.jp/problem/kth_term_of_linearly_recurrent_sequence) | 핵심 연습 | 복원한 점화식으로 큰 인덱스의 항을 계산한다 |
| 3 | [CSES — Fibonacci Numbers](https://cses.fi/problemset/task/1722) | 핵심 연습 | 알려진 점화식을 작은 수열로 검산한다 |
| 4 | [Library Checker - Sparse Matrix Determinant](https://judge.yosupo.jp/problem/sparse_matrix_det) | 희소 행렬의 행렬식 | Wiedemann: 무작위 벡터로 `uᵀ Mᵏ v` 수열을 만들고 BM으로 최소 다항식을 구해 상수항에서 행렬식. 이 저장소 범위를 넘는 응용이지만 BM의 대표적인 쓰임 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
