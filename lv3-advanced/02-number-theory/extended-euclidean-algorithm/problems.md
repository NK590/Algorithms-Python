# 연습문제 — 확장 유클리드 호제법

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 1250 Check If It Is a Good Array](https://leetcode.com/problems/check-if-it-is-a-good-array/) | 베주 항등식 | 정수 결합으로 1을 만들 수 있는가 ⟺ 전체 gcd가 1. 구현 없이 항등식만 알아도 풀린다 |
| 2 | [LeetCode 365 Water and Jug Problem](https://leetcode.com/problems/water-and-jug-problem/) | 베주 항등식 | 두 물통으로 `z`리터를 만들 수 있는가 ⟺ `z`가 두 용량의 `gcd`의 배수이고 `z ≤ x + y` |
| 3 | [백준 14565 역원(Inverse) 구하기](https://www.acmicpc.net/problem/14565) | 합성수의 역원 | 모듈러가 소수가 아니므로 페르마가 안 된다. `mod_inverse`. 역원이 없으면 -1 |
| 4 | [백준 21568 Ax+By=C](https://www.acmicpc.net/problem/21568) | 일차 부정 방정식 | 해가 없으면 -1, 있으면 출력 범위 안의 해를 구한다. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 5 | [백준 3955 캔디 분배](https://www.acmicpc.net/problem/3955) | 일차 방정식 + 범위 | 인당 사탕 수와 봉지 수의 조건을 `ax + by = c`의 정수 해로 바꾸고 양수·상한을 만족하는 해를 고른다 |
| 6 | [AtCoder ABC186 E - Throne](https://atcoder.jp/contests/abc186/tasks/abc186_e) | 일차 합동식 | 원형 위에서 일정한 칸씩 이동해 목표 위치에 처음 도착하는 횟수 = 일차 합동식의 최소 음이 아닌 해 (`solve_linear_congruence`) |

## 풀이 메모

- 1번, 2번은 코드 없이 "정수 결합으로 만들 수 있는 수 = `gcd`의 배수"라는 베주 항등식만으로 풀립니다. [README](README.md#2-핵심-아이디어)의 증명 구조와 비교해 보세요.
- 3번은 `pow(a, -1, m)`도 같은 답을 줍니다. 직접 구현으로 `gcd`가 1인지 확인하는 부분을 익히는 것이 목적입니다.
- 4번에서 해의 범위를 맞추려면 일반해 `x = x₁ + (b/g)·t`에서 `t`를 골라 크기를 줄입니다. [테스트](test_solution.py)가 일반해를 모든 작은 입력에서 완전탐색과 비교합니다.
- 5번은 `K·x ≡ ... (mod C)`꼴로 정리해 `solve_linear_congruence`로 푸는 방법과 `ax + by = c`로 푸는 방법이 있습니다. 두 방법을 모두 구현해 비교하면 합동식과 부정 방정식의 관계가 보입니다.
- 6번은 이동 칸 수와 원의 크기의 `gcd`가 필요한 이동량을 나누지 않으면 영원히 도착하지 못합니다. 합동식 `a·t ≡ b (mod m)`으로 세우고 `solve_linear_congruence`가 돌려준 `x₀`가 가장 작은 음이 아닌 해입니다.
