# 연습문제 — 퀵 정렬

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Partition](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_6_B) | 핵심 연습 | 피벗을 기준으로 구간을 분할한다 |
| 2 | [AOJ — Quick Sort](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_6_C) | 핵심 연습 | 퀵 정렬의 정렬 결과와 안정성을 별도로 검사한다 |
| 3 | [LeetCode 75 Sort Colors](https://leetcode.com/problems/sort-colors/) | 3분할 | 값이 0, 1, 2뿐인 배열을 한 번 훑어 정렬한다. 이 문서의 네덜란드 국기 분할(`_partition`)이 그대로 풀이다 |
| 4 | [LeetCode 215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 퀵 셀렉트 / 힙 | k번째로 큰 값. 퀵 셀렉트(평균 O(n))와 크기 k짜리 힙(O(n log k)) 두 가지로 풀어 비교해 보자 |
| 5 | [LeetCode 912 Sort an Array](https://leetcode.com/problems/sort-an-array/) | 직접 구현 | 내장 정렬 없이 정렬을 구현하는 문제. 퀵 정렬은 입력에 같은 값이 많거나 정렬되어 있으면 느려지는 구현이 있으니, 무작위 기준값과 3분할이 왜 필요한지 확인할 수 있다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
