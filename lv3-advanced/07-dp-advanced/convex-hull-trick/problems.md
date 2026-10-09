# 연습문제 — 볼록 껍질 트릭

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Frog 3](https://atcoder.jp/contests/dp/tasks/dp_z) | 핵심 연습 | 제곱식을 전개해 직선의 기울기와 절편을 분리한다 |
| 2 | [Codeforces 319C Kalila and Dimna](https://codeforces.com/problemset/problem/319/C) | 같은 점화식 + 입력 정렬이 보장됨 | 문제 조건에서 기울기·질의의 단조성을 찾아내는 연습 |
| 3 | [Codeforces 660F Bear and Bowling 4](https://codeforces.com/problemset/problem/660/F) | 부분 배열의 점수 최대화 | 질의 `x`가 정렬되지 않아 이진 탐색 `query`나 리차오 트리가 필요 |
| 4 | [Codeforces 1083E The Fair Nut and Rectangles](https://codeforces.com/problemset/problem/1083/E) | 직사각형 합집합 넓이 − 비용 | 정렬 후 `dp[i] = max_j dp[j] − x_j·y_i + ...`. 겹치는 부분을 빼는 항의 분리 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
