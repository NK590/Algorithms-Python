# 연습문제 — 분할 정복

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1074 Z](https://www.acmicpc.net/problem/1074) | 사분면 재귀 | 칸의 방문 번호. 사분면마다 앞선 칸 수를 더한다. `z_order_index`. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 1992 쿼드트리](https://www.acmicpc.net/problem/1992) | 사분면 재귀 | 모두 같으면 한 글자, 아니면 괄호. `quad_tree` |
| 3 | [백준 1780 종이의 개수](https://www.acmicpc.net/problem/1780) | 9등분 재귀 | -1, 0, 1로 채워진 종이를 같은 수가 되도록 9등분. `count_uniform_regions` |
| 4 | [백준 2630 색종이 만들기](https://www.acmicpc.net/problem/2630) | 4등분 재귀 | 흰색/파란색 정사각형의 개수 |
| 5 | [LeetCode 53 Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | 가운데를 걸침 | 분할 정복으로도 풀어 보고 카데인과 비교. `max_subarray_dc` |
| 6 | [백준 1517 버블 소트](https://www.acmicpc.net/problem/1517) | 역전 쌍 | 버블 정렬의 교환 횟수 = 역전 쌍의 수. n ≤ 500,000이라 병합 정렬 방식. `count_inversions_dc` |
| 7 | [LeetCode 493 Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | 역전 쌍 변형 | `a[i] > 2·a[j]`인 쌍. 합치기 전에 두 포인터로 먼저 센다 |
| 8 | [백준 2261 가장 가까운 두 점](https://www.acmicpc.net/problem/2261) | 가장 가까운 점 쌍 | 띠 안에서 y 순으로 비교. 같은 점이 있으면 0. `closest_pair_squared` |
| 9 | [LeetCode 215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 분할 + 한쪽만 | 퀵 선택. 한쪽만 재귀하여 평균 O(n) |

## 풀이 메모

- 1~4번은 모두 "같은 모양으로 4등분(9등분)" 재귀입니다. 기저 조건(크기 1 또는 모두 같음)과 4등분의 순서를 문제 정의와 맞추세요.
- 6번은 **같은 값을 역전으로 세지 않는** 비교(`<=`)가 중요합니다. 정렬이 안정적이어야 하는 이유와 같습니다.
- 8번은 구현량이 많습니다. 먼저 O(n²)로 풀어 정답을 확인하고, 분할 정복 버전과 임의 입력으로 비교하세요. (이 폴더의 [테스트](test_solution.py)도 같은 방법입니다.)
- 9번은 두 쪽을 모두 풀지 않고 **필요한 쪽만** 재귀하는 점에서 이분 탐색과 닮았습니다. 평균 O(n).
