# 연습문제 — 접미사 배열과 LCP

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11656 접미사 배열](https://www.acmicpc.net/problem/11656) | 접미사를 정렬해 출력 | 길이 1000이라 슬라이스를 정렬하면 된다. 접미사 배열이 무엇인지 확인하는 문제 |
| 2 | [LeetCode 718 Maximum Length of Repeated Subarray](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) | 두 수열의 가장 긴 공통 부분 배열 | `O(nm)` DP로 풀리고, 접미사 배열로도 푼다. 정수 리스트를 그대로 넣어 본다 |
| 3 | [백준 5582 공통 부분 문자열](https://www.acmicpc.net/problem/5582) | 두 문자열의 가장 긴 공통 부분 문자열 | 길이 4000이라 DP도 되지만 파이썬에서는 `longest_common_substring`이 훨씬 빠르다 |
| 4 | [백준 9248 Suffix Array](https://www.acmicpc.net/problem/9248) | 접미사 배열 + LCP 출력 | [solution.py](solution.py)의 `main()`이 같은 형태. 첫 칸의 `x`와 1부터 세는 위치 |
| 5 | [백준 11479 서로 다른 부분 문자열의 개수 2](https://www.acmicpc.net/problem/11479) | 서로 다른 부분 문자열 수 | `count_distinct_substrings`. 길이가 10⁶이라 파이썬에서는 시간이 빠듯하다 |
| 6 | [백준 1605 반복 부분문자열](https://www.acmicpc.net/problem/1605) | 가장 긴 반복 부분 문자열 | `max(lcp)`. 겹쳐도 되는지 문제에서 확인 |
| 7 | [백준 1701 Cubeness](https://www.acmicpc.net/problem/1701) | 두 번 이상 나오는 가장 긴 부분 문자열 | 같은 문제를 [Z 알고리즘](../z-algorithm/)으로 접미사마다 풀면 `O(n²)`, 접미사 배열이면 `O(n log² n)` |
| 8 | [백준 3033 가장 긴 문자열](https://www.acmicpc.net/problem/3033) | 가장 긴 반복 부분 문자열 (큰 입력) | 길이 20만. 해시 + 이진 탐색과 접미사 배열 두 풀이를 비교 |
| 9 | [백준 9249 최장 공통 부분 문자열](https://www.acmicpc.net/problem/9249) | 공통 부분 문자열 (큰 입력) | 길이 10만. 구분자와 "서로 다른 문자열에서 온 이웃" 조건. 부분 문자열 자체도 출력 |
| 10 | [LeetCode 1044 Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | 가장 긴 중복 부분 문자열 | 길이 3·10⁴. 해시 + 이진 탐색이 정석이지만 `longest_repeated_substring`도 된다 |
| 11 | [AtCoder ACL Practice I - Number of Substrings](https://atcoder.jp/contests/practice2/tasks/practice2_i) | 서로 다른 부분 문자열 수 | 접미사 배열 + LCP의 기본형. 답이 `n(n+1)/2` 근처까지 커져 32비트 정수를 쓰는 언어에서는 64비트가 필요하다 |
| 12 | [Codeforces 123D String](https://codeforces.com/problemset/problem/123/D) | 부분 문자열의 출현 횟수 제곱의 합 | 서로 다른 부분 문자열마다 `occ²`를 더한다. `lcp`를 스택으로 합쳐 구간별 계산 |

## 풀이 메모

- 1번은 슬라이스를 정렬하는 순진한 방법으로 풀어 놓고, [solution.py](solution.py)의 `suffix_array`로 같은 결과가 나오는지 비교해 보세요.
- 3번과 9번은 같은 문제이고 크기만 다릅니다. 3번은 DP, 9번은 접미사 배열이 필요합니다. 같은 입력에서 둘의 시간을 비교해 보세요.
- 6, 7, 8, 10번은 모두 "두 번 이상 나오는 가장 긴 부분 문자열"입니다. 해시 + 이진 탐색(길이 단조성)과 접미사 배열(`max(lcp)`) 두 풀이로 푸세요. 겹쳐서 나와도 되는지는 문제마다 다르니 지문을 확인하세요.
- 12번이 가장 어렵습니다. `lcp` 값을 스택(단조)으로 합쳐 "길이 `L` 이상으로 일치하는 접미사 구간"을 한꺼번에 처리하는 방법을 배웁니다.
