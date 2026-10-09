---
level: 0
order: 1
tags: [recursion]
prerequisites: []
time: 호출 횟수에 비례
space: O(재귀 깊이)
status: done
---

# Recursion Basics (재귀 함수의 구조)

> **한 줄 요약**: 함수가 **더 작은 문제로 자기 자신을 호출**하고, 더 쪼갤 수 없는 **기저 조건**에서 답을 바로 돌려주며 끝난다.

## 1. 언제 쓰나 (문제 신호)

- 문제가 **같은 모양의 더 작은 문제**로 나뉠 때: 팩토리얼, 피보나치, 자릿수의 합, 문자열 뒤집기
- 구조 자체가 재귀적일 때: 트리, 프랙탈 패턴(칸토어 집합, 별 찍기), 하노이의 탑
- 모든 경우를 나열하는 [순열·조합](../../03-brute-force/permutations-and-combinations/), [백트래킹](../../../lv1-elementary/07-algorithm-paradigms/backtracking/), [DFS](../../../lv1-elementary/05-graph-basics/dfs/)의 바탕

## 2. 핵심 아이디어

재귀 함수에는 반드시 두 부분이 있습니다.

1. **기저 조건(base case)**: 더 이상 호출하지 않고 답을 바로 주는 경우. (`factorial(0) = 1`) 없으면 무한히 호출합니다.
2. **재귀 호출(recursive case)**: **더 작은** 입력으로 자기 자신을 부릅니다. (`n * factorial(n - 1)`) 입력이 기저 조건에 가까워져야 합니다.

호출은 **스택**에 쌓입니다. `factorial(4)`는 `factorial(3)`의 결과를 기다리며 쌓이고, 기저 조건에서 값이 돌아오면 거꾸로 풀립니다. 이 쌓이는 깊이가 파이썬에서는 기본 **1000**까지로 제한됩니다.

**같은 값을 반복해서 계산하면 느려집니다.** 피보나치를 `F(n) = F(n-1) + F(n-2)`로 그대로 재귀하면 같은 `F(k)`를 수없이 다시 구합니다. 한 번 구한 값을 기억(**메모이제이션**)하면 O(n)이 됩니다.

### 무엇을 저장하고 어떻게 움직이나

재귀 함수 한 번은 현재 입력의 작은 부분 문제 하나를 담당합니다. 함수가 무엇을 반환하는지 먼저 약속하고, 더 작은 입력의 답을 이용해 현재 답을 만듭니다. 종료 조건과 매 호출에서 감소하는 값이 있어야 끝납니다.

### 왜 이 방법이 맞는가

기저 사례가 맞고 크기가 작은 모든 입력에서 함수가 맞다고 가정했을 때 현재 입력도 맞게 조립된다면 수학적 귀납법으로 전체를 설명할 수 있습니다. 공유 리스트를 바꾸는 재귀에서는 호출 전 상태로 복원하는 규칙도 이 약속에 포함됩니다.

### 작은 예제로 검산하기

`factorial(3)`은 `3*factorial(2)`, `2*factorial(1)`을 기다린 뒤 아래에서 1, 2, 6을 돌려줍니다. 호출 횟수와 호출 깊이는 다릅니다. 깊이만 큰 DFS는 반복문과 명시적 스택으로 옮기는 편이 안전합니다.

## 3. 손으로 따라가기

**`factorial(4)`**: 호출이 쌓이고(↓), 값이 돌아오며 풀립니다(↑).

| 단계 | 호출 | 상태 |
|---|---|---|
| ↓ | `factorial(4)` | `4 * factorial(3)`을 기다림 |
| ↓ | `factorial(3)` | `3 * factorial(2)`를 기다림 |
| ↓ | `factorial(2)` | `2 * factorial(1)`을 기다림 |
| ↓ | `factorial(1)` | `1 * factorial(0)`을 기다림 |
| ↓ | `factorial(0)` | **기저 조건**: 1을 반환 |
| ↑ | `factorial(1)` | `1 * 1 = 1` |
| ↑ | `factorial(2)` | `2 * 1 = 2` |
| ↑ | `factorial(3)` | `3 * 2 = 6` |
| ↑ | `factorial(4)` | `4 * 6 = 24` |

