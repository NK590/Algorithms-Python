# 연습문제 — 다이나믹 프로그래밍

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 509 Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | 기본형 | 세 가지 구현(재귀·메모이제이션·표)을 모두 써 본다 |
| 2 | [백준 2748 피보나치 수 2](https://www.acmicpc.net/problem/2748) | 기본형 | n이 커지면 느린 재귀는 불가. `fib_fast` |
| 3 | [LeetCode 70 Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | 점화식 | 마지막 걸음이 1칸/2칸. `climb_stairs` |
| 4 | [백준 11726 2×n 타일링](https://www.acmicpc.net/problem/11726) | 점화식 | 결과를 `mod`로. 매 단계 나머지. `tile_2xn` |
| 5 | [백준 1463 1로 만들기](https://www.acmicpc.net/problem/1463) | 최솟값 | `min(dp[i−1], dp[i/2], dp[i/3]) + 1`. 그리디가 틀리는 이유. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 6 | [백준 11727 2×n 타일링 2](https://www.acmicpc.net/problem/11727) | 점화식 | 2×2 타일이 추가되면 점화식이 어떻게 바뀌는지 |
| 7 | [백준 9095 1, 2, 3 더하기](https://www.acmicpc.net/problem/9095) | 점화식 | 마지막에 더한 수가 1/2/3. 테스트 케이스 여러 개 |
| 8 | [백준 1003 피보나치 함수](https://www.acmicpc.net/problem/1003) | 호출 횟수 | 0과 1이 각각 몇 번 호출되는지 (`fib_naive_calls`와 같은 발상) |
| 9 | [백준 1904 01타일](https://www.acmicpc.net/problem/1904) | 점화식 | 끝이 `1`/`00`로 끝나는 경우로 나눈다. 큰 n이라 `mod` |
| 10 | [백준 9461 파도반 수열](https://www.acmicpc.net/problem/9461) | 점화식 찾기 | 규칙에서 `P(n) = P(n−2) + P(n−3)`을 찾는다 |
| 11 | [LeetCode 746 Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | 최솟값 | `dp[i] = cost[i] + min(dp[i−1], dp[i−2])` |
| 12 | [백준 10844 쉬운 계단 수](https://www.acmicpc.net/problem/10844) | 상태 확장 | `dp[길이][마지막 숫자]` 2차원 상태 |

## 풀이 메모

- 1~4번은 "점화식을 직접 세워 보기"가 목표입니다. 상태 정의를 한 문장으로 적고, 작은 n으로 손으로 값을 구해 점화식과 비교하세요.
- 5번이 이 개념의 핵심입니다. `parent`를 기록해 경로까지 복원해 보고, 그리디(나눠지는 것부터)가 틀리는 입력을 직접 찾으세요(10).
- 12번은 상태에 **마지막 숫자**를 추가해야 다음 선택이 정해지는 문제입니다. "다음 선택을 정하는 데 필요한 정보"가 상태에 들어가야 합니다.
- 막히면 작은 N에서 **전수 열거**한 결과와 비교해 점화식을 검증하세요. 이 폴더의 [테스트](test_solution.py)가 타일링과 계단을 그렇게 검증합니다.
