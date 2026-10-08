# 연습문제 — 매개변수 탐색

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1654 랜선 자르기](https://www.acmicpc.net/problem/1654) | 최대화 (`last_true`) | 같은 길이로 잘라 `N`개 이상. 하한은 1(0이면 나눗셈 오류). [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [백준 2805 나무 자르기](https://www.acmicpc.net/problem/2805) | 최대화 | 절단기 높이. 높이가 낮을수록 많이 얻는 단조 구조. 합이 커서 Python에서도 판정 함수를 가볍게 |
| 3 | [백준 2512 예산](https://www.acmicpc.net/problem/2512) | 최대화 | 상한액 `x`를 정해 `min(요청, x)`의 합이 총액 이하인가 |
| 4 | [LeetCode 875 Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 최소화 (`first_true`) | 시간 `h` 안에 다 먹을 수 있는 최소 속도. 올림 나눗셈 `ceil` 처리 |
| 5 | [백준 2110 공유기 설치](https://www.acmicpc.net/problem/2110) | 최소를 최대화 | 이웃 거리의 최솟값을 최대로. 정렬 후 앞에서부터 그리디로 놓기 (`max_min_distance`) |
| 6 | [LeetCode 1011 Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | 최대를 최소화 | 하루 적재량의 하한은 가장 무거운 짐, 상한은 전체 합 |
| 7 | [백준 2343 기타 레슨](https://www.acmicpc.net/problem/2343) | 최대를 최소화 | 연속한 `M`개 블루레이로 나눌 때 가장 큰 크기의 최소 (`split_array_min_largest_sum`) |
| 8 | [백준 3079 입국심사](https://www.acmicpc.net/problem/3079) | 최소 시간 | 시간 `t`에 심사한 사람 수는 `Σ t // 시간`. 답이 10¹⁸까지 (`min_time_to_finish`) |
| 9 | [LeetCode 410 Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | 최대를 최소화 | 위의 7번과 같은 문제. DP로도 풀리지만 이분 탐색이 훨씬 간단하다 |
| 10 | [백준 1939 중량제한](https://www.acmicpc.net/problem/1939) | 그래프 + 이분 탐색 | 중량 `w` 이상 다리만 써서 두 섬이 연결되는가를 BFS로 판정 |
| 11 | [백준 1300 K번째 수](https://www.acmicpc.net/problem/1300) | 개수 세기 | 곱셈표(`i × j`)에서 `x` 이하의 개수를 `Σ min(N, x // i)`로 센다. 배열을 만들지 않고 K번째 수를 구한다 |
| 12 | [백준 1561 놀이공원](https://www.acmicpc.net/problem/1561) | 시간 + 시뮬레이션 | 시간 `t`까지 탑승한 인원을 센 뒤 마지막 한 명을 시뮬레이션 |

## 풀이 메모

- 1번부터 3번까지 `ok(x)`를 직접 쓰고 `first_true`/`last_true`에 넣어 보세요. 경계 실수는 [테스트](test_solution.py)처럼 **모든 `x`를 하나씩 시도한 결과와 비교**하면 바로 찾을 수 있습니다.
- 4번은 `ceil(p / s)`를 `(p + s - 1) // s`로 씁니다. 5번의 `ok`는 "놓은 개수 ≥ `C`"이므로 `C`개를 놓고도 남는 경우에도 `True`입니다.
- 7번과 9번과 6번은 같은 판정(묶음 수가 `m` 이하인가)입니다. 9번의 `lo = max(원소)`, `hi = sum`을 한 번 직접 설명해 보면 좋습니다.
- 8번의 `hi`는 `(가장 빠른 심사대의 시간) × 사람 수`입니다. 10¹⁸ 근처라서 C++/Java에서는 `long long`이 필요합니다.
- 11번처럼 "x 이하의 개수를 셀 수 있다"면 K번째 수를 구할 수 있는 것이 이 기법의 확장입니다. 정답은 개수가 `K` 이상이 되는 **최소** `x`(`first_true`)입니다.
