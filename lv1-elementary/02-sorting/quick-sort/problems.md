# 연습문제 — 퀵 정렬

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 75 Sort Colors](https://leetcode.com/problems/sort-colors/) | 3분할 | 값이 0, 1, 2뿐인 배열을 한 번 훑어 정렬한다. 이 문서의 네덜란드 국기 분할(`_partition`)이 그대로 풀이다 |
| 2 | [백준 11004 K번째 수](https://www.acmicpc.net/problem/11004) | 퀵 셀렉트 | 정렬하지 않고 k번째 수를 구한다. N이 매우 크므로 `quick_select`의 평균 O(n)을 떠올리는 문제. 파이썬에서의 입력 속도와 메모리도 함께 신경 써야 한다 |
| 3 | [LeetCode 215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 퀵 셀렉트 / 힙 | k번째로 큰 값. 퀵 셀렉트(평균 O(n))와 크기 k짜리 힙(O(n log k)) 두 가지로 풀어 비교해 보자 |
| 4 | [LeetCode 912 Sort an Array](https://leetcode.com/problems/sort-an-array/) | 직접 구현 | 내장 정렬 없이 정렬을 구현하는 문제. 퀵 정렬은 입력에 같은 값이 많거나 정렬되어 있으면 느려지는 구현이 있으니, 무작위 기준값과 3분할이 왜 필요한지 확인할 수 있다 |

## 풀이 메모

- 1번은 기준값이 1인 `_partition`을 한 번만 호출하면 됩니다. `lt`, `gt` 경계를 직접 그려 보세요.
- 2번은 `quick_select(arr, k - 1)`입니다. (문제의 K는 1부터 센다)
