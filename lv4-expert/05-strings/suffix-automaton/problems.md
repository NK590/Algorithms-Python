# 연습문제 — 접미사 자동자

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES 2105 Distinct Substrings](https://cses.fi/problemset/task/2105) | 서로 다른 부분 문자열의 수 | `distinct`. 접미사 배열 + LCP 풀이와 비교 |
| 2 | [Library Checker - Number of Substrings](https://judge.yosupo.jp/problem/number_of_substrings) | 서로 다른 부분 문자열의 수 (`n ≤ 5·10⁵`) | [solution.py](solution.py)의 `main()`이 같은 형태. 큰 입력에서 파이썬 속도 가늠 |
| 3 | [CSES 2103 Counting Patterns](https://cses.fi/problemset/task/2103) | 패턴 여러 개의 출현 횟수 | `count_occurrences`. 상태별 `cnt` 전파 |
| 4 | [CSES 2104 Pattern Positions](https://cses.fi/problemset/task/2104) | 패턴의 처음 나오는 위치 | `first_occurrence`. 복제가 원본의 `first_end`를 물려받는 이유 |
| 5 | [SPOJ LCS - Longest Common Substring](https://www.spoj.com/problems/LCS/) | 두 문자열의 최장 공통 부분 문자열 | `longest_common_substring_with`. 링크를 따라 올라가며 길이를 줄이는 부분 |
| 6 | [SPOJ SUBLEX - Lexicographical Substring Search](https://www.spoj.com/problems/SUBLEX/) | 서로 다른 부분 문자열의 사전순 `k`번째 (여러 질의) | `kth_distinct_substring`. 질의가 많으면 `paths`를 한 번만 계산해 재사용 |
| 7 | [SPOJ LCS2 - Longest Common Substring II](https://www.spoj.com/problems/LCS2/) | 최대 10개 문자열의 최장 공통 부분 문자열 | `longest_common_substring_of_many`. 링크 위로의 전파가 핵심 |
| 8 | [SPOJ NSUBSTR - Substrings](https://www.spoj.com/problems/NSUBSTR/) | 길이 `i`인 부분 문자열의 최대 출현 횟수 (모든 `i`) | `best[len[v]] = max(cnt[v])` 뒤 길이를 줄이며 최댓값 전파 |
| 9 | [Codeforces 235C Cyclical Quest](https://codeforces.com/problemset/problem/235/C) | 패턴의 모든 순환 이동이 본문에 몇 번 나오나 | 패턴을 두 번 이어 붙여 읽으며 맞춘 길이를 패턴 길이로 유지, 중복 순환 이동은 상태 표시로 한 번만 센다 |
| 10 | [Codeforces 616F Expensive Strings](https://codeforces.com/problemset/problem/616/F) | 비용이 붙은 여러 문자열에서 `(s의 길이) × Σ cᵢ·(tᵢ에서 s의 출현 횟수)`의 최댓값 | 여러 문자열의 일반화 자동자 + 링크 트리 위 합 전파. 상태마다 `len × (비용 합)`의 최댓값 |

## 풀이 메모

- 1번과 2번은 같은 문제입니다. 둘 다 접미사 배열 + LCP로도 풀리므로 [Lv3 접미사 배열](../../../lv3-advanced/05-strings-advanced/suffix-array-lcp/)의 `count_distinct_substrings`와 값을 비교해 보세요. 이 저장소의 두 구현이 무작위 문자열에서 같은 값을 냅니다.
- 3번과 4번은 *본문 하나, 패턴 여러 개*. 자동자를 한 번 만들고 패턴마다 `O(|패턴|)`로 답합니다. `cnt`는 첫 질의에서 한 번 계산해 캐시됩니다.
- 5번~7번은 공통 부분 문자열의 변주입니다. 7번은 문자열이 10개라 문자열마다 "각 상태에서 맞춘 최대 길이"를 구해 링크를 따라 올린 뒤 상태별 최솟값을 취합니다.
- 8번은 `cnt[v]`와 `len[v]`만으로 풀립니다. 상태 `v`의 문자열 길이는 `len[link[v]] + 1 .. len[v]`인데 가장 긴 것의 `cnt`가 같은 상태의 모든 문자열의 `cnt`와 같으므로 `len[v]`에서만 갱신하고 짧은 길이는 큰 길이의 값을 물려받으면 됩니다 (`best[i] = max(best[i], best[i + 1])`).
- 9번과 10번은 자동자를 부품으로 쓰는 응용입니다. 9번은 순환 이동 패턴 길이만큼을 하나씩 따라가며 *한 상태를 중복으로 세지 않도록* 방문 표시를 둡니다.
