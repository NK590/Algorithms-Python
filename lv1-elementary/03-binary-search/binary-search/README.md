---
level: 1
order: 1
tags: [search, binary-search]
prerequisites: [array]
time: O(log n)
space: O(1)
status: done
---

# Binary Search (이분 탐색)

> **한 줄 요약**: **정렬된** 배열에서 가운데 값과 비교해 탐색 범위를 절반씩 버려 가며 값을 찾는다. n = 10^9도 약 30번이면 끝난다.

## 1. 언제 쓰나 (문제 신호)

- "**정렬된** 배열에서 값을 찾기", "이 수가 있는가?" (질문이 매우 많을 때)
- N이 10^5~10^9로 커서 처음부터 훑는 O(n)이 부담될 때
- 배열이 없어도 "**답이 클수록 조건을 만족하기 쉬워진다**(단조성)"면 답의 범위를 이분 탐색할 수 있습니다. ([lower/upper bound](../lower-upper-bound/), [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/))

## 2. 핵심 아이디어

배열이 정렬되어 있으므로 가운데 값 `arr[mid]`와 `target`을 비교하면 **한쪽 절반을 통째로 버릴 수** 있습니다.

- `arr[mid] == target` → 찾았다.
- `arr[mid] < target` → 답은 오른쪽에만 있을 수 있다 → `lo = mid + 1`
- `arr[mid] > target` → 답은 왼쪽에만 있을 수 있다 → `hi = mid - 1`

탐색 범위 `[lo, hi]`가 매번 절반으로 줄어들어, 길이 n인 배열에서 많아야 `⌊log₂ n⌋ + 1`번 들여다봅니다. 범위가 비면(`lo > hi`) 없는 것입니다.

**불변식**: "답이 있다면 항상 `arr[lo..hi]` 안에 있다." 모든 버그는 이 구간을 잘못 줄일 때(`mid`를 포함할지, 말지) 생깁니다.

**배열 없이 쓰기**: "x * x ≤ n인 가장 큰 x" 같이 조건이 `True…True False…False`로 갈라지면 같은 방식으로 경계를 찾을 수 있습니다. (`integer_sqrt`)

### 무엇을 저장하고 어떻게 움직이나

탐색할 값이 있을 수 있는 구간을 유지하고 중간값과 비교해 절반을 버립니다. 값이 정렬돼 있다는 조건이 어느 절반을 버려도 되는지 보장합니다. 닫힌 구간인지 반열린 구간인지 먼저 하나를 선택하고 갱신 규칙을 일관되게 씁니다.

### 왜 이 방법이 맞는가

버리는 구간에는 답이 없고 남기는 구간에는 답의 가능성이 모두 남는다는 불변식을 지킵니다. 매번 구간 길이가 줄어 O(log n)번 후 종료합니다. 단순 존재 검사와 첫 등장·마지막 등장 위치 찾기는 동률 처리 규칙이 다릅니다.

### 작은 예제로 검산하기

`[1,3,3,7]`에서 3을 찾았다고 중간 인덱스를 즉시 반환하면 첫 위치인지 알 수 없습니다. 첫 위치가 필요하면 동률에서도 왼쪽 가능성을 유지해야 합니다. 빈 배열에서 중간값을 읽지 않는 종료 조건도 확인하세요.

## 3. 손으로 따라가기

`arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]`에서 `23`을 찾습니다.

| 단계 | lo | hi | mid | `arr[mid]` | 판단 |
|---|---|---|---|---|---|
| 1 | 0 | 9 | 4 | 16 | 16 < 23 → `lo = 5` |
| 2 | 5 | 9 | 7 | 56 | 56 > 23 → `hi = 6` |
| 3 | 5 | 6 | 5 | 23 | **찾았다 → 인덱스 5** |

없는 값 `7`을 찾으면:

| 단계 | lo | hi | mid | `arr[mid]` | 판단 |
|---|---|---|---|---|---|
| 1 | 0 | 9 | 4 | 16 | 16 > 7 → `hi = 3` |
| 2 | 0 | 3 | 1 | 5 | 5 < 7 → `lo = 2` |
| 3 | 2 | 3 | 2 | 8 | 8 > 7 → `hi = 1` |
| 끝 | 2 | 1 | | | `lo > hi` → **없음, −1** |

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1              # 답이 있다면 arr[lo..hi] 안에 있다
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1                   # 가운데보다 작은 쪽은 모두 버린다
        else:
            hi = mid - 1
    return -1
```

`binary_search_recursive`(재귀 버전), `binary_search_steps`(비교 횟수), `integer_sqrt`(배열 없는 이분 탐색)도 있습니다. 직접 실행하면 `N M`, 정렬된 N개의 수, M개의 질문을 받아 각 질문의 수가 있으면 1, 없으면 0을 출력합니다.

실전에서는 표준 라이브러리의 `bisect`를 쓰기도 합니다. ([lower/upper bound](../lower-upper-bound/))

## 5. 복잡도와 입력 크기 가이드

- **시간 O(log n)**, 공간 O(1). 질문이 Q개라면 O(Q log n)입니다.
- n = 10^9도 30번 안팎이면 끝납니다. 정렬 비용 O(n log n)은 한 번만 내면 됩니다. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))
- 질문이 몇 번 안 되고 n이 작으면 그냥 `in`으로 찾는 것이 간단합니다. 질문이 많고 값이 큰 범위면 `set`([해시](../../01-data-structures/set-and-dict/))이 O(1)이라 더 빠를 수 있지만, 이분 탐색은 **"x 이상 첫 위치"처럼 순서가 필요한 질문**에 강합니다.

## 6. 자주 하는 실수

- **정렬되지 않은 배열에 사용**: 조용히 틀린 답이 나옵니다. 먼저 정렬하세요.
- **종료 조건과 갱신 불일치**: `while lo <= hi`면 `hi = mid - 1`, `while lo < hi`면 `hi = mid`처럼 짝이 맞아야 합니다. 어긋나면 무한 반복하거나 마지막 원소를 놓칩니다.
- **`lo = mid`로 갱신**: `mid`가 `lo`와 같아 구간이 줄지 않으면 무한 반복합니다. 올림(`(lo + hi + 1) // 2`)과 짝을 맞추는 경우만 허용됩니다.
- **중복 값에서 위치 해석**: 같은 값이 여럿일 때 반환되는 위치는 정해져 있지 않습니다. 첫 위치·마지막 위치가 필요하면 [lower/upper bound](../lower-upper-bound/)입니다.
- **`(lo + hi) // 2` 오버플로**: C++ 등에서는 `lo + (hi - lo) // 2`로 씁니다. 파이썬은 정수 크기 제한이 없어 괜찮습니다.

## 7. 변형과 응용

- **lower bound / upper bound**: 같은 값 중 첫/끝 위치, 삽입 위치 → [lower/upper bound](../lower-upper-bound/)
- **매개변수 탐색**: "이 값이 가능한가?"를 판정하는 함수로 답의 범위를 이분 탐색 → [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/)
- **LIS를 O(n log n)에**: [LIS](../../../lv2-intermediate/04-dynamic-programming/lis/)

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [배열](../../../lv0-basics/01-data-structures/array/)
- 이어서: [lower/upper bound](../lower-upper-bound/), [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/)
