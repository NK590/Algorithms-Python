# 정수론 기초 (Number Theory)

**최대공약수와 서로소, 소수 구하기, 소인수분해, 약수 구하기**를 다룹니다. 모두 "나머지와 배수"만으로 만든 도구이고, 이후 Lv2~3의 모듈러 연산(오일러 피 함수, 페르마의 소정리, 확장 유클리드 호제법)이 이 위에 쌓입니다.

## 한눈에 비교

| 개념 | 하는 일 | 입력 크기 | 시간 |
|---|---|---|---|
| [유클리드 호제법](euclidean-algorithm/) | 두 수의 최대공약수·최소공배수 | 수가 10^18까지 | O(log min(a, b)) |
| [서로소](relatively-prime/) | 공약수가 1뿐인지, 기약분수 | 수가 10^18까지 | O(log min(a, b)) |
| [에라토스테네스의 체](sieve-of-eratosthenes/) | **범위 안의 모든 소수**와 소수 판별표 | n ≤ 10^6~10^7 | O(n log log n) |
| [소인수분해](prime-factorization/) | **수 하나**를 소수의 곱으로 | n ≤ 10^12 | O(√n) |
| [약수 체](divisor-sieve/) | **1~n 모든 수**의 약수 개수·합·목록 | n ≤ 10^6 | O(n log n) |

## 어떤 도구를 쓸까

| 문제 상황 | 선택 |
|---|---|
| 두 수의 최대공약수 / 최소공배수 / 약분 | [유클리드 호제법](euclidean-algorithm/) |
| "서로소인가?", 기약분수 | [서로소](relatively-prime/) |
| 소수 여부를 **수 하나만** (n ≤ 10^12) | [단순 판별](../../lv0-basics/02-number-theory/naive-prime-check/)의 O(√n) |
| 소수 여부를 **범위 전체에서 여러 번** | [체](sieve-of-eratosthenes/) |
| 수 **하나**를 소인수분해 | [소인수분해](prime-factorization/) (n ≤ 10^12) |
| 수 **많이**를 소인수분해 (모두 10^7 이하) | [체](sieve-of-eratosthenes/)의 가장 작은 소인수 표 + [소인수분해](prime-factorization/)의 `factorize_with_spf` |
| 수 하나의 약수 | √n까지 탐색 ([약수와 배수](../../lv0-basics/02-number-theory/divisors-and-multiples/)) |
| 1~n **모든 수**의 약수의 합·개수 | [약수 체](divisor-sieve/) |
| 수 하나의 약수의 개수·합 | [소인수분해](prime-factorization/)에서 지수로 공식 |

**수 하나냐, 범위 전체냐**가 첫 번째 질문입니다. 하나만 필요한데 표를 만들면 낭비이고, 많이 필요한데 하나씩 구하면 시간 초과입니다. (약수의 합을 n = 10^6까지 구할 때 표는 1.5초, 수마다 구하면 41.7초 걸렸습니다.)

## 읽는 순서

1. [유클리드 호제법](euclidean-algorithm/) → [서로소](relatively-prime/): 나머지만으로 만든 가장 오래된 알고리즘
2. [에라토스테네스의 체](sieve-of-eratosthenes/) → [소인수분해](prime-factorization/): 소수와 분해
3. [약수 체](divisor-sieve/): 체의 틀을 약수에 적용

이후: [오일러 피 함수](../../lv2-intermediate/06-number-theory/euler-phi/), [페르마의 소정리](../../lv2-intermediate/06-number-theory/fermat-little-theorem/), [확장 유클리드 호제법](../../lv3-advanced/02-number-theory/extended-euclidean-algorithm/)
