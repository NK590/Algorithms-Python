# 연습문제 — 누적 합

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11659 구간 합 구하기 4](https://www.acmicpc.net/problem/11659) | 기본형 | 구간 합 질의 M개. [solution.py](solution.py)의 `main()`이 그대로 풀이다. 질문마다 합을 구하면 시간 초과다 |
| 2 | [백준 2559 수열](https://www.acmicpc.net/problem/2559) | 고정 길이 구간 | 연속된 K일의 합의 최댓값. 누적 합으로 모든 구간 합을 O(1)씩 구한다 |
| 3 | [백준 16139 인간-컴퓨터 상호작용](https://www.acmicpc.net/problem/16139) | 글자별 누적 | 알파벳마다 누적 개수를 만들어 구간에 글자가 몇 번 나오는지 O(1)에 답한다 |
| 4 | [백준 2015 수들의 합 4](https://www.acmicpc.net/problem/2015) | 합이 K인 구간 개수 | 누적 합 + 딕셔너리 (`count_subarrays_with_sum`). 음수가 있어 투 포인터는 안 된다 |
| 5 | [백준 10986 나머지 합](https://www.acmicpc.net/problem/10986) | 나머지가 같은 누적 합 | 구간 합이 M의 배수 ⇔ 두 누적 합의 나머지가 같다. 같은 나머지끼리 쌍의 수를 센다 |
| 6 | [LeetCode 560 Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | 합이 K인 구간 개수 | 4번과 같은 아이디어를 영문 문제로 |

## 풀이 메모

- 1번은 N, M이 10만이라 `sum(arr[i:j])`로 풀면 안 됩니다. 입력도 `sys.stdin.readline`으로 읽으세요.
- 5번은 나머지가 같은 누적 합이 `c`개 있으면 쌍이 `c × (c − 1) / 2`개이고, 나머지 0은 누적 합 자체(0부터 시작하는 구간)를 포함해 센다는 점이 핵심입니다.
