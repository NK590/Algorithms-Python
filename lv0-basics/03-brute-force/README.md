# 브루트 포스 (Brute Force)

가능한 **모든 경우를 확인**하는 가장 단순한 풀이 방식입니다. 더 영리한 알고리즘을 배우기 전에, 느리더라도 정답을 보장하는 풀이를 먼저 떠올리는 연습을 합니다. 그 풀이는 나중에 빠른 풀이를 검증하는 기준이 됩니다.

## 한눈에 비교

| 개념 | 하는 일 | 경우의 수 |
|---|---|---|
| [브루트 포스](brute-force/) | 반복문으로 후보를 모두 시험 | 쌍 N², 세 개 N³ |
| [순열과 조합 나열](permutations-and-combinations/) | 순서 있는/없는 선택, 부분집합을 중복 없이 만들기 | N!, C(N, r), 2^N |

## 읽는 순서

1. [브루트 포스](brute-force/): 경우의 수를 먼저 계산하는 습관
2. [재귀 함수의 구조](../06-recursion/recursion-basics/): 나열하는 재귀를 쓰기 위한 준비
3. [순열과 조합 나열](permutations-and-combinations/)

경우의 수가 시간 제한을 넘으면 [백트래킹](../../lv1-elementary/07-algorithm-paradigms/backtracking/)으로 가지치기하거나 [다이나믹 프로그래밍](../../lv1-elementary/07-algorithm-paradigms/dynamic-programming/)으로 중복 계산을 줄입니다.