**피보나치의 호출 횟수** (`fibonacci_call_count`): `fibonacci(n)`이 함수를 부르는 총 횟수는 `2·F(n+1) − 1`입니다.

| n | 5 | 10 | 20 | 25 | 30 |
|---|---|---|---|---|---|
| 호출 횟수 | 15 | 177 | 21,891 | 242,785 | 2,692,537 |

n이 5 늘 때마다 약 11배씩 느는 **지수적 증가**입니다. 메모이제이션을 쓰면 각 n을 한 번씩만 계산합니다.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def factorial(n):
    if n == 0:                      # 기저 조건
        return 1
    return n * factorial(n - 1)     # 더 작은 문제로 호출

def fibonacci_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n < 2:
        return n
    if n not in memo:               # 처음 구하는 값만 계산해서 기억한다
        memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]
```

그 밖에 `sum_of_digits`, `reverse_string`, 칸토어 집합 문자열(`cantor_string`), 재귀 깊이 제한을 보여 주는 `sum_to_recursive`(깊이 5만에서 `RecursionError`)와 반복문 버전 `sum_to_iterative`가 있습니다.

## 5. 복잡도와 입력 크기 가이드

- 시간은 **호출 횟수 × 호출 하나의 비용**입니다. 호출이 한 갈래로 이어지면(팩토리얼) O(n), 두 갈래로 갈라지고 겹치면(순진한 피보나치) 지수적입니다.
- 공간은 **재귀 깊이**입니다. 파이썬의 기본 제한은 1000이라, 깊이가 10^4~10^5가 될 수 있는 입력은 반복문으로 바꾸거나 `sys.setrecursionlimit`을 올려야 합니다. 그래도 깊이가 매우 크면 메모리 문제로 비정상 종료될 수 있습니다. ([파이썬으로 PS 하기](../../../docs/python-for-ps.md))

## 6. 자주 하는 실수

- **기저 조건 누락·오류**: 없으면 `RecursionError`입니다. `factorial`의 기저를 `n == 1`로 쓰면 `factorial(0)`이 끝나지 않습니다.
- **입력이 작아지지 않음**: `factorial(n)`이 `factorial(n)`을 부르면 영원히 돕니다.
- **중복 계산**: 피보나치를 메모 없이 쓰면 n = 40쯤에서 멈춘 듯 느려집니다.
- **재귀 깊이 제한**: 깊이 1000을 넘는 재귀(예: 1부터 n까지 더하기, n = 10^5)는 `RecursionError`입니다.
- **가변 기본 인자**: `def f(n, memo={})`의 `{}`는 함수 정의 때 한 번만 만들어져 호출 사이에 공유됩니다. `None`을 받고 안에서 만드세요.

## 7. 변형과 응용

- **반복문으로 바꾸기**: 꼬리에서 하나만 부르는 재귀는 대부분 반복문으로 바꿀 수 있습니다. (`sum_to_iterative`)
- **메모이제이션 → DP**: [다이나믹 프로그래밍](../../../lv1-elementary/07-algorithm-paradigms/dynamic-programming/)
- **분할 정복**: 문제를 둘로 나눠 각각 재귀로 푸는 [병합 정렬](../../../lv1-elementary/02-sorting/merge-sort/), [하노이의 탑](../../../lv1-elementary/08-recursion/tower-of-hanoi/)

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 이어서: [순열과 조합 나열](../../03-brute-force/permutations-and-combinations/), [하노이의 탑](../../../lv1-elementary/08-recursion/tower-of-hanoi/), [DFS](../../../lv1-elementary/05-graph-basics/dfs/)
