# 연습문제 — 단절점과 단절선

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Bridge](https://atcoder.jp/contests/abc075/tasks/abc075_c) | 핵심 연습 | 작은 그래프에서 간선 제거를 직접 해 정답 기준을 만든다 |
| 2 | [LeetCode 1192 Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) | 단절선 | `n ≤ 10⁵`. 재귀 DFS는 파이썬에서 깊이 제한에 걸리니 반복문 구현이 필요 |
| 3 | [Codeforces 118E Bertown roads](https://codeforces.com/problemset/problem/118/E) | 방향 부여 | 단절선이 있으면 불가능, 없으면 DFS 트리의 간선은 내려가는 방향, 역방향 간선은 올라가는 방향으로 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
