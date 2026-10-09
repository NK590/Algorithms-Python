# 연습문제 — 접미사 배열과 LCP

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Suffix Array](https://judge.yosupo.jp/problem/suffixarray) | 핵심 연습 | 접미사 인덱스를 사전순으로 정렬한다 |
| 2 | [CSES — Distinct Substrings](https://cses.fi/problemset/task/2105) | 핵심 연습 | LCP가 중복 부분 문자열을 얼마나 제거하는지 계산한다 |
| 3 | [LeetCode 718 Maximum Length of Repeated Subarray](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) | 두 수열의 가장 긴 공통 부분 배열 | `O(nm)` DP로 풀리고, 접미사 배열로도 푼다. 정수 리스트를 그대로 넣어 본다 |
| 4 | [LeetCode 1044 Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | 가장 긴 중복 부분 문자열 | 길이 3·10⁴. 해시 + 이진 탐색이 정석이지만 `longest_repeated_substring`도 된다 |
| 5 | [AtCoder ACL Practice I - Number of Substrings](https://atcoder.jp/contests/practice2/tasks/practice2_i) | 서로 다른 부분 문자열 수 | 접미사 배열 + LCP의 기본형. 답이 `n(n+1)/2` 근처까지 커져 32비트 정수를 쓰는 언어에서는 64비트가 필요하다 |
| 6 | [Codeforces 123D String](https://codeforces.com/problemset/problem/123/D) | 부분 문자열의 출현 횟수 제곱의 합 | 서로 다른 부분 문자열마다 `occ²`를 더한다. `lcp`를 스택으로 합쳐 구간별 계산 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
