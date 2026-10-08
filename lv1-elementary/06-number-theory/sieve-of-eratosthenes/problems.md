# 연습문제 — 에라토스테네스의 체

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1929 소수 구하기](https://www.acmicpc.net/problem/1929) | 기본형 | M 이상 N 이하의 소수 출력. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 2960 에라토스테네스의 체](https://www.acmicpc.net/problem/2960) | 과정 따라가기 | K번째로 지워지는 수. 체의 지우는 **순서**를 그대로 시뮬레이션한다 |
| 3 | [LeetCode 204 Count Primes](https://leetcode.com/problems/count-primes/) | 개수 | `count_primes`. n 미만이라는 경계에 주의 |
| 4 | [백준 4948 베르트랑 공준](https://www.acmicpc.net/problem/4948) | 여러 질의 | 큰 쪽 최댓값까지 체를 **한 번만** 만들고 질의마다 개수를 센다 (누적 합 [prefix-sum](../../04-range-techniques/prefix-sum/)) |
| 5 | [백준 6588 골드바흐의 추측](https://www.acmicpc.net/problem/6588) | 여러 질의 | 체 한 번 + 각 짝수마다 작은 소수부터 보며 `n − p`가 소수인지 확인 |
| 6 | [백준 17103 골드바흐 파티션](https://www.acmicpc.net/problem/17103) | 개수 세기 | 순서가 다른 합을 같은 것으로 센다 |
| 7 | [백준 1644 소수의 연속합](https://www.acmicpc.net/problem/1644) | 체 + 투 포인터 | 소수 목록을 만들어 [투 포인터](../../04-range-techniques/two-pointers/)로 연속 구간의 합을 센다 |
| 8 | [백준 1990 소수인팰린드롬](https://www.acmicpc.net/problem/1990) | 체 + 조건 | 범위가 크면 체와 팰린드롬 조건 중 무엇을 먼저 걸러야 효율적인지 생각해 보기 |
| 9 | [백준 16563 어려운 소인수분해](https://www.acmicpc.net/problem/16563) | 변형 (spf 표) | 가장 작은 소인수 표를 만들어 질의마다 O(log) 소인수분해. `smallest_prime_factor_table` |
| 10 | [백준 1456 거의 소수](https://www.acmicpc.net/problem/1456) | 응용 | 소수의 거듭제곱을 센다. `i × i`로 오버플로가 나지 않게 범위를 조절한다 |
| 11 | [백준 1016 제곱ㄴㄴ수](https://www.acmicpc.net/problem/1016) | 구간 체 | 범위의 값이 크고 길이는 작은 구간에서 제곱수의 배수를 지운다. 체를 구간으로 옮기는 연습 |

## 풀이 메모

- 1번은 `sieve(n)`을 만들고 `p >= m`만 걸러 출력하면 됩니다. 경계(M 자신이 소수일 때)가 맞는지 [테스트](test_solution.py)의 `test_main_range_is_inclusive_on_both_ends`처럼 확인하세요.
- 4~6번처럼 질의가 여러 번이면 **체를 질의마다 다시 만들지 말고** 한 번만 만드세요. 입력의 최댓값까지 만들어 두는 것이 정석입니다.
- 9번은 소인수분해가 질의마다 O(√n)이면 느립니다. 표를 한 번 만들어 두는 이유를 직접 확인할 수 있습니다.
- 10, 11번은 체의 변형이라 처음 풀 때 막히기 쉽습니다. 이 레벨에서는 건너뛰었다가 돌아와도 됩니다.
