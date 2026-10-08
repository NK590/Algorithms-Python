# 연습문제 — 모노톤 스택

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 17298 오큰수](https://www.acmicpc.net/problem/17298) | 오른쪽에서 처음으로 큰 값 | 기본형. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [백준 2493 탑](https://www.acmicpc.net/problem/2493) | 왼쪽에서 처음으로 큰 값 | 레이저가 왼쪽으로 가서 처음 맞는 탑의 **번호**. 값이 아니라 위치를 저장 |
| 3 | [백준 6198 옥상 정원 꾸미기](https://www.acmicpc.net/problem/6198) | 볼 수 있는 개수 | 각 건물이 볼 수 있는 건물 수의 합 = 각 건물을 볼 수 있는 건물 수의 합. pop할 때마다 개수를 더한다 |
| 4 | [LeetCode 739 Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | 위치 차이 | 오큰수의 거리. `days_until_warmer` |
| 5 | [백준 17299 오등큰수](https://www.acmicpc.net/problem/17299) | 값을 바꿔서 | 비교 기준이 "등장 횟수"인 오큰수. 비교 대상만 바꾸면 같은 코드 |
| 6 | [LeetCode 503 Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | 원형 배열 | 수열을 두 번 훑는다 (인덱스 `i % n`) |
| 7 | [백준 6549 히스토그램에서 가장 큰 직사각형](https://www.acmicpc.net/problem/6549) | 히스토그램 | 센티널 `0`과 pop 시의 폭 계산. `largest_rectangle_in_histogram` |
| 8 | [LeetCode 42 Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | 빗물 | 스택으로 층별 계산 (`trapped_rain_water`), 양쪽 최댓값 배열이나 투 포인터로도 풀린다 |
| 9 | [LeetCode 402 Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | 그리디 + 스택 | 앞 자리가 크면 pop하는 오름차순 스택, 남은 `k`는 끝에서 제거 |
| 10 | [백준 3015 오아시스 재결합](https://www.acmicpc.net/problem/3015) | 쌍의 개수 | 서로 볼 수 있는 쌍의 수. 같은 키가 연속될 때 (키, 개수) 쌍을 스택에 저장 |
| 11 | [LeetCode 907 Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | 기여도 계산 | 각 원소가 최솟값인 구간의 왼쪽·오른쪽 한계를 스택으로 구해 `값 × 왼쪽 개수 × 오른쪽 개수`. 중복 값은 한쪽만 `≤` |
| 12 | [LeetCode 85 Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | 히스토그램으로 환원 | 행마다 위로 연속한 1의 개수를 막대 높이로 하는 히스토그램 문제 |

## 풀이 메모

- 1번을 풀 때 스택에 값 대신 위치를 넣고 `numbers[stack[-1]]`으로 비교해 보세요. 2번, 4번, 7번에서 그대로 쓰입니다.
- 3번은 "몇 개의 건물을 볼 수 있는가"를 pop 횟수로 세는 문제로 바꾸면 합이 `O(n)`입니다. 전체 합은 `n²/2` 수준까지 커질 수 있어 C++에서는 `long long`이 필요합니다.
- 7번과 8번은 [README](README.md#3-손으로-따라가기)의 표를 손으로 따라가 보고 코드와 같은 값이 나오는지 확인하세요. [테스트](test_solution.py)가 모든 작은 입력에서 순진한 계산과 비교합니다.
- 10번과 11번은 **같은 값**을 어떻게 처리하는지가 핵심입니다. 같은 값이 연속되면 한쪽에서는 `<`, 다른 쪽에서는 `≤`로 비교해야 구간이 겹쳐 세어지지 않습니다.
- 12번은 모노톤 스택을 `행의 수`번 호출하므로 `O(행 × 열)`입니다.
