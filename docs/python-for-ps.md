# 파이썬으로 PS/CP 하기

알고리즘은 같아도 파이썬은 C++보다 느리고 기본 설정이 PS에 맞지 않아서, 몇 가지를 알고 시작하는 편이 좋습니다. (Python 3.9 이상 기준이며, 채점 사이트의 파이썬 버전은 다를 수 있습니다.)

## 1. 빠른 입출력

```python
import sys

input = sys.stdin.readline          # 내장 input() 보다 훨씬 빠르다

n = int(input())
arr = list(map(int, input().split()))
word = input().rstrip()             # readline 은 줄바꿈 문자를 포함하므로 문자열은 rstrip/strip
```

- 입력이 매우 크면 한 번에 읽어서 쪼개는 방법이 더 빠릅니다.

  ```python
  data = sys.stdin.buffer.read().split()   # 바이트열 토큰 리스트
  n = int(data[0])
  ```

- 출력은 `print`를 여러 번 부르지 말고 모아서 한 번에 내보냅니다.

  ```python
  out = []
  for ...:
      out.append(str(value))
  print("\n".join(out))
  ```

## 2. 재귀

- CPython의 기본 재귀 한도는 1000입니다. `sys.setrecursionlimit(10**6)`으로 올릴 수 있지만, 정말 깊은 재귀는 한도를 올려도 메모리·스택 문제로 비정상 종료될 수 있습니다.
- DFS처럼 깊이가 입력 크기(예: 10^5)에 비례하는 재귀는 **스택을 직접 쓰는 반복문**으로 바꾸는 것이 가장 안전합니다.
- 메모이제이션 재귀 DP(`functools.lru_cache`)도 깊이 제한에 걸립니다. 상태 순서가 분명하면 반복문(bottom-up)으로 쓰는 편이 빠르고 안전합니다.

## 3. CPython vs PyPy

백준(BOJ) 같은 사이트에서는 **Python 3(CPython)** 과 **PyPy3** 중에서 골라 제출할 수 있습니다.

- 반복문과 정수 연산이 많은 코드는 PyPy가 훨씬 빠른 경우가 많습니다.
- `sort`, `bisect`처럼 내장 함수 호출 위주인 코드는 둘의 차이가 작거나 CPython이 더 빠를 수 있고, PyPy는 메모리를 더 쓰는 경향이 있습니다.
- 시간 초과가 나면 같은 코드를 두 인터프리터로 모두 제출해 보는 것이 가장 확실합니다.
- numpy 같은 외부 라이브러리는 대부분의 채점 사이트에서 쓸 수 없습니다.

## 4. 자주 쓰는 표준 라이브러리

| 모듈 | 용도 |
|---|---|
| `collections.deque` | 큐/덱 (양 끝 O(1)). BFS, 슬라이딩 윈도우 |
| `collections.defaultdict`, `Counter` | 기본값이 있는 딕셔너리, 빈도 세기 |
| `heapq` | 우선순위 큐 (최소 힙). 최대 힙은 값에 `-`를 붙여 넣는다 |
| `bisect` | `bisect_left` / `bisect_right`로 이분 탐색 (lower/upper bound) |
| `itertools` | `permutations`, `combinations`, `product`, `accumulate` (누적 합) |
| `functools` | `lru_cache` / `cache` (메모이제이션) |
| `math` | `gcd`, `lcm`, `isqrt`(정수 제곱근), `comb`, `perm`, `inf` |
| `pow(a, b, m)` | 모듈러 거듭제곱. `pow(a, -1, m)`은 모듈러 역원 (a와 m이 서로소일 때) |

## 5. 자주 하는 실수

- **2차원 리스트 만들기**: `[[0] * m] * n`은 같은 행을 n번 공유합니다. 반드시 `[[0] * m for _ in range(n)]`.
- **큐를 리스트로 쓰기**: `list.pop(0)`, `list.insert(0, x)`는 O(n)입니다. `deque`를 쓰세요.
- **리스트에서 `in` 검사**: O(n)입니다. 자주 확인하면 `set`/`dict`로 바꾸세요.
- **문자열을 반복해서 `+=`**: 매번 복사됩니다. 리스트에 모았다가 `"".join(...)`.
- **나눗셈과 나머지**: `//`는 내림 나눗셈이라 `-7 // 2 == -4`이고, `%`의 결과는 제수의 부호를 따라 `-7 % 3 == 2`입니다. C++과 다릅니다.
- **정수 오버플로**: 파이썬 정수는 오버플로가 없지만, 아주 큰 수는 연산이 느려집니다. 모듈러 문제에서는 중간마다 `% MOD`를 하세요.
- **무한대**: `float("inf")`는 정수와 섞이면 실수 연산이 됩니다. 정수만 쓰려면 `10**18` 같은 큰 정수를 `INF`로 둡니다.

## 6. 속도 팁

- 전역 변수보다 **함수 안의 지역 변수**가 빠릅니다. 코드를 `main()` 안에 두세요.
- `for` + `append`보다 리스트 컴프리헨션이 보통 빠릅니다.
- 반복문 안에서 `arr.append`처럼 속성을 계속 조회한다면 `append = arr.append`로 미리 꺼내 둘 수 있습니다.
- 정렬은 `cmp` 함수 대신 `key=`를 쓰세요.
- 시간 제한 감각은 [복잡도 치트시트](complexity-cheatsheet.md)를 참고하세요.

## 7. 이 저장소의 `solution.py` 규칙

- 알고리즘은 **함수**로 작성하고 입력은 인자로 받습니다. 그래야 테스트에서 불러다 쓸 수 있습니다.
- 표준 입력을 읽는 코드와 예제 실행은 `if __name__ == "__main__":` 아래에 둡니다. (모듈을 불러올 때 입력을 기다리거나 출력을 쏟아내지 않도록)
- 자세한 작성법은 [CONTRIBUTING](../CONTRIBUTING.md)과 [문서 템플릿](TEMPLATE/)을 참고하세요.
