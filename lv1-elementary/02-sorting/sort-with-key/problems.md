# 연습문제 — 정렬 활용

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Tasks and Deadlines](https://cses.fi/problemset/task/1630) | 핵심 연습 | 처리 시간이 짧은 작업부터 정렬해 목적함수를 최적화한다 |
| 2 | [CSES — Movie Festival](https://cses.fi/problemset/task/1629) | 핵심 연습 | 구간의 종료 시각을 정렬 키로 선택한다 |
| 3 | [AOJ — Stable Sort](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_2_C) | 핵심 연습 | 같은 키의 입력 순서를 보존하는 이유를 확인한다 |
| 4 | [LeetCode 179 Largest Number](https://leetcode.com/problems/largest-number/) | 비교 함수 | `a+b`와 `b+a`를 비교하는 `cmp_to_key` (`largest_number`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
