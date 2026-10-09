# 연습문제 — 병합 정렬

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Merge Sort](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_5_B) | 핵심 연습 | 두 정렬된 구간을 합치고 비교 횟수를 센다 |
| 2 | [AOJ — Stable Sort](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_2_C) | 핵심 연습 | 안정 정렬의 동률 처리 규칙을 확인한다 |
| 3 | [LeetCode 912 Sort an Array](https://leetcode.com/problems/sort-an-array/) | 직접 구현 | 내장 정렬 없이 O(n log n)으로 정렬하는 것이 취지다. 병합 정렬을 직접 짜서 통과시켜 보자 |
| 4 | [LeetCode 148 Sort List](https://leetcode.com/problems/sort-list/) | 연결 리스트 | 연결 리스트에서는 임의 접근이 안 되므로 병합 정렬이 가장 자연스럽다. 중간 지점 찾기와 합치기를 직접 구현한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
