# 연습문제 — 최소 공통 조상 (LCA)

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Company Queries II](https://cses.fi/problemset/task/1688) | 핵심 연습 | 깊이를 맞추고 두 정점을 함께 올린다 |
| 2 | [CSES — Distance Queries](https://cses.fi/problemset/task/1135) | 핵심 연습 | LCA로 트리 경로 거리를 계산한다 |
| 3 | [Library Checker — Lowest Common Ancestor](https://judge.yosupo.jp/problem/lca) | 핵심 연습 | 0 기반 정점 입력의 기본 LCA를 구현한다 |
| 4 | [LeetCode 235 Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | BST의 LCA | 값의 대소만으로 내려가며 갈라지는 곳이 LCA. 표가 필요 없는 가장 쉬운 경우 |
| 5 | [LeetCode 236 Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 이진 트리의 LCA | 질의가 한 번이면 DFS 한 번으로 충분하다. 두 노드를 서브트리에서 각각 찾았는지 올려 보낸다 |
| 6 | [LeetCode 1483 Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | `k`번째 조상 | `kth_ancestor`. 루트를 넘어가면 -1을 돌려주는 규칙에 주의 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
