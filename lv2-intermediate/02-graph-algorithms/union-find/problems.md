# 연습문제 — 유니온 파인드

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Disjoint Set](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_1_A) | 핵심 연습 | 서로소 집합의 합치기와 대표 찾기를 구현한다 |
| 2 | [CSES — Road Construction](https://cses.fi/problemset/task/1676) | 핵심 연습 | 간선 추가마다 요소 수와 최대 크기를 갱신한다 |
| 3 | [Library Checker — Unionfind](https://judge.yosupo.jp/problem/unionfind) | 핵심 연습 | 대표 찾기와 합치기의 기본 입출력을 확인한다 |
| 4 | [LeetCode 547 Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | 연결 요소 | 인접 행렬의 연결된 쌍을 합치고 남은 집합의 수 (`UnionFind.count`) |
| 5 | [LeetCode 684 Redundant Connection](https://leetcode.com/problems/redundant-connection/) | 사이클 간선 | 트리에 간선 하나가 더해진 그래프에서 지울 간선 |
| 6 | [LeetCode 721 Accounts Merge](https://leetcode.com/problems/accounts-merge/) | 응용 | 같은 이메일을 가진 계정을 합친다. 이메일 → 번호 매핑 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
