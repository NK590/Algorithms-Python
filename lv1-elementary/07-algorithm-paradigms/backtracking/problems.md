# 연습문제 — 백트래킹

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Chessboard and Queens](https://cses.fi/problemset/task/1624) | 핵심 연습 | 열·대각선 충돌을 즉시 잘라 낸다 |
| 2 | [CSES — Creating Strings](https://cses.fi/problemset/task/1622) | 핵심 연습 | 선택 후 상태를 복원하고 중복 순열을 피한다 |
| 3 | [CSES — Grid Paths](https://cses.fi/problemset/task/1625) | 심화·응용 | 심화로 격자의 막힌 경로를 조기에 가지치기한다 |
| 4 | [LeetCode 78 Subsets](https://leetcode.com/problems/subsets/) | 부분집합 | 각 원소를 넣는다/넣지 않는다. `all_subsets` |
| 5 | [LeetCode 22 Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | 가지치기 | 열린 것 ≥ 닫힌 것이라는 조건으로 가지치기. `generate_parentheses` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
