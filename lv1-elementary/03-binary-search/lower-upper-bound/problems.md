# 연습문제 — lower bound / upper bound

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 35 Search Insert Position](https://leetcode.com/problems/search-insert-position/) | 삽입 위치 | 값이 없으면 들어갈 위치를 돌려준다. lower bound 그대로다 |
| 2 | [백준 10816 숫자 카드 2](https://www.acmicpc.net/problem/10816) | 개수 세기 | 각 수가 몇 개인지 질문에 답한다. [solution.py](solution.py)의 `count_equal`/`main()`이 그대로 풀이다 (`Counter`로도 풀리지만 이분 탐색으로 풀어 보자) |
| 3 | [LeetCode 34 Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | 첫/끝 위치 | lower bound와 `upper bound − 1`로 처음과 마지막 위치를 구한다 |
| 4 | [백준 12015 가장 긴 증가하는 부분 수열 2](https://www.acmicpc.net/problem/12015) | LIS | 꼬리 배열에서 lower bound 위치를 갱신하는 O(n log n) 풀이. [LIS](../../../lv2-intermediate/04-dynamic-programming/lis/)로 이어진다 |

## 풀이 메모

- 2번은 질문마다 `count_equal`을 호출합니다. 입력이 많으니 [빠른 입출력](../../../lv0-basics/04-io-and-complexity/fast-io/)을 함께 쓰세요.
- 3번에서 값이 없을 때는 lower bound 위치의 값이 x와 다르므로 `[-1, -1]`을 돌려줍니다.
