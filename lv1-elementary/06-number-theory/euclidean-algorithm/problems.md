# 연습문제 — 유클리드 호제법

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2609 최대공약수와 최소공배수](https://www.acmicpc.net/problem/2609) | 기본형 | `gcd`와 `lcm = a / gcd × b`. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 1934 최소공배수](https://www.acmicpc.net/problem/1934) | 기본형 | 테스트 케이스가 여러 개. 빠른 입력으로 읽는다 |
| 3 | [백준 5347 LCM](https://www.acmicpc.net/problem/5347) | 기본형 | 값이 커질 수 있어도 파이썬은 그대로 계산된다 |
| 4 | [백준 1735 분수 합](https://www.acmicpc.net/problem/1735) | 약분 | 통분한 합을 gcd로 약분해 기약분수로 출력한다 |
| 5 | [백준 3036 링](https://www.acmicpc.net/problem/3036) | 약분 | 첫 링과 각 링의 반지름 비를 기약분수로 만든다 |
| 6 | [LeetCode 1979 Find Greatest Common Divisor of Array](https://leetcode.com/problems/find-greatest-common-divisor-of-array/) | 응용 | 배열의 최솟값과 최댓값의 gcd |
| 7 | [백준 9613 GCD 합](https://www.acmicpc.net/problem/9613) | 모든 쌍 | 가능한 모든 쌍의 gcd를 합한다. 합이 커질 수 있다 |
| 8 | [백준 2981 검문](https://www.acmicpc.net/problem/2981) | 성질 | 나머지가 같다 ⇔ 차이가 `m`의 배수. 차이들의 `gcd`의 약수를 구한다 |
| 9 | [LeetCode 1071 Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | 응용 | 문자열의 "공약수"도 길이의 gcd로 확인할 수 있다 |
| 10 | [백준 1850 최대공약수](https://www.acmicpc.net/problem/1850) | 관찰 | 1로만 이루어진 두 수의 gcd는 1의 개수의 gcd로 이루어진 수다. 입력이 매우 크다 |
| 11 | [백준 2824 최대공약수](https://www.acmicpc.net/problem/2824) | 큰 수 | 두 수열의 곱의 gcd. 곱을 직접 만들지 말고 하나씩 gcd로 줄여 간다 |
| 12 | [백준 14476 최대공약수 하나 빼기](https://www.acmicpc.net/problem/14476) | 심화 | 하나를 빼고 gcd를 최대화. 앞·뒤 누적 gcd ([누적 합](../../04-range-techniques/prefix-sum/)과 같은 발상) |

## 풀이 메모

- 1번과 2번은 `math.gcd`로 한 줄에 풀리지만, 한 번은 [solution.py](solution.py)의 `gcd`를 직접 써서 `while` 루프를 손에 익히세요.
- 4번과 5번은 약분 후 출력 형식(부호, 분모가 1일 때)을 [서로소](../relatively-prime/)의 `reduce_fraction`과 같은 방식으로 처리합니다.
- 8번은 서로 다른 수들의 **차이의 gcd**를 구해 약수를 나열하는 문제입니다. 약수 나열은 [약수와 배수](../../../lv0-basics/02-number-theory/divisors-and-multiples/)를 참고하세요.
- 10번은 입력이 몇 자리까지 오는지 확인하세요. 수를 정수로 만들지 않고 **자릿수(개수)** 의 gcd로 환원해야 합니다.
