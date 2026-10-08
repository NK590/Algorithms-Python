# 연습문제 — 이분 탐색

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 704 Binary Search](https://leetcode.com/problems/binary-search/) | 기본형 | 정렬된 배열에서 값의 위치를 찾는다 (`binary_search`) |
| 2 | [백준 1920 수 찾기](https://www.acmicpc.net/problem/1920) | 존재 확인 | 정렬 후 M개의 질문에 이분 탐색으로 답한다. [solution.py](solution.py)의 `main()`이 같은 형태(있으면 1, 없으면 0)를 처리한다 |
| 3 | [LeetCode 69 Sqrt(x)](https://leetcode.com/problems/sqrtx/) | 배열 없는 이분 탐색 | `x * x <= n`을 만족하는 가장 큰 x를 찾는다 (`integer_sqrt`) |
| 4 | [백준 1654 랜선 자르기](https://www.acmicpc.net/problem/1654) | 답을 이분 탐색 | 랜선 길이를 정해 놓고 "N개 이상 만들 수 있는가"를 판정한다. 가능한 최대 길이를 찾는 [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/) |
| 5 | [백준 2805 나무 자르기](https://www.acmicpc.net/problem/2805) | 답을 이분 탐색 | 절단기 높이를 정해 놓고 얻는 나무 길이를 센다. 높이 범위가 크다 |

## 풀이 메모

- 2번은 `set`으로도 풀리지만, 이분 탐색으로도 풀어 보며 정렬이 전제라는 점을 확인하세요.
- 4, 5번은 배열을 이분 탐색하는 것이 아니라 **답 자체**의 범위를 이분 탐색합니다. 판정 함수가 단조적(`True…True False…False`)인지 먼저 확인하세요.
