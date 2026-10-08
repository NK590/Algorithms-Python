# 수학·정수론 기초 (Number Theory Basics)

정수를 다루는 가장 기본적인 도구인 **소수 판별**, **약수와 배수**, **진법 변환**, **나머지 연산**을 다룹니다. 이후 [최대공약수·체·모듈러 연산](../../lv1-elementary/06-number-theory/)과 Lv2 이상의 정수론으로 이어집니다.

## 한눈에 비교

| 개념 | 하는 일 | 핵심 아이디어 | 시간 |
|---|---|---|---|
| [단순 소수 판별](naive-prime-check/) | n이 소수인지 | 2부터 √n까지 나눠 보기 | O(√n) |
| [약수와 배수](divisors-and-multiples/) | n의 약수를 모두 | `(d, n/d)` 쌍, √n까지만 | O(√n) |
| [진법 변환](base-conversion/) | 수를 다른 진법으로 | 나머지를 모아 뒤집기 / `× b + 자리` | O(자릿수) |
| [나머지 연산](modular-arithmetic/) | 큰 수를 나머지로 계산 | 중간마다 `% m` | O(1) 연산 |

## 읽는 순서

1. [단순 소수 판별](naive-prime-check/): √n 관찰이 이후 약수·소인수분해의 공통 뼈대입니다.
2. [약수와 배수](divisors-and-multiples/)
3. [진법 변환](base-conversion/), [나머지 연산](modular-arithmetic/)

나머지 연산에서 **나눗셈**과 **큰 거듭제곱**은 [Lv2](../../lv2-intermediate/06-number-theory/)에서 다룹니다.
