# 연습문제 — 제곱근 분할

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | 핵심 연습 | 블록 합과 블록 내부 직접 순회를 결합한다 |
| 2 | [CSES — Static Range Minimum Queries](https://cses.fi/problemset/task/1647) | 핵심 연습 | 정적 최소 질의를 블록 경계로 나눠 처리한다 |
| 3 | [LeetCode 307 Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 한 점 갱신 + 구간 합 | 블록 합만 갱신하면 되는 가장 단순한 형태. 펜윅 트리와 비교 |
| 4 | [Codeforces 13E Holes](https://codeforces.com/problemset/problem/13/E) | 점프 횟수와 마지막 구멍 | 블록마다 "블록을 나갈 때까지의 점프 수와 나가는 위치"를 저장. 갱신은 블록 하나만 다시 계산 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
