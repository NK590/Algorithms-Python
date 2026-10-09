# 연습문제 — 헤비-라이트 분할

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Vertex Add Path Sum](https://judge.yosupo.jp/problem/vertex_add_path_sum) | 핵심 연습 | 경로를 여러 연속 구간으로 분해한다 |
| 2 | [CSES — Path Queries II](https://cses.fi/problemset/task/2134) | 핵심 연습 | 구간 최댓값 자료구조와 경로 분해를 결합한다 |
| 3 | [CSES 1137 Subtree Queries](https://cses.fi/problemset/task/1137) | 점 갱신 + 서브트리 합 | 서브트리가 연속 구간이 되는 전위 번호만으로 풀린다. HLD의 `pos`와 `size`를 이해하는 출발점 |
| 4 | [CSES 1138 Path Queries](https://cses.fi/problemset/task/1138) | 루트까지 경로 합 + 점 갱신 | 루트에서 시작하는 경로만이면 HLD 없이 오일러 투어 + 펜윅 트리. "루트 경로" 와 "임의 경로" 의 차이 |
| 5 | [SPOJ QTREE - Query on a tree](https://www.spoj.com/problems/QTREE/) | 간선 갱신과 경로 최댓값, 여러 테스트 케이스 | 간선 값을 아래쪽 정점에 저장하고, 케이스마다 자료구조를 초기화한다 |
| 6 | [Codeforces 343D Water Tree](https://codeforces.com/problemset/problem/343/D) | 서브트리 채우기 + 루트 경로 비우기 + 점 질의 | 서브트리 연산과 경로 연산이 한 배열에서 섞인다. 시각(타임스탬프)으로 "더 최근에 한 연산" 을 비교하는 발상 |
| 7 | [Library Checker - Vertex Set Path Composite](https://judge.yosupo.jp/problem/vertex_set_path_composite) | 정점의 일차함수를 경로 순서대로 합성 | **교환 법칙이 안 되는** 연산: `u` 쪽 구간과 `v` 쪽 구간을 따로 모아서 방향을 맞춰야 한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
