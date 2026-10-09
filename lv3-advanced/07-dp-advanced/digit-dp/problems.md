# 연습문제 — 자릿수 DP

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Digit Sum](https://atcoder.jp/contests/dp/tasks/dp_s) | 핵심 연습 | 자릿수 합의 나머지와 상한 일치 여부를 상태로 둔다 |
| 2 | [LeetCode 233 Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) | 숫자 `1`의 출현 횟수 | `count_digit_occurrences(n, 1)`. 기본형 |
| 3 | [AtCoder ABC007 D 禁止された数字](https://atcoder.jp/contests/abc007/tasks/abc007_4) | 4 또는 9가 들어간 수의 개수 | 구간 `[A, B]` = `f(B) − f(A−1)`. 금지 숫자 두 개 |
| 4 | [LeetCode 357 Count Numbers with Unique Digits](https://leetcode.com/problems/count-numbers-with-unique-digits/) | 모든 자릿수가 다른 수 | `10ⁿ` 미만이라 상한이 없다. 조합으로도 풀리지만 자릿수 DP + 사용한 숫자 비트마스크의 입문 |
| 5 | [LeetCode 600 Non-negative Integers without Consecutive Ones](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/) | 이진수에서 `11`이 없는 수 | `count_binary_without_adjacent_ones`. `0`을 포함한다는 점에 주의 |
| 6 | [LeetCode 902 Numbers At Most N Given Digit Set](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/) | 주어진 숫자들로만 만든 수 | 쓸 수 있는 숫자 집합 제약. 길이가 짧은 수를 따로 세는 부분을 직접 구현해 본다 |
| 7 | [LeetCode 1012 Numbers With Repeated Digits](https://leetcode.com/problems/numbers-with-repeated-digits/) | 같은 숫자가 반복되는 수 | 전체 − (모든 자릿수가 다른 수) |
| 8 | [LeetCode 2376 Count Special Integers](https://leetcode.com/problems/count-special-integers/) | 모든 자릿수가 다른 수 (상한 있음) | 사용한 숫자의 집합을 상태로. tight와 비트마스크 결합 |
| 9 | [LeetCode 2719 Count of Integers](https://leetcode.com/problems/count-of-integers/) | 구간 `[num1, num2]` + 자릿수 합 범위 | `f(num2) − f(num1 − 1)`. `num1`이 문자열이라 `num1 − 1`의 처리 |
| 10 | [AtCoder ABC135 D Digits Parade](https://atcoder.jp/contests/abc135/tasks/abc135_d) | `?`가 섞인 문자열을 13으로 나눈 나머지가 5 | 위치마다 숫자를 고르는 DP. 나머지를 상태로 (`count_multiples`의 기본형) |
| 11 | [Codeforces 55D Beautiful numbers](https://codeforces.com/problemset/problem/55/D) | 0이 아닌 모든 자릿수로 나누어떨어지는 수 | 상태에 LCM(2520의 약수)과 나머지. 상태 수를 줄이는 아이디어 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
