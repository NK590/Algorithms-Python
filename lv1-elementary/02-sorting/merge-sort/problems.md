# 연습문제 — 병합 정렬

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2751 수 정렬하기 2](https://www.acmicpc.net/problem/2751) | 기본형 | N이 커서 O(N²) 정렬은 시간 초과다. O(N log N) 정렬이 필요한 첫 문제 |
| 2 | [LeetCode 912 Sort an Array](https://leetcode.com/problems/sort-an-array/) | 직접 구현 | 내장 정렬 없이 O(n log n)으로 정렬하는 것이 취지다. 병합 정렬을 직접 짜서 통과시켜 보자 |
| 3 | [백준 1517 버블 소트](https://www.acmicpc.net/problem/1517) | 역전 수 | 버블 정렬의 교환 횟수 = 역전의 수. 합치는 단계에서 `len(left) - i`를 더해 센다 |
| 4 | [LeetCode 148 Sort List](https://leetcode.com/problems/sort-list/) | 연결 리스트 | 연결 리스트에서는 임의 접근이 안 되므로 병합 정렬이 가장 자연스럽다. 중간 지점 찾기와 합치기를 직접 구현한다 |

## 풀이 메모

- 1번은 [solution.py](solution.py)의 `merge_sort`로 풀립니다. `main()`은 첫 줄 N, 이후 한 줄에 정수 하나를 읽습니다. 다만 N이 매우 크므로 시간이 빠듯하면 내장 `sorted()`로도 풀 수 있고, 이 문제는 알고리즘 자체를 익히는 용도로 삼으세요.
- 3번은 `count_inversions`를 그대로 쓰면 됩니다. 값이 같은 원소를 역전으로 세지 않는다는 점(`<=`)을 확인하세요. 작은 입력은 [버블 정렬](../bubble-sort/)의 교환 횟수와 비교해 검증할 수 있습니다.
