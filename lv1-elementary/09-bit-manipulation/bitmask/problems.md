# 연습문제 — 비트마스크

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11723 집합](https://www.acmicpc.net/problem/11723) | 집합 연산 | add / remove / check / toggle / all / empty. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 78 Subsets](https://leetcode.com/problems/subsets/) | 모든 부분집합 | `mask`를 `0`부터 `2ⁿ−1`까지 돌려 비트로 원소 선택 |
| 3 | [백준 1182 부분수열의 합](https://www.acmicpc.net/problem/1182) | 부분집합 합 | `count_subsets_with_sum`. 공집합을 세지 않는 것에 주의 (`S = 0`) |
| 4 | [LeetCode 1239 Maximum Length of a Concatenated String with Unique Characters](https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/) | 문자 집합 | 문자열마다 알파벳 마스크를 만들어 겹치는지 `&`로 판정 |
| 5 | [LeetCode 2044 Count Number of Maximum Bitwise-OR Subsets](https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/) | 부분집합 + OR | 모든 부분집합의 OR을 구해 최댓값과 같은 개수 |
| 6 | [백준 1987 알파벳](https://www.acmicpc.net/problem/1987) | 방문 집합 | 지나온 알파벳을 마스크 하나에 담고 DFS. `set`/리스트보다 빠르다 |
| 7 | [백준 14889 스타트와 링크](https://www.acmicpc.net/problem/14889) | k개 조합 | `masks_with_k_bits`로 팀 구성을 모두 보고, 0번을 팀 A에 고정해 대칭을 줄인다 (`min_team_difference`) |
| 8 | [백준 1062 가르침](https://www.acmicpc.net/problem/1062) | k개 선택 | 배울 글자 K개를 모두 고르며 단어마다 필요한 글자 마스크와 비교 |

## 풀이 메모

- 1번은 가장 기본형입니다. `1..20`을 비트 `1..20`에 대응시키고 `all`은 `((1 << 21) − 2)`처럼 비트 0을 비웁니다. 입력이 많으니 빠른 입력을 쓰세요. ([빠른 입출력](../../../lv0-basics/04-io-and-complexity/fast-io/))
- 3번은 `S = 0`일 때 공집합(합 0)을 세면 안 됩니다. 이 폴더의 테스트가 `count_subsets_with_sum([1, 2], 0) == 0`으로 확인합니다.
- 7번과 8번은 전체 `2ⁿ`을 돌면서 켜진 비트 수를 걸러내는 방법과 `masks_with_k_bits`로 바로 생성하는 방법을 비교해 보세요.
- 비트로 상태를 압축해 DP까지 가는 것은 Lv2의 [비트마스크 DP](../../../lv2-intermediate/04-dynamic-programming/bitmask-dp/)입니다.
