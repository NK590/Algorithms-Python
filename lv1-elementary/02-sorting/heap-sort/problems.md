# 연습문제 — 힙 정렬

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1927 최소 힙](https://www.acmicpc.net/problem/1927) | 힙 기본 | 힙에 넣고 최솟값을 꺼내는 연산을 `heapq`로 해 본다. 힙 정렬이 쓰는 두 연산의 실전 형태 |
| 2 | [백준 11279 최대 힙](https://www.acmicpc.net/problem/11279) | 최대 힙 | `heapq`는 최소 힙뿐이라 값에 `-`를 붙여 넣어 최대 힙처럼 쓴다. 이 문서의 최대 힙과 같은 방향 |
| 3 | [백준 2751 수 정렬하기 2](https://www.acmicpc.net/problem/2751) | 정렬 | N이 커서 O(N log N)이 필요하다. 힙 정렬이든 `heapq`든 `sorted()`든 풀리는지 비교해 보자 |
| 4 | [LeetCode 215 Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 상위 k개 | 크기 k짜리 최소 힙을 유지하면 O(n log k)에 k번째로 큰 값을 얻는다. [퀵 셀렉트](../quick-sort/)와 비교해 보기 좋다 |

## 풀이 메모

- 1, 2번은 입력이 "연산 개수 N + 연산 N개" 형태이므로 [solution.py](solution.py)의 `main()`과 입력 형식이 다릅니다. 같은 힙 개념을 `heapq`로 옮겨 쓰는 연습입니다.
- 힙 정렬을 직접 구현해서 3번을 통과시킬 수 있는지는 CPython/PyPy에서 시간을 재 보고, [병합 정렬](../merge-sort/)과도 비교해 보세요.
