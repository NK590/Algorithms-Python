# 연습문제 — 좌표 압축

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Distinct Numbers](https://cses.fi/problemset/task/1621) | 핵심 연습 | 서로 다른 값을 정렬하고 순위로 바꾼다 |
| 2 | [CSES — Concert Tickets](https://cses.fi/problemset/task/1091) | 핵심 연습 | 원래 가격과 순위의 대응을 유지한다 |
| 3 | [CSES — Forest Queries II](https://cses.fi/problemset/task/1739) | 심화·응용 | 심화로 좌표와 구간 길이를 혼동하지 않는 전처리를 연습한다 |
| 4 | [LeetCode 1331 Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/) | 1부터 시작하는 순위 | `compress` 결과에 1을 더한 값. 같은 값은 같은 순위 |
| 5 | [LeetCode 315 Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 압축 + 펜윅 트리 | 값을 순위로 바꾸고 뒤에서부터 센다 |
| 6 | [LeetCode 327 Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | 접두사 합 압축 | 접두사 합들을 압축하고 `lower ≤ P[j] − P[i] ≤ upper`인 쌍을 센다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
