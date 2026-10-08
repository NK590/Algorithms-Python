# 연습문제 — 에일리언 트릭

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2228 구간 나누기](https://www.acmicpc.net/problem/2228) | 서로 인접하지 않은 `M`개 구간의 합의 최대 | [solution.py](solution.py)의 `main()`이 같은 형태 (`N`이 작으면 `O(NM)` DP로도 풀리니 두 방법 비교). 구간이 인접해도 되는지는 문제 조건으로 확인 |
| 2 | [Codeforces 958E2 Guard Duty (medium)](https://codeforces.com/problemset/problem/958/E2) | 인접하지 않은 간선 `k`개 고르기, 합 최소 (`k` 큼) | 최소화 + 볼록. 간선이 양 끝점을 공유하지 않아야 하므로 완화 DP는 `i`번째 간선을 쓰는지만 추적 |
| 3 | [Codeforces 321E Ciel and Gondolas](https://codeforces.com/problemset/problem/321/E) | 수열을 `k`개 구간으로 나눠 구간 비용 합 최소 | 비용이 사각 부등식을 만족. 완화 DP `O(n²)` 대신 분할 정복 최적화/볼록 껍질 트릭 `O(n log n)`을 `partition_min_cost`에 대입해 비교 |
| 4 | [Codeforces 739E Gosha is hunting](https://codeforces.com/problemset/problem/739/E) | 두 종류의 포획 도구를 각각 `a`개, `b`개 쓰는 기대값 최대화 | **제약이 두 개**: 한 종류는 `λ`로 완화하고 다른 종류는 `O(n²)` DP, 또는 `λ` 두 개(중첩 이분 탐색). 동점 처리가 특히 까다롭다 |
| 5 | [Codeforces 1279F New Year and Handle Change](https://codeforces.com/problemset/problem/1279/F) | 길이 `l`짜리 구간 `k`개로 문자열 덮기 | 덮은 구간 수 `k` 이하 제약. 개수가 늘수록 이득이 줄어드는 볼록 구조. 완화 DP `O(n)` |
| 6 | [AtCoder ARC168 E - Subsegments with Large Sums](https://atcoder.jp/contests/arc168/tasks/arc168_e) | `k`개 원소를 골라 (구간 개수 - 원소 개수 관련) 최솟값 | 문제를 "각 구간에 벌점"으로 바꾸면 에일리언 트릭이 정확히 들어맞는 최근 문제. 볼록성의 증명보다 작은 입력 실험으로 확인하는 연습 |
| 7 | [IOI 2016 Aliens (oj.uz)](https://oj.uz/problem/view/IOI16_aliens) | 점들을 `k`개의 정사각형으로 덮는 최소 총 면적 | 에일리언 트릭의 원조. 점을 정렬·불필요한 점 제거 → 완화 DP를 볼록 껍질 트릭으로 `O(n)` → 이분 탐색 (제곱합 구간 나누기와 같은 구조) |

## 풀이 메모

- 1번은 가장 작은 입력부터 시작해서 [test_solution.py](test_solution.py)처럼 느린 DP, 전수 탐색(비트마스크), 에일리언 트릭 세 방법이 같은 값을 내는지 확인해 보세요.
- 2번과 3번은 이 단원의 두 번째와 세 번째 응용(`partition_min_cost`, `partition_sum_of_squares`)의 변주입니다. 3번은 비용 함수가 `cost(l, r)`로 주어지므로 `O(n²)` 완화를 `O(n log n)`으로 줄이는 것이 과제입니다.
- 4번은 볼록성 자체를 증명하기 어려운 문제입니다. 실제로는 작은 입력에서 `F(k)`의 2차 차분이 항상 한 방향임을 확인하고 쓰는 경우가 많습니다.
- 5번~7번을 풀 때는 먼저 *개수를 제한하지 않는 버전* 의 DP를 `(값, 개수)` 쌍으로 쓰는 연습을 하고, 동점일 때 개수를 많이 하는 쪽을 고르도록 비교를 정리한 다음 이분 탐색으로 감싸세요.
- 6번과 7번은 이 단원에서 가장 어렵습니다. 6번은 완화한 벌점이 정수가 아닐 수 있는지(정수 `λ`로 충분한지)도 확인해 보세요.
