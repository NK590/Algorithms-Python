# 연습문제 — 구간 DP

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10942 팰린드롬?](https://www.acmicpc.net/problem/10942) | 팰린드롬 표 | 구간 `[s, e]`가 팰린드롬인지 질의가 많다. `palindrome_table`을 한 번 만들어 O(1) 응답 |
| 2 | [LeetCode 516 Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | 양 끝 | `longest_palindromic_subsequence` |
| 3 | [백준 11066 파일 합치기](https://www.acmicpc.net/problem/11066) | 구간 분할 | 인접한 파일끼리만 합친다. K ≤ 500, 테스트 케이스 여러 개. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다. 크누스 최적화도 가능 |
| 4 | [백준 11049 행렬 곱셈 순서](https://www.acmicpc.net/problem/11049) | 구간 분할 | 최소 곱셈 횟수. `matrix_chain_order` |
| 5 | [LeetCode 312 Burst Balloons](https://leetcode.com/problems/burst-balloons/) | 마지막을 기준 | "마지막에 터뜨릴 풍선"으로 뒤집기. `burst_balloons` |
| 6 | [LeetCode 1130 Minimum Cost Tree From Leaf Values](https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/) | 구간 분할 | 구간을 둘로 나누고 각 구간의 최댓값의 곱을 더한다 |
| 7 | [백준 1509 팰린드롬 분할](https://www.acmicpc.net/problem/1509) | 팰린드롬 + DP | 문자열을 최소 개수의 팰린드롬으로 분할. `palindrome_table` 위에서 1차원 DP |
| 8 | [백준 2315 가로등 끄기](https://www.acmicpc.net/problem/2315) | 구간 확장 | 이미 끈 구간 `[l, r]`에서 왼쪽 또는 오른쪽으로 한 칸 확장. 마지막 위치(왼쪽 끝/오른쪽 끝)를 상태에 포함 |

## 풀이 메모

- 3번은 CPython에서 시간이 빠듯합니다(K = 500이면 한 케이스에 2초대). PyPy3로 제출하거나 크누스 최적화(`opt` 배열)를 적용하세요.
- 5번이 구간 DP의 핵심 사고법을 담고 있습니다. "처음 터뜨릴 것"으로 나누려 하면 막히고, "마지막"으로 뒤집으면 풀립니다.
- 3번과 [대표 그리디 유형](../../../lv1-elementary/07-algorithm-paradigms/greedy-patterns/)의 "카드 정렬하기"를 비교해 보세요. **인접해야 하느냐**에 따라 DP와 그리디가 갈립니다. (이 폴더의 [테스트](test_solution.py) `test_adjacent_merging_differs_from_free_merging`)
- 7번은 구간 DP로 만든 표를 재료로 쓰는 2단계 문제입니다.
