# 연습문제 — 비트마스크

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Apple Division](https://cses.fi/problemset/task/1623) | 핵심 연습 | 비트가 켜진 위치를 부분집합의 원소로 해석한다 |
| 2 | [AtCoder — Matching](https://atcoder.jp/contests/dp/tasks/dp_o) | 심화·응용 | 심화로 선택한 대상 집합을 DP 상태에 포함한다 |
| 3 | [LeetCode 78 Subsets](https://leetcode.com/problems/subsets/) | 모든 부분집합 | `mask`를 `0`부터 `2ⁿ−1`까지 돌려 비트로 원소 선택 |
| 4 | [LeetCode 1239 Maximum Length of a Concatenated String with Unique Characters](https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/) | 문자 집합 | 문자열마다 알파벳 마스크를 만들어 겹치는지 `&`로 판정 |
| 5 | [LeetCode 2044 Count Number of Maximum Bitwise-OR Subsets](https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/) | 부분집합 + OR | 모든 부분집합의 OR을 구해 최댓값과 같은 개수 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
