# 연습문제 — 매내처 알고리즘

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Longest Palindrome](https://cses.fi/problemset/task/1111) | 핵심 연습 | 홀수·짝수 중심의 반지름 배열에서 가장 긴 회문 구간을 복원한다 |
| 2 | [LeetCode 5 Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | 가장 긴 회문 | 길이 1000이라 `O(n²)` 넓히기로도 풀린다. 매내처와 결과를 비교하는 기준 문제 |
| 3 | [LeetCode 647 Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | 회문 개수 | `sum(odd) + sum(even)`. 위치가 다르면 같은 내용이어도 따로 센다 |
| 4 | [LeetCode 132 Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) | 최소 분할 | `min_palindrome_cuts`. 회문 판정 표 + 1차원 DP |
| 5 | [LeetCode 1960 Maximum Product of the Length of Two Palindromic Substrings](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-substrings/) | 겹치지 않는 두 회문 | 각 위치까지(부터) 가장 긴 홀수 회문을 반지름 배열에서 퍼뜨려 구한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
