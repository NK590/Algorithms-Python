# 연습문제 — 최소 비용 최대 유량

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — School Dance](https://cses.fi/problemset/task/1696) | 선행 연습 | 선행으로 비용이 없는 이분 매칭 모델부터 구성한다 |
| 2 | [Library Checker — Assignment Problem](https://judge.yosupo.jp/problem/assignment) | 핵심 연습 | 완전 이분 배정에 비용을 붙여 흐름과 헝가리안을 비교한다 |
| 3 | [Codeforces 277E Binary Tree on Plane](https://codeforces.com/problemset/problem/277/E) | 이진 트리 구성에서 간선 길이의 합 최소 (실수 비용) | 부모를 자식 두 개까지 배정하는 최소 비용 매칭. 비용이 실수이므로 정수로 바꾸거나 부동소수 오차 처리 |
| 4 | [Library Checker - Minimum Cost b-flow](https://judge.yosupo.jp/problem/min_cost_b_flow) | 심화·응용 | 공급·수요와 하한 제약을 유량으로 환원한다. 음의 순환 처리도 필요하므로 현재의 최단 증가 경로 구현을 그대로 제출할 수 없다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
