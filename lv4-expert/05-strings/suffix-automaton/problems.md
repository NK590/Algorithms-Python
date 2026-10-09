# 연습문제 — 접미사 자동자

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Number of Substrings](https://judge.yosupo.jp/problem/number_of_substrings) | 핵심 연습 | 상태별 길이 차이로 서로 다른 부분 문자열을 센다 |
| 2 | [CSES 2105 Distinct Substrings](https://cses.fi/problemset/task/2105) | 서로 다른 부분 문자열의 수 | `distinct`. 접미사 배열 + LCP 풀이와 비교 |
| 3 | [CSES 2103 Counting Patterns](https://cses.fi/problemset/task/2103) | 패턴 여러 개의 출현 횟수 | `count_occurrences`. 상태별 `cnt` 전파 |
| 4 | [CSES 2104 Pattern Positions](https://cses.fi/problemset/task/2104) | 패턴의 처음 나오는 위치 | `first_occurrence`. 복제가 원본의 `first_end`를 물려받는 이유 |
| 5 | [SPOJ LCS - Longest Common Substring](https://www.spoj.com/problems/LCS/) | 두 문자열의 최장 공통 부분 문자열 | `longest_common_substring_with`. 링크를 따라 올라가며 길이를 줄이는 부분 |
| 6 | [SPOJ SUBLEX - Lexicographical Substring Search](https://www.spoj.com/problems/SUBLEX/) | 서로 다른 부분 문자열의 사전순 `k`번째 (여러 질의) | `kth_distinct_substring`. 질의가 많으면 `paths`를 한 번만 계산해 재사용 |
| 7 | [SPOJ LCS2 - Longest Common Substring II](https://www.spoj.com/problems/LCS2/) | 최대 10개 문자열의 최장 공통 부분 문자열 | `longest_common_substring_of_many`. 링크 위로의 전파가 핵심 |
| 8 | [SPOJ NSUBSTR - Substrings](https://www.spoj.com/problems/NSUBSTR/) | 길이 `i`인 부분 문자열의 최대 출현 횟수 (모든 `i`) | `best[len[v]] = max(cnt[v])` 뒤 길이를 줄이며 최댓값 전파 |
| 9 | [Codeforces 235C Cyclical Quest](https://codeforces.com/problemset/problem/235/C) | 패턴의 모든 순환 이동이 본문에 몇 번 나오나 | 패턴을 두 번 이어 붙여 읽으며 맞춘 길이를 패턴 길이로 유지, 중복 순환 이동은 상태 표시로 한 번만 센다 |
| 10 | [Codeforces 616F Expensive Strings](https://codeforces.com/problemset/problem/616/F) | 비용이 붙은 여러 문자열에서 `(s의 길이) × Σ cᵢ·(tᵢ에서 s의 출현 횟수)`의 최댓값 | 여러 문자열의 일반화 자동자 + 링크 트리 위 합 전파. 상태마다 `len × (비용 합)`의 최댓값 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
