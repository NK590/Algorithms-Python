# 연습문제 — 집합과 딕셔너리 활용

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1269 대칭 차집합](https://www.acmicpc.net/problem/1269) | 집합 연산 | 한쪽에만 있는 원소의 수. [solution.py](solution.py)의 `symmetric_difference_size`/`main()`이 그대로 풀이다 |
| 2 | [백준 1764 듣보잡](https://www.acmicpc.net/problem/1764) | 교집합 | 두 명단에 모두 있는 이름을 사전순으로 출력한다 (`common_elements`) |
| 3 | [LeetCode 217 Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | 중복 확인 | 집합의 크기와 리스트의 크기를 비교하거나 `first_duplicate`처럼 훑는다 |
| 4 | [LeetCode 347 Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | 빈도 | `Counter`로 세고 횟수 기준으로 상위 k개를 고른다 (`top_k_frequent`) |
| 5 | [LeetCode 128 Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 집합 + 시작점 | 정렬 없이 O(n)에 가장 긴 연속 수열을 찾는다 (`longest_consecutive`) |

## 풀이 메모

- 1번은 입력이 `A B`와 두 줄의 수 목록입니다. `main()`처럼 첫 줄의 `A B`는 개수라서 읽고 넘깁니다.
- 5번은 모든 수에서 앞으로 세면 O(n²)이 되므로, "시작점일 때만 센다"는 조건이 핵심입니다.
