# 연습문제 — 배낭 문제

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 12865 평범한 배낭](https://www.acmicpc.net/problem/12865) | 0/1 배낭 | 가장 기본형. N ≤ 100, K ≤ 100,000. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 2293 동전 1](https://www.acmicpc.net/problem/2293) | 동전 (조합의 수) | 동전을 바깥 반복으로 돌려 순서를 무시한다. `count_coin_ways` |
| 3 | [백준 2294 동전 2](https://www.acmicpc.net/problem/2294) | 동전 (최소 개수) | 만들 수 없으면 -1. `min_coins` |
| 4 | [LeetCode 322 Coin Change](https://leetcode.com/problems/coin-change/) | 동전 (최소 개수) | 그리디가 틀리는 동전 체계 (`[1, 3, 4]`로 6) |
| 5 | [LeetCode 416 Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 부분집합의 합 | 전체 합의 절반을 만들 수 있는가. `can_partition_equal` |
| 6 | [LeetCode 518 Coin Change II](https://leetcode.com/problems/coin-change-ii/) | 동전 (조합의 수) | 2번과 같은 문제 |
| 7 | [백준 7579 앱](https://www.acmicpc.net/problem/7579) | 상태 뒤집기 | 무게(메모리)가 크고 가치(비용)가 작다. `dp[비용]` = 확보한 메모리의 최댓값으로 뒤집는다 |
| 8 | [백준 12920 평범한 배낭 2](https://www.acmicpc.net/problem/12920) | 개수 제한 | 물건마다 여러 개. 이진 분할로 0/1로 바꾼다. `knapsack_bounded` |
| 9 | [LeetCode 494 Target Sum](https://leetcode.com/problems/target-sum/) | 부분집합 + 변환 | `+`/`-`를 붙여 합이 target. 부분집합의 합의 경우의 수로 바꾼다 |

## 풀이 메모

- 1번에서 갱신 방향을 일부러 거꾸로 해 보고, 같은 물건이 여러 번 쓰여 정답이 커지는 것을 확인하세요.
- 2번과 6번은 같은 문제입니다. 동전과 금액 중 무엇이 바깥 반복인지가 조합과 순열을 가릅니다. ([테스트](test_solution.py)의 `test_coin_problems_match_independent_methods`)
- 7번은 한도(메모리)가 아니라 **비용**을 상태로 두는 발상의 전환이 필요합니다. 비용 합의 상한이 작아야 합니다.
- 9번은 "양수로 만든 부분집합의 합 P"와 "음수로 만든 부분집합의 합 N"이 `P − N = target`, `P + N = total`을 만족하므로 `P = (total + target) / 2`인 부분집합의 수를 세는 문제가 됩니다.
