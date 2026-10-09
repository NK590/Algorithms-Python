# 연습문제 — KMP 알고리즘

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — String Matching](https://cses.fi/problemset/task/1753) | 핵심 연습 | 실패 함수로 일치한 접두 정보를 재사용한다 |
| 2 | [CSES — Finding Borders](https://cses.fi/problemset/task/1732) | 핵심 연습 | 접두사이면서 접미사인 길이를 따라간다 |
| 3 | [CSES — Finding Periods](https://cses.fi/problemset/task/1733) | 핵심 연습 | 전체 문자열을 덮는 주기를 검사한다 |
| 4 | [LeetCode 28 Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | 기본형 | 첫 등장 위치. 내장 `find`로도 풀리지만 `kmp_search`의 첫 원소와 같다 |
| 5 | [LeetCode 459 Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) | 반복 단위 | `n − failure[n−1]`이 `n`을 나누는지. `smallest_period`가 `n`보다 작으면 참 |
| 6 | [LeetCode 1392 Longest Happy Prefix](https://leetcode.com/problems/longest-happy-prefix/) | 테두리 | 접두사이자 접미사인 가장 긴 부분 = `failure[n−1]` 그 자체 |
| 7 | [LeetCode 214 Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | 실패 함수 응용 | `s + '#' + reverse(s)`의 실패 함수 마지막 값이 가장 긴 회문 접두사의 길이 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
