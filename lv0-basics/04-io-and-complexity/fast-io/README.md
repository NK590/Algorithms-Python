---
level: 0
order: 1
tags: [io, python]
prerequisites: []
time: 입력 크기에 비례
space: O(입력 크기)
status: done
---

# Fast I/O (빠른 입출력)

> **한 줄 요약**: 입력이 많을 때 파이썬 기본 `input()`과 `print()`는 느리다. `sys.stdin.readline`과 한 번에 모아 출력하기로 시간을 아낀다.

## 1. 언제 쓰나 (문제 신호)

- 입력이 **수만 줄 이상**이거나, 출력해야 할 줄이 많을 때. ("테스트 케이스 T ≤ 10^5", "쿼리 M ≤ 10^6")
- 알고리즘은 맞는데 **시간 초과**가 나는 경우, 입출력이 병목일 수 있습니다.
- 입력이 **언제 끝나는지 모르는** 문제 (EOF까지 읽기)

## 2. 핵심 아이디어

`input()`은 편리하지만 매번 여러 일을 합니다. 같은 일을 더 가볍게 하는 방법이 몇 가지 있습니다.

| 하고 싶은 일 | 방법 |
|---|---|
| 줄 단위로 읽기 | `input = sys.stdin.readline` (줄바꿈 `\n`이 포함된다) |
| 전부 한 번에 읽기 | `data = sys.stdin.buffer.read().split()` (바이트열 토큰) |
| EOF까지 읽기 | `for line in sys.stdin:` |
| 많이 출력하기 | 리스트에 모았다가 `"\n".join(map(str, values))`을 `print` 한 번으로 |

**출력은 호출 횟수가 비용입니다.** `print`를 값마다 부르면 느리고, 문자열 하나로 합쳐 한 번에 내보내면 훨씬 빠릅니다.

## 3. 손으로 따라가기

다음 입력의 합을 구합니다.

```
2
1 2
3 4
```

| 방법 | 읽는 법 | 결과 |
|---|---|---|
| 줄 단위 | `t = int(readline())` → `2`; `a, b = map(int, readline().split())` → `1 2`, `3 4` | 3, 7 |
| 한 번에 | `data = [2, 1, 2, 3, 4]`; `t = data[0]`; 이후 두 개씩 | 3, 7 |

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
import sys
input = sys.stdin.readline                # 내장 input 을 덮어써서 아래 코드는 그대로 쓴다

def sum_each_test(stream):
    readline = stream.readline
    t = int(readline())
    results = []
    for _ in range(t):
        a, b = map(int, readline().split())   # split() 이 줄바꿈도 제거한다
        results.append(a + b)
    return results

print("\n".join(map(str, results)))       # 출력은 한 번에
```

EOF까지 읽는 문제는 `for line in sys.stdin:`으로 읽고 빈 줄을 건너뜁니다. (`read_pairs_until_eof`)

**측정값** (CPython 3.13, `A B` 형식 50만 줄을 읽어 합 구하기, 이 저장소의 개발 환경에서 한 번 잰 값):

| 방법 | 시간 |
|---|---|
| `input()` | 0.63초 |
| `sys.stdin.readline` | 0.33초 |
| `sys.stdin.buffer.read().split()` | 0.24초 |

**출력** (정수 30만 개): `print`를 30만 번 호출하면 0.33초, `join`으로 합쳐 한 번 출력하면 0.05초였습니다. 환경에 따라 달라지지만 **상대적인 차이**는 일정합니다.

## 5. 복잡도와 입력 크기 가이드

- 입력 크기 N에 비례하는 O(N)이지만, **상수**가 다릅니다. 입력이 10^5줄 안팎이면 `input()`도 대개 통과하고, 10^6줄에서는 차이가 갈립니다.
- 입출력이 많은 문제에서는 `readline`과 한 번에 출력하기를 기본으로 쓰세요. ([파이썬으로 PS 하기](../../../docs/python-for-ps.md))

## 6. 자주 하는 실수

- **줄바꿈 처리**: `readline()`은 `\n`을 포함합니다. 문자열을 읽을 때는 `.rstrip()`을 하세요. 숫자는 `int()`나 `split()`이 알아서 무시합니다.
- **`input`과 `sys.stdin.readline` 섞어 쓰기**: 둘이 버퍼를 따로 쓰는 환경이 있어 일부 줄을 놓칠 수 있습니다. 한 가지로 통일하세요.
- **빈 줄과 EOF**: `readline()`은 EOF에서 빈 문자열 `""`을 돌려줍니다. `int("")`는 에러이므로 EOF 문제는 `for line in sys.stdin`으로 읽으세요.
- **큰 출력을 문자열로 이어 붙이기**: `s += str(x) + "\n"`을 반복하면 느립니다. 리스트에 모아서 `join`하세요.
- **불필요한 `flush`**: 대화형 문제가 아니면 매번 flush할 필요가 없습니다.

## 7. 변형과 응용

- **여러 테스트 케이스**: 케이스마다 결과를 `results`에 모았다가 한 번에 출력
- **격자 입력**: 줄마다 `list(map(int, readline().split()))` ([2차원 배열](../../01-data-structures/two-dimensional-array/))
- PyPy3로 제출하면 입출력도 함께 빨라지는 경우가 많습니다. ([파이썬으로 PS 하기](../../../docs/python-for-ps.md))

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 이어서: [시간 복잡도](../time-complexity/), [구현·시뮬레이션](../../05-implementation/simulation/)
