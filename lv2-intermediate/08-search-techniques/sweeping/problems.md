# 연습문제 — 스위핑

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2170 선 긋기](https://www.acmicpc.net/problem/2170) | 덮인 길이 | 겹치는 선분을 합쳐 전체 길이. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [LeetCode 56 Merge Intervals](https://leetcode.com/problems/merge-intervals/) | 구간 합치기 | 시작점 정렬 + 끝은 `max`. 맞닿은 구간(`[1,4]`, `[4,5]`)도 합친다 |
| 3 | [LeetCode 57 Insert Interval](https://leetcode.com/problems/insert-interval/) | 구간 삽입 | 이미 정렬·병합된 목록에 하나를 넣는 `O(n)` 스위핑 |
| 4 | [백준 1689 겹치는 선분](https://www.acmicpc.net/problem/1689) | 최대 겹침 | 반열린 구간으로 이벤트를 만들고 같은 위치는 끝 먼저 (`max_overlap`) |
| 5 | [백준 19598 최소 회의실 개수](https://www.acmicpc.net/problem/19598) | 최대 겹침 | 필요한 회의실 수 = 최대 동시 회의 수 |
| 6 | [백준 11000 강의실 배정](https://www.acmicpc.net/problem/11000) | 최대 겹침 / 힙 | 위와 같은 개념. 시작 순으로 정렬하고 끝나는 시각의 최소 힙으로도 풀린다 |
| 7 | [LeetCode 986 Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | 두 목록의 교집합 | 정렬된 두 목록을 투 포인터로 훑기 |
| 8 | [백준 1933 스카이라인](https://www.acmicpc.net/problem/1933) | 스카이라인 | `skyline`과 같은 구조. 출력은 `(x, 높이)`를 공백으로 |
| 9 | [LeetCode 218 The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | 스카이라인 | 같은 `x`의 시작/끝 이벤트 순서와 힙 지연 삭제 |
| 10 | [LeetCode 850 Rectangle Area II](https://leetcode.com/problems/rectangle-area-ii/) | 직사각형 합집합 | 직사각형 최대 200개. 띠 방법(`rectangle_union_area`)으로 풀리고 `mod 10⁹+7` 출력 |
| 11 | [백준 3392 화성 지도](https://www.acmicpc.net/problem/3392) | 직사각형 합집합 | 직사각형 최대 3만 개라 `O(n²)` 띠 방법은 불가능. 세그먼트 트리로 덮인 길이를 관리 |

## 풀이 메모

- 1번은 `covered_length`가 그대로 답입니다. 입력 선분이 `x > y`로 뒤바뀌어 있을 수 있어서 `(min, max)`로 정리합니다.
- 4번~6번은 구간의 정의(반열린인가 닫힌인가)가 이벤트 순서를 정합니다. 끝과 시작이 같은 시각에 만나도 회의실을 같이 쓰지 않는다면 끝 이벤트를 먼저 처리합니다. [테스트](test_solution.py)의 `test_max_overlap_matches_pointwise_count_for_half_open_intervals`가 모든 정수 점에서 세어 본 값과 비교합니다.
- 8번과 9번은 [README](README.md#3-손으로-따라가기)의 표를 그대로 따라 구현해 보세요. 같은 `x`에서 높이가 큰 시작 이벤트를 먼저 처리하는 이유와 `result[-1][1] != top` 검사의 역할을 직접 확인합니다.
- 10번은 좌표를 압축해 띠를 만들고 띠마다 y 구간을 합치는 방법이 `O(n² log n)`이라 200개 정도에 충분합니다. 11번처럼 개수가 많으면 [세그먼트 트리](../../../lv3-advanced/01-range-query-structures/segment-tree/)가 필요합니다.
