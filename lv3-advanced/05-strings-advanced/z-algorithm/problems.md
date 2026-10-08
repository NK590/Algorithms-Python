# 연습문제 — Z 알고리즘

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 28 Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | 문자열 찾기 | `z_search`의 가장 기본형. 내장 `find`와 결과를 비교해 보기 |
| 2 | [백준 16916 부분 문자열](https://www.acmicpc.net/problem/16916) | 부분 문자열 여부 | 긴 입력(100만)에서 패턴이 있는지만 묻는다. 한 번 찾으면 끝 |
| 3 | [백준 1786 찾기](https://www.acmicpc.net/problem/1786) | 모든 위치 | 개수와 모든 시작 위치(1부터). [solution.py](solution.py)의 `main()`이 같은 형태. 공백이 있는 줄을 읽는 법 |
| 4 | [LeetCode 459 Repeated Substring Pattern](https://leetcode.com/problems/repeated-substring-pattern/) | 완전한 반복 | 최소 주기 `p`가 `n`의 약수이고 `p < n`인가 |
| 5 | [백준 4354 문자열 제곱](https://www.acmicpc.net/problem/4354) | 반복 횟수 | `n % p == 0`일 때만 `n / p`번 반복, 아니면 1. 입력은 `.`이 나올 때까지 여러 줄 |
| 6 | [백준 1305 광고](https://www.acmicpc.net/problem/1305) | 최소 주기 | 전광판이 돌며 보이는 문자열에서 광고의 최소 길이. `z[p] == n − p`인 가장 작은 `p` |
| 7 | [LeetCode 214 Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | 접두사 회문 | `s + 구분자 + reverse(s)`의 Z에서 가장 긴 "접두사 회문"을 찾는다 |
| 8 | [LeetCode 2223 Sum of Scores of Built Strings](https://leetcode.com/problems/sum-of-scores-of-built-strings/) | `sum(z)` | 모든 접미사의 점수가 곧 `z` 값. 한 줄 문제이지만 Z의 정의를 정확히 이해해야 한다 |
| 9 | [백준 10266 시계 사진 찾기](https://www.acmicpc.net/problem/10266) | 원형 일치 | 각도 집합을 길이 36만의 0/1 배열로 만들어 `T + T`에서 `P`를 찾는다 |
| 10 | [Codeforces 126B Password](https://codeforces.com/problemset/problem/126/B) | 테두리가 중간에도 | 접두사이자 접미사이면서 **가운데에도** 나오는 가장 긴 조각. 테두리 + 앞쪽 위치의 `z` 최댓값 |
| 11 | [백준 13713 문자열과 쿼리](https://www.acmicpc.net/problem/13713) | 뒤집은 Z | 접두사 대신 **접미사**와의 공통 길이를 묻는다. 뒤집은 문자열의 Z 배열 |
| 12 | [Codeforces 432D Prefixes and Suffixes](https://codeforces.com/problemset/problem/432/D) | 테두리별 출현 횟수 | 모든 테두리의 길이와 문자열 안 출현 횟수를 함께. `prefix_occurrence_counts` |

## 풀이 메모

- 1번을 풀고 나면 내장 `str.find`와 시간을 비교해 보세요. 파이썬에서 단순 문자열 찾기는 내장이 빠르다는 것, Z가 필요한 곳은 `z` 배열 자체가 답의 재료일 때라는 것을 확인하는 문제입니다.
- 5번과 6번은 같은 `smallest_period`로 풀립니다. 다만 5번은 "완전한 반복"이라 `n % p == 0`을 확인해야 하고, 6번은 마지막 반복이 잘려도 되므로 확인하지 않습니다.
- 10번은 테두리 `z[i] == n − i`를 긴 것부터(작은 `i`부터) 보면서, 그보다 **앞선** 위치 `j < i`에 `z[j] ≥ n − i`인 것이 있는지 확인하면 됩니다. 앞선 `j`의 일치는 `j + (n − i) < n`이라 접미사 자리가 아닌 가운데에 있기 때문입니다. `abcabcab`처럼 작은 예로 직접 확인해 보세요.
- 11번과 12번이 Z의 응용 능력을 가장 잘 보여 줍니다. 11번은 "뒤집는다", 12번은 "`z` 값을 누적한다"가 핵심입니다.
