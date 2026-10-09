# 연습문제 — LIS

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Increasing Subsequence](https://cses.fi/problemset/task/1145) | 핵심 연습 | 길이별 최소 끝값을 이분 탐색으로 갱신한다 |
| 2 | [LeetCode 300 Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | 기본형 | 엄격한 증가. `lis_length` |
| 3 | [LeetCode 354 Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | 2차원 | 너비로 정렬(같은 너비는 높이 내림차순) 후 높이의 LIS |
| 4 | [LeetCode 673 Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) | 개수 | LIS의 개수. `O(n²)` DP(`길이`, `개수` 두 배열). n이 크면 세그먼트 트리가 필요 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
