---
level: 0
name: 입문
tier: Bronze
summary: 입출력과 구현, 완전 탐색으로 쉬운 문제를 푼다
---

# Lv0 · 입문 (Bronze)

프로그래밍 문법을 막 익힌 단계입니다. 알고리즘 이름을 외우기보다 "문제를 읽고, 코드로 옮기고, 제한 시간 안에 돌아가는지 가늠하는" 기본기를 만드는 것이 목표입니다.

- **solved.ac 기준**: Bronze 난이도의 문제 (알고리즘별 난이도는 문제에 따라 달라 대략적인 기준입니다)
- **선수 지식**: 변수·조건문·반복문·함수, 리스트 사용법
- **이 레벨을 마치면**: 입력 크기를 보고 완전 탐색이 가능한지 판단하고, 간단한 구현·시뮬레이션 문제를 풀 수 있다

## 개념 목록

<!-- INDEX:START -->
### [자료구조 기초 (Data Structures)](01-data-structures/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Array (배열)](01-data-structures/array/) | `done` | 접근 O(1), 삽입·삭제 O(n) | - |
| [Two-dimensional Array (2차원 배열)](01-data-structures/two-dimensional-array/) | `done` | 칸 접근 O(1), 전체 훑기 O(행 × 열) | [array](01-data-structures/array/) |
| [String Basics (문자열 기초)](01-data-structures/string-basics/) | `done` | 훑기 O(n), 비교 O(n) | [array](01-data-structures/array/) |

### [수학·정수론 기초 (Number Theory Basics)](02-number-theory/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Naive Prime Number Check (단순 소수 판별)](02-number-theory/naive-prime-check/) | `done` | O(√n) | - |
| [Divisors and Multiples (약수와 배수)](02-number-theory/divisors-and-multiples/) | `done` | 약수 구하기 O(√n) | [naive-prime-check](02-number-theory/naive-prime-check/) |
| [Base Conversion (진법 변환)](02-number-theory/base-conversion/) | `done` | O(자릿수) | - |
| [Modular Arithmetic (나머지 연산)](02-number-theory/modular-arithmetic/) | `done` | 연산당 O(1) | - |

### [브루트 포스 (Brute Force)](03-brute-force/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Brute Force (브루트 포스, 완전 탐색)](03-brute-force/brute-force/) | `done` | 경우의 수에 비례 | - |
| [Permutations and Combinations (순열과 조합 나열)](03-brute-force/permutations-and-combinations/) | `done` | 순열 O(n!), 조합 O(C(n, r)), 부분집합 O(2^n) | [brute-force](03-brute-force/brute-force/), [recursion-basics](06-recursion/recursion-basics/) |

### [입출력과 시간 복잡도 (I/O and Complexity)](04-io-and-complexity/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Fast I/O (빠른 입출력)](04-io-and-complexity/fast-io/) | `done` | 입력 크기에 비례 | - |
| [Time Complexity (시간 복잡도와 빅오)](04-io-and-complexity/time-complexity/) | `done` | 해당 없음 (개념) | - |

### [구현·시뮬레이션 (Implementation)](05-implementation/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Implementation and Simulation (구현·시뮬레이션)](05-implementation/simulation/) | `done` | 시뮬레이션 단계 수에 비례 | [two-dimensional-array](01-data-structures/two-dimensional-array/) |
| [String Processing (문자열 처리)](05-implementation/string-processing/) | `done` | O(문자열 길이) | [string-basics](01-data-structures/string-basics/) |

### [재귀 (Recursion)](06-recursion/)

| 개념 | 상태 | 시간 복잡도 | 선행 개념 |
|---|---|---|---|
| [Recursion Basics (재귀 함수의 구조)](06-recursion/recursion-basics/) | `done` | 호출 횟수에 비례 | - |
<!-- INDEX:END -->

전체 커리큘럼과 개념 사이의 선행 관계는 [ROADMAP](../ROADMAP.md)에서 볼 수 있습니다.
