# 연습문제 — 라빈-카프 알고리즘

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 16916 부분 문자열](https://www.acmicpc.net/problem/16916) | 기본형 | `S`에 `P`가 있는가. 롤링 해시로 풀어 보고, 실제 비교로 확인하는 부분의 효과를 느낀다. [solution.py](solution.py)의 `main()`이 비슷한 형태 |
| 2 | [LeetCode 187 Repeated DNA Sequences](https://leetcode.com/problems/repeated-dna-sequences/) | 같은 길이 부분 문자열 | 길이 10의 모든 부분 문자열의 해시를 집합에 넣고 두 번 나온 것을 모은다 |
| 3 | [백준 11585 속타는 저녁 메뉴](https://www.acmicpc.net/problem/11585) | 원형 매칭 | 본문을 두 번 이어 붙이고 패턴과 같은 위치 수를 센다. 해시와 KMP 두 방법 모두 가능 |
| 4 | [AtCoder ABC141 E - Who Says a Pun?](https://atcoder.jp/contests/abc141/tasks/abc141_e) | 겹치지 않는 반복 | 길이 `L`이 가능한가를 이분 탐색하되 **겹치지 않아야** 한다는 조건을 `i + L ≤ j`로 확인 |
| 5 | [LeetCode 1044 Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | 이분 탐색 + 해시 | 가장 긴 중복 부분 문자열(겹쳐도 됨). `longest_repeated_substring_length`와 같은 틀에 문자열을 돌려줘야 한다 |
| 6 | [백준 3033 가장 긴 문자열](https://www.acmicpc.net/problem/3033) | 이분 탐색 + 해시 | `L`이 20만이라 `O(n log n)`이 필요. 실제 문자열 비교 없이 해시만 믿는다면 충돌 위험을 줄이는 방법(큰 소수, 이중 해시)을 고민 |
| 7 | [백준 13275 가장 긴 팰린드롬 부분 문자열](https://www.acmicpc.net/problem/13275) | 회문 + 해시 | 앞에서 읽은 접두사 해시와 뒤에서 읽은 해시를 비교한다. 매내처 알고리즘의 대안 |
| 8 | [Codeforces 126B Password](https://codeforces.com/problemset/problem/126/B) | 테두리 | 접두사이자 접미사이면서 중간에도 나오는 가장 긴 부분 문자열. 접두사 해시로 `O(1)` 비교하거나 실패 함수로 해결 |

## 풀이 메모

- 1번과 3번은 [KMP](../kmp/)로도 풀립니다. 같은 문제를 두 방법으로 풀어 비교해 보세요.
- 4번, 5번, 6번은 같은 틀입니다: **길이를 이분 탐색** → 각 길이에서 **해시를 집합에 넣고 중복 검사**. [solution.py](solution.py)의 `has_repeated_substring`이 그 판정 함수입니다. 4번은 겹침을 허용하지 않으므로 같은 해시가 나온 위치들의 거리를 따로 확인해야 합니다.
- 6번과 같은 큰 입력에서는 `has_repeated_substring`이 해시마다 위치 목록을 저장하느라 메모리와 시간이 큽니다. 충돌 확률이 낮은 큰 `mod`에서는 위치 목록 대신 해시만 `set`에 넣어도 됩니다(확률적 풀이).
- 해시 풀이의 정답이 틀리는 주된 원인은 고정된 `base`/`mod`(안티 해시 테스트)와 글자 값을 0으로 매긴 것입니다. [README](README.md#6-자주-하는-실수)의 목록을 확인하세요.
- 8번은 해시로도 풀리지만 [Z 알고리즘](../../../lv3-advanced/05-strings-advanced/z-algorithm/)이나 KMP의 실패 함수가 더 깔끔합니다.
