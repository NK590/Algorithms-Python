# 연습문제 — 라빈-카프 알고리즘

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — String Matching](https://cses.fi/problemset/task/1753) | 핵심 연습 | 해시 후보를 찾고 충돌을 검증한다 |
| 2 | [AtCoder — Who Says a Pun?](https://atcoder.jp/contests/abc141/tasks/abc141_e) | 핵심 연습 | 이분 탐색과 부분 문자열 해시를 결합한다 |
| 3 | [LeetCode 187 Repeated DNA Sequences](https://leetcode.com/problems/repeated-dna-sequences/) | 같은 길이 부분 문자열 | 길이 10의 모든 부분 문자열의 해시를 집합에 넣고 두 번 나온 것을 모은다 |
| 4 | [LeetCode 1044 Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | 이분 탐색 + 해시 | 가장 긴 중복 부분 문자열(겹쳐도 됨). `longest_repeated_substring_length`와 같은 틀에 문자열을 돌려줘야 한다 |
| 5 | [Codeforces 126B Password](https://codeforces.com/problemset/problem/126/B) | 테두리 | 접두사이자 접미사이면서 중간에도 나오는 가장 긴 부분 문자열. 접두사 해시로 `O(1)` 비교하거나 실패 함수로 해결 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
