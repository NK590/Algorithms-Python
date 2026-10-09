# 연습문제 — Z 알고리즘

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Z Algorithm](https://judge.yosupo.jp/problem/zalgorithm) | 핵심 연습 | 접두사와 각 접미사의 LCP 길이를 구한다 |
| 2 | [CSES — String Matching](https://cses.fi/problemset/task/1753) | 핵심 연습 | 패턴과 본문을 구분자로 연결해 매칭한다 |
| 3 | [LeetCode 28 Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | 문자열 찾기 | `z_search`의 가장 기본형. 내장 `find`와 결과를 비교해 보기 |
| 4 | [LeetCode 459 Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) | 완전한 반복 | 최소 주기 `p`가 `n`의 약수이고 `p < n`인가 |
| 5 | [LeetCode 214 Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | 접두사 회문 | `s + 구분자 + reverse(s)`의 Z에서 가장 긴 "접두사 회문"을 찾는다 |
| 6 | [LeetCode 2223 Sum of Scores of Built Strings](https://leetcode.com/problems/sum-of-scores-of-built-strings/) | `sum(z)` | 모든 접미사의 점수가 곧 `z` 값. 한 줄 문제이지만 Z의 정의를 정확히 이해해야 한다 |
| 7 | [Codeforces 126B Password](https://codeforces.com/problemset/problem/126/B) | 테두리가 중간에도 | 접두사이자 접미사이면서 **가운데에도** 나오는 가장 긴 조각. 테두리 + 앞쪽 위치의 `z` 최댓값 |
| 8 | [Codeforces 432D Prefixes and Suffixes](https://codeforces.com/problemset/problem/432/D) | 테두리별 출현 횟수 | 모든 테두리의 길이와 문자열 안 출현 횟수를 함께. `prefix_occurrence_counts` |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
