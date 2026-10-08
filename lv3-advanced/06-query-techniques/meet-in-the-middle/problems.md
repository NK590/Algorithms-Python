# 연습문제 — 중간에서 만나기

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1450 냅색문제](https://www.acmicpc.net/problem/1450) | 합이 `C` 이하인 부분집합 수 | `N ≤ 30`, 무게 ≤ 10⁹. [solution.py](solution.py)의 `main()`이 같은 형태. 빈 집합도 센다 |
| 2 | [백준 1208 부분수열의 합 2](https://www.acmicpc.net/problem/1208) | 합이 정확히 `S`인 부분수열 수 | `N ≤ 40`. 값이 음수일 수 있다. `S = 0`이면 공집합을 빼야 한다 |
| 3 | [LeetCode 1755 Closest Subsequence Sum](https://leetcode.com/problems/closest-subsequence-sum/) | 목표에 가장 가까운 합 | `n ≤ 40`, 음수 가능. `closest_subset_sum`의 기본형. 빈 부분수열이 허용된다 |
| 4 | [백준 2143 두 배열의 합](https://www.acmicpc.net/problem/2143) | 두 배열의 부분 배열 합 | 부분 배열 합을 각각 나열하고 `Counter`로 맞춘다. 같은 "절반씩 맞춰 보기" 구조 |
| 5 | [LeetCode 2035 Partition Array Into Two Arrays to Minimize Sum Difference](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/) | 두 배열로 나눠 합의 차 최소화 | 원소 `2n ≤ 30`. 각 절반에서 *고른 개수별*로 합을 나열해 맞춘다 |
| 6 | [LeetCode 805 Split Array With Same Average](https://leetcode.com/problems/split-array-with-same-average/) | 평균이 같은 두 부분으로 나누기 | 개수별 합 집합 + 평균 조건을 정수로 바꾸는 법 |
| 7 | [백준 7453 합이 0인 네 정수](https://www.acmicpc.net/problem/7453) | 네 배열의 합이 0 | `N ≤ 4000`. `four_sum_zero_count`의 기본형이지만 파이썬은 메모리/시간이 한계 |
| 8 | [Codeforces 1006F Xor-Paths](https://codeforces.com/problemset/problem/1006/F) | 격자 경로의 XOR | 출발점과 도착점에서 중간 대각선까지 각각 탐색해 대각선에서 만난다 |

## 풀이 메모

- 1번과 2번은 둘 다 `N ≈ 30~40`이지만 1번은 "이하", 2번은 "정확히"입니다. `bisect_right`와 `Counter`로 각각 풉니다. 2번에서 **공집합** 처리가 자주 틀립니다.
- 3번은 값이 음수일 수 있어서 부분집합 합의 범위로 인덱스를 잡는 DP가 불가능합니다. 이진 탐색으로 후보 두 개를 비교하는 방법을 [README](README.md)의 표와 대조해 보세요.
- 5번은 중간에서 만나기의 일반형입니다. 합만 맞추면 안 되고 **각 절반에서 몇 개를 골랐는지**도 맞춰야 합니다(왼쪽에서 `k`개 고르면 오른쪽에서 `n − k`개).
- 7번은 파이썬에서 Counter 방식이 `N = 2000`에서도 336MB를 씁니다([README](README.md#5-복잡도와-입력-크기-가이드)의 측정). 원래 크기를 푸는 데는 정렬된 배열 두 개와 두 포인터를 쓰는 변형이나 다른 언어가 필요합니다.
- 8번은 "격자의 대각선에서 만난다"는 발상이 핵심입니다. 중간 대각선의 각 칸에서 `XOR`값 → 개수를 `dict`로 모읍니다.
