# 연습문제 — 세그먼트 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Range Minimum Query](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_A) | 핵심 연습 | 점 갱신과 구간 최솟값을 구현한다 |
| 2 | [CSES — Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | 핵심 연습 | 구간을 결합하는 항등원을 정한다 |
| 3 | [CSES — Hotel Queries](https://cses.fi/problemset/task/1143) | 심화·응용 | 심화로 노드의 최댓값을 이용해 첫 가능한 위치를 찾는다 |
| 4 | [LeetCode 307 Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 점 갱신 + 구간 합 | 가장 기본적인 점 갱신. 합은 펜윅 트리로도 가능 |
| 5 | [LeetCode 699 Falling Squares](https://leetcode.com/problems/falling-squares/) | 구간 최댓값 + 구간 대입 | 떨어지는 정사각형의 높이. 구간 갱신이 필요해 [느리게 갱신되는 세그먼트 트리](../lazy-propagation/) 연습으로 이어진다 |
| 6 | [LeetCode 2407 Longest Increasing Subsequence II](https://leetcode.com/problems/longest-increasing-subsequence-ii/) | 트리 위의 DP | 값 구간 `[x − k, x − 1]`의 최대 길이를 트리에서 질의하고 `x` 위치를 갱신 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
