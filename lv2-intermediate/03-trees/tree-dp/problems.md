# 연습문제 — 트리 DP

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Tree Matching](https://cses.fi/problemset/task/1130) | 핵심 연습 | 부모 간선 사용 여부에 따른 트리 매칭 상태를 세운다 |
| 2 | [AtCoder — Independent Set](https://atcoder.jp/contests/dp/tasks/dp_p) | 핵심 연습 | 선택·미선택 상태로 독립 집합 수를 센다 |
| 3 | [CSES — Tree Distances II](https://cses.fi/problemset/task/1133) | 심화·응용 | 심화로 루트를 바꾸며 거리 합을 갱신한다 |
| 4 | [LeetCode 337 House Robber III](https://leetcode.com/problems/house-robber-iii/) | 독립 집합 | 이진 트리에서 인접한 집을 못 턴다. `(턴다, 안 턴다)` 두 상태 |
| 5 | [LeetCode 968 Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras/) | 지배 집합 | 카메라가 자신과 인접한 노드를 감시. 세 가지 상태. `min_dominating_set` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
