# 연습문제 — SCC (강한 연결 요소)

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Planets and Kingdoms](https://cses.fi/problemset/task/1683) | 핵심 연습 | 정점을 강한 연결 요소 번호로 묶는다 |
| 2 | [Library Checker — Strongly Connected Components](https://judge.yosupo.jp/problem/scc) | 핵심 연습 | 축약 DAG의 위상 순서 조건을 확인한다 |
| 3 | [CSES — Flight Routes Check](https://cses.fi/problemset/task/1682) | 선행 연습 | 선행으로 정방향·역방향 도달성을 비교한다 |
| 4 | [LeetCode 802 Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) | 사이클에 닿지 않는 정점 | 사이클에 속하거나 사이클로 이어지는 정점을 제외. 간선을 뒤집은 위상 정렬이나 SCC로 풀린다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
