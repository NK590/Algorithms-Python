---
level: 1
order: 2
tags: [search, binary-search, bisect]
prerequisites: [binary-search]
time: O(log n)
space: O(1)
status: done
---

# Lower Bound / Upper Bound (하한과 상한)

> **한 줄 요약**: 정렬된 배열에서 **"x 이상이 처음 나오는 위치"** (lower bound)와 **"x 초과가 처음 나오는 위치"** (upper bound)를 O(log n)에 찾는다. 이 둘의 차이가 x의 개수다.

## 1. 언제 쓰나 (문제 신호)

- "정렬된 배열에서 x가 **몇 개** 있는가"
- "x **이상(또는 초과)** 인 첫 위치", "x를 넣어도 정렬이 유지되는 **삽입 위치**", "x **이하의 가장 큰 값**" (floor), "x **이상의 가장 작은 값**" (ceil)
- "구간 [a, b]에 들어가는 원소의 개수"
- [LIS를 O(n log n)](../../../lv2-intermediate/04-dynamic-programming/lis/)에 구하는 풀이의 핵심 도구

## 2. 핵심 아이디어

**조건이 `False … False True … True`로 갈라질 때, 처음 `True`인 위치**를 찾는 것이 핵심입니다. (`partition_point`)

| 이름 | 조건 `predicate(i)` | 뜻 |
|---|---|---|
| lower bound | `arr[i] >= x` | x 이상이 처음 나오는 위치 |
| upper bound | `arr[i] > x` | x 초과가 처음 나오는 위치 |

정렬된 배열에서 `arr[i] >= x`는 앞쪽이 `False`, 뒤쪽이 `True`로 갈라지므로 이분 탐색이 가능합니다. 모두 `False`이면 결과는 `len(arr)`(끝)입니다.

- **개수**: `upper_bound(x) − lower_bound(x)` = x와 같은 원소의 수
- **구간 [a, b]의 원소 수**: `upper_bound(b) − lower_bound(a)`
- **삽입 위치**: x를 넣어도 정렬이 유지되는 위치는 `lower_bound`(가장 왼쪽) ~ `upper_bound`(가장 오른쪽)

**이분 탐색의 틀**: `True`가 될 수 있는 `mid`는 버리지 않고(`hi = mid`), `False`면 `mid`까지 버립니다(`lo = mid + 1`). 그래서 `lo < hi`로 반복하고, 끝나면 `lo == hi`가 답입니다.

## 3. 손으로 따라가기

`arr = [1, 2, 2, 2, 5, 7]`, `x = 2`:

| 위치 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 값 | 1 | 2 | 2 | 2 | 5 | 7 |
| `arr[i] >= 2` | F | **T** | T | T | T | T |
| `arr[i] > 2` | F | F | F | F | **T** | T |

- lower bound = 첫 `T`의 위치 = **1**, upper bound = **4**, 개수 = 4 − 1 = **3**
- 없는 값 `x = 3`: `arr[i] >= 3`의 첫 `T`는 위치 4(값 5), `arr[i] > 3`의 첫 `T`도 위치 4 → 같으므로 개수 0이고, 삽입 위치는 4

**lower_bound(2)의 이분 탐색 과정**:

| lo | hi | mid | `arr[mid] >= 2`? | 하는 일 |
|---|---|---|---|---|
| 0 | 6 | 3 | T | `hi = 3` |
| 0 | 3 | 1 | T | `hi = 1` |
| 0 | 1 | 0 | F | `lo = 1` |
| 1 | 1 | | | 끝. 답 **1** |

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def partition_point(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid                    # mid 도 답의 후보이므로 버리지 않는다
        else:
            lo = mid + 1
    return lo

def lower_bound(arr, x):
    return partition_point(0, len(arr), lambda i: arr[i] >= x)

def upper_bound(arr, x):
    return partition_point(0, len(arr), lambda i: arr[i] > x)
```

`count_equal`, `count_in_range`, `floor_value`, `ceil_value`도 있습니다. 직접 실행하면 정렬된 N개의 수와 M개의 질문을 받아 각 수가 몇 개인지 출력합니다.

파이썬 표준 라이브러리의 `bisect.bisect_left`가 lower bound, `bisect.bisect_right`가 upper bound와 같습니다. 실전에서는 이것을 쓰세요.

```python
from bisect import bisect_left, bisect_right
count = bisect_right(arr, x) - bisect_left(arr, x)
```

## 5. 복잡도와 입력 크기 가이드

- 한 번에 **O(log n)**, 공간 O(1). 질문이 Q개면 O(Q log n)입니다. n, Q = 10^5~10^6도 안전합니다.
- 정렬은 한 번만(O(n log n)) 하면 됩니다. 질문마다 정렬하면 안 됩니다. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))

## 6. 자주 하는 실수

- **`>=`와 `>`를 바꿔 쓰기**: lower는 `>=`, upper는 `>`입니다. 헷갈리면 "같은 값이 있는 경우의 결과"를 한 번 손으로 확인하세요.
- **끝 처리**: 모든 값이 x보다 작으면 결과는 `len(arr)`입니다. `arr[결과]`를 바로 읽으면 `IndexError`입니다.
- **반환값을 "찾은 위치"로 착각**: lower bound는 x가 **없어도** 위치를 돌려줍니다. 존재 여부는 `i < len(arr) and arr[i] == x`로 따로 확인하세요.
- **`hi = mid - 1`로 쓰기**: 답의 후보인 `mid`를 버리게 됩니다. 이 틀에서는 `hi = mid`입니다.
- **정렬 기준이 다름**: 내림차순 배열이면 조건을 바꿔야 합니다.

## 7. 변형과 응용

- **LIS O(n log n)**: 각 원소를 lower bound 위치에 놓으며 꼬리 배열을 유지 → [LIS](../../../lv2-intermediate/04-dynamic-programming/lis/)
- **매개변수 탐색**: `partition_point`를 **배열이 아닌 판정 함수**에 적용 → [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/)
- **좌표 압축 후 질의**: 정렬한 값에서 위치 구하기 → [좌표 압축](../../../lv2-intermediate/08-search-techniques/coordinate-compression/)

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [이분 탐색](../binary-search/)
- 이어서: [LIS](../../../lv2-intermediate/04-dynamic-programming/lis/), [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/)
