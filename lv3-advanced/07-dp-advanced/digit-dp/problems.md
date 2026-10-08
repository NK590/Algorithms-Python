# 연습문제 — 자릿수 DP

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 233 Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) | 숫자 `1`의 출현 횟수 | `count_digit_occurrences(n, 1)`. 기본형 |
| 2 | [백준 1019 책 페이지](https://www.acmicpc.net/problem/1019) | 숫자 `0~9`의 출현 횟수 | [solution.py](solution.py)의 `main()`이 같은 형태. 앞쪽 0을 세지 않는 것 |
| 3 | [AtCoder ABC007 D 禁止された数字](https://atcoder.jp/contests/abc007/tasks/abc007_4) | 4 또는 9가 들어간 수의 개수 | 구간 `[A, B]` = `f(B) − f(A−1)`. 금지 숫자 두 개 |
| 4 | [LeetCode 357 Count Numbers with Unique Digits](https://leetcode.com/problems/count-numbers-with-unique-digits/) | 모든 자릿수가 다른 수 | `10ⁿ` 미만이라 상한이 없다. 조합으로도 풀리지만 자릿수 DP + 사용한 숫자 비트마스크의 입문 |
| 5 | [LeetCode 600 Non-negative Integers without Consecutive Ones](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/) | 이진수에서 `11`이 없는 수 | `count_binary_without_adjacent_ones`. `0`을 포함한다는 점에 주의 |
| 6 | [LeetCode 902 Numbers At Most N Given Digit Set](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/) | 주어진 숫자들로만 만든 수 | 쓸 수 있는 숫자 집합 제약. 길이가 짧은 수를 따로 세는 부분을 직접 구현해 본다 |
| 7 | [LeetCode 1012 Numbers With Repeated Digits](https://leetcode.com/problems/numbers-with-repeated-digits/) | 같은 숫자가 반복되는 수 | 전체 − (모든 자릿수가 다른 수) |
| 8 | [LeetCode 2376 Count Special Integers](https://leetcode.com/problems/count-special-integers/) | 모든 자릿수가 다른 수 (상한 있음) | 사용한 숫자의 집합을 상태로. tight와 비트마스크 결합 |
| 9 | [AtCoder Educational DP S - Digit Sum](https://atcoder.jp/contests/dp/tasks/dp_s) | 자릿수 합이 `D`의 배수 | `K`가 10¹⁰⁰⁰⁰ 자릿수의 문자열. 파이썬은 `int(K)`로 그대로 받는다. `count_digit_sum_divisible` |
| 10 | [LeetCode 2719 Count of Integers](https://leetcode.com/problems/count-of-integers/) | 구간 `[num1, num2]` + 자릿수 합 범위 | `f(num2) − f(num1 − 1)`. `num1`이 문자열이라 `num1 − 1`의 처리 |
| 11 | [AtCoder ABC135 D Digits Parade](https://atcoder.jp/contests/abc135/tasks/abc135_d) | `?`가 섞인 문자열을 13으로 나눈 나머지가 5 | 위치마다 숫자를 고르는 DP. 나머지를 상태로 (`count_multiples`의 기본형) |
| 12 | [Codeforces 55D Beautiful numbers](https://codeforces.com/problemset/problem/55/D) | 0이 아닌 모든 자릿수로 나누어떨어지는 수 | 상태에 LCM(2520의 약수)과 나머지. 상태 수를 줄이는 아이디어 |

## 풀이 메모

- 1번과 2번은 같은 `digit_dp`로 풀립니다. 먼저 `str(x).count('1')`를 `1..N`에 합하는 순진한 방법으로 작은 `N`에서 비교해 보세요.
- 3번은 구간 `[A, B]`이므로 `f(B) − f(A − 1)`입니다. `A = 1`이면 `f(0) = 0`.
- 5번은 문제가 `0`부터 `n`까지를 세므로 [solution.py](solution.py)의 `1..n` 결과에 `+1`을 해야 합니다.
- 4번, 7번, 8번은 모두 "사용한 숫자의 집합을 상태로" 가는 문제입니다. 상태 수는 `2¹⁰`이며 `step`을 `(사용한 숫자 비트마스크)`로 쓰면 이 구현으로도 풀립니다.
- 9번은 `K`가 10¹⁰⁰⁰⁰ 자릿수이고 답을 `10⁹ + 7`로 나눈 나머지로 요구합니다. [solution.py](solution.py)의 `count_digit_sum_divisible`은 정확한 정수를 돌려주므로 이 크기에서는 느립니다. `digit_dp`의 합산을 모듈러로 바꿔 직접 확장해 보는 연습입니다.
- 12번은 상태 수 줄이기가 핵심입니다. "수가 이 자릿수들로 나누어떨어진다"는 것은 "수가 자릿수들의 LCM으로 나누어떨어진다"와 같고, 가능한 LCM은 `2520`의 약수(48개)뿐입니다. 나머지는 `mod 2520`만 유지합니다.
