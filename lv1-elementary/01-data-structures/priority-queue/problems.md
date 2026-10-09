# 연습문제 — 우선순위 큐

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Priority Queue](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_9_C) | 핵심 연습 | 최대 힙의 삽입과 추출을 직접 구현한다 |
| 2 | [CSES — Room Allocation](https://cses.fi/problemset/task/1164) | 심화·응용 | 방이 비는 시각을 최소 힙에 두고 재사용할 방을 선택한다. 같은 시각의 입실·퇴실 조건도 확인한다 |
| 3 | [CSES — Shortest Routes I](https://cses.fi/problemset/task/1671) | 심화·응용 | 다익스트라를 배운 뒤 최단 거리 후보를 최소 힙에서 꺼내고 낡은 후보를 버린다 |
| 4 | [LeetCode 215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 상위 k개 | 크기 k의 최소 힙만 유지한다 (`kth_largest`) |
| 5 | [LeetCode 23 Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | K개 합치기 | 각 리스트의 맨 앞만 힙에 두고 가장 작은 것을 꺼낸다 (`merge_sorted_lists`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
