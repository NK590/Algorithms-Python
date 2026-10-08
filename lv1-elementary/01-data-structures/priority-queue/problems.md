# 연습문제 — 우선순위 큐

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1927 최소 힙](https://www.acmicpc.net/problem/1927) | 기본형 | 양수는 넣고 0이면 가장 작은 값을 꺼낸다. [solution.py](solution.py)의 `main()`이 그대로 풀이다 |
| 2 | [백준 11279 최대 힙](https://www.acmicpc.net/problem/11279) | 최대 힙 | `heapq`에 값에 `-`를 붙여 넣는다 |
| 3 | [백준 11286 절댓값 힙](https://www.acmicpc.net/problem/11286) | 정렬 기준 | `(절댓값, 값)` 튜플로 넣으면 절댓값이 같을 때 작은 수가 먼저 나온다 |
| 4 | [백준 1715 카드 정렬하기](https://www.acmicpc.net/problem/1715) | 그리디 + 힙 | 가장 작은 두 묶음을 합치는 일을 반복한다. 매번 최솟값 두 개가 필요해서 힙이 어울린다 |
| 5 | [백준 1655 가운데를 말해요](https://www.acmicpc.net/problem/1655) | 중앙값 유지 | 두 개의 힙으로 중앙값을 O(log n)에 구한다 (`RunningMedian`). 짝수 개일 때는 작은 쪽을 말한다 |
| 6 | [LeetCode 215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 상위 k개 | 크기 k의 최소 힙만 유지한다 (`kth_largest`) |
| 7 | [LeetCode 23 Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | K개 합치기 | 각 리스트의 맨 앞만 힙에 두고 가장 작은 것을 꺼낸다 (`merge_sorted_lists`) |

## 풀이 메모

- 1~3번은 입력이 10만 줄이라 `sys.stdin.readline`을 쓰세요. ([빠른 입출력](../../../lv0-basics/04-io-and-complexity/fast-io/))
- 5번은 [solution.py](solution.py)의 `RunningMedian`이 이 문제의 아이디어 그대로입니다.
