# 연습문제 — 세그먼트 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10868 최솟값](https://www.acmicpc.net/problem/10868) | 정적 구간 최솟값 | 갱신이 없다. `SegmentTree(values, min, inf)`. 희소 배열로도 풀린다 |
| 2 | [백준 2357 최솟값과 최댓값](https://www.acmicpc.net/problem/2357) | 최솟값 + 최댓값 | 트리 두 개. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 3 | [LeetCode 307 Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 점 갱신 + 구간 합 | 가장 기본적인 점 갱신. 합은 펜윅 트리로도 가능 |
| 4 | [백준 14438 수열과 쿼리 17](https://www.acmicpc.net/problem/14438) | 점 갱신 + 최솟값 | `update`와 `query`를 섞어 쓰는 기본형 |
| 5 | [백준 11505 구간 곱 구하기](https://www.acmicpc.net/problem/11505) | 곱 mod p | 항등원 1. 0이 있을 수 있어서 역원으로 나누는 방법은 안 되고 트리로 곱한다 |
| 6 | [백준 2517 달리기](https://www.acmicpc.net/problem/2517) | 순위 | 값을 인덱스로 하는 개수 트리(합). 펜윅 트리로도 풀리니 두 가지를 비교 |
| 7 | [백준 16993 연속합과 쿼리](https://www.acmicpc.net/problem/16993) | 최대 연속 부분 합 | `(합, 접두, 접미, 최대)` 노드와 비가환 결합. `max_subarray_tree` |
| 8 | [백준 14476 최대공약수 하나 빼기](https://www.acmicpc.net/problem/14476) | gcd | 한 수를 빼고 나머지 gcd. 접두사/접미사 gcd 또는 구간 gcd 트리 |
| 9 | [백준 2336 굴러가는 박스](https://www.acmicpc.net/problem/2336) | 정렬 + 트리 | 세 번의 시험 성적 중 한 번도 다른 사람에게 지지 않은 사람. 한 시험으로 정렬하고 다른 시험의 순위로 최솟값 트리를 쓴다 |
| 10 | [LeetCode 699 Falling Squares](https://leetcode.com/problems/falling-squares/) | 구간 최댓값 + 구간 대입 | 떨어지는 정사각형의 높이. 구간 갱신이 필요해 [느리게 갱신되는 세그먼트 트리](../lazy-propagation/) 연습으로 이어진다 |
| 11 | [LeetCode 2407 Longest Increasing Subsequence II](https://leetcode.com/problems/longest-increasing-subsequence-ii/) | 트리 위의 DP | 값 구간 `[x − k, x − 1]`의 최대 길이를 트리에서 질의하고 `x` 위치를 갱신 |

## 풀이 메모

- 1번과 2번은 `SegmentTree(values, min, float("inf"))`와 `SegmentTree(values, max, float("-inf"))`로 푸는 기본형입니다. 닫힌 구간 `[a, b]`(1부터)는 `query(a − 1, b)`입니다. [테스트](test_solution.py)가 모든 작은 입력에서 순진한 계산과 비교합니다.
- 5번은 모듈러가 소수이고 구간에 0이 있을 수 있으니 역원으로 나누는 방법(구간 곱의 누적곱을 이용)은 실패합니다. 트리로 직접 곱하세요.
- 7번에서 항등원을 `(0, 0, 0, 0)`으로 두면 전부 음수인 구간에서 틀립니다([README](README.md#6-자주-하는-실수)).
- 9번과 11번은 "정렬해서 한 차원을 없애고, 다른 차원을 트리 인덱스로 쓴다"는 같은 사고방식입니다.
- 6번은 [펜윅 트리](../fenwick-tree/)의 연습문제와 겹칩니다. 합이면 펜윅 트리, 그 외 연산이면 세그먼트 트리라는 선택 기준을 두 구현의 속도로 비교해 보세요.
