---
level: 1
order: 3
tags: [two-pointers, range-query, sliding-window]
prerequisites: [array]
time: O(n)
space: O(1)
status: done
---

# Two Pointers (투 포인터)

> **한 줄 요약**: 위치 두 개를 가지고 **한 방향으로만** 움직이면서, 모든 쌍·구간을 보지 않고 O(n)에 답을 찾는다.

## 1. 언제 쓰나 (문제 신호)

- "**정렬된 배열**에서 합이 K인 두 수", "두 용액을 섞어 0에 가장 가깝게"
- "합이 K인 **연속 부분 구간**의 개수", "합이 S 이상인 **가장 짧은 구간**" — 원소가 **모두 양수**일 때
- 두 정렬된 배열을 합치기, 두 배열의 교집합
- N이 10^5~10^6이라 모든 쌍·구간(O(n²))을 볼 수 없을 때

## 2. 핵심 아이디어

**① 양 끝에서 안쪽으로** (정렬된 배열의 두 수 합): `left = 0`, `right = n − 1`에서 시작합니다.

- 합이 `target`보다 **작으면** 더 큰 값이 필요하니 `left`를 늘립니다. 지금의 `left`는 어떤 `right`와도 `target`을 못 만들기 때문에 안전하게 버릴 수 있습니다. (`right`가 가장 큰 후보였는데도 작았으므로)
- **크면** `right`를 줄입니다.
- 둘이 만나면 끝. 각 포인터가 한 방향으로만 가서 **O(n)** 입니다.

**② 같은 방향으로 구간(윈도우) 늘리고 줄이기**: 구간 `[start, end]`의 합을 유지하면서 `end`를 하나씩 늘립니다. 합이 너무 크면 `start`를 늘려 줄입니다. **원소가 모두 양수**라서 "구간을 늘리면 합이 커지고, 줄이면 작아진다"는 단조성이 있기에 `start`를 되돌릴 필요가 없습니다. 둘 다 오른쪽으로만 가므로 O(n)입니다.

**③ 두 배열에 하나씩**: 두 정렬된 배열에 포인터를 하나씩 두고 작은 쪽을 가져갑니다. (병합)

**음수가 섞이면** 단조성이 깨져서 ②는 쓸 수 없습니다. 이때는 [누적 합 + 해시](../prefix-sum/)를 씁니다.

## 3. 손으로 따라가기

**합이 15인 두 수** `[1, 2, 4, 7, 11, 15]`:

| left | right | 합 | 판단 |
|---|---|---|---|
| 0 (1) | 5 (15) | 16 | 크다 → `right = 4` |
| 0 (1) | 4 (11) | 12 | 작다 → `left = 1` |
| 1 (2) | 4 (11) | 13 | 작다 → `left = 2` |
| 2 (4) | 4 (11) | 15 | **찾았다 → (2, 4)** |

**합이 7 이상인 가장 짧은 구간** `[2, 3, 1, 2, 4, 3]`:

| end | 구간 `[start..end]` | 합 | 하는 일 | 최소 길이 |
|---|---|---|---|---|
| 0 | `[2]` | 2 | | - |
| 1 | `[2, 3]` | 5 | | - |
| 2 | `[2, 3, 1]` | 6 | | - |
| 3 | `[2, 3, 1, 2]` | 8 ≥ 7 | 길이 4 기록, `start` 줄임 → 합 6 | 4 |
| 4 | `[3, 1, 2, 4]` | 10 ≥ 7 | 길이 4, 줄임 → `[1, 2, 4]` 합 7 ≥ 7 → 길이 3, 줄임 → 합 6 | 3 |
| 5 | `[2, 4, 3]` | 9 ≥ 7 | 길이 3, 줄임 → `[4, 3]` 합 7 ≥ 7 → 길이 **2**, 줄임 → 합 3 | **2** |

답은 `[4, 3]`의 길이 **2**입니다.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def pair_with_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None

def shortest_subarray_at_least(arr, s):            # arr 의 원소는 모두 양수
    best = total = start = 0
    for end in range(len(arr)):
        total += arr[end]
        while total >= s:                          # 조건이 성립하는 동안 왼쪽을 줄이며 기록
            length = end - start + 1
            if best == 0 or length < best:
                best = length
            total -= arr[start]
            start += 1
    return best
```

`count_subarrays_with_sum`(합이 정확히 target인 구간 수), `merge_sorted`도 있습니다. 직접 실행하면 `N M`과 N개의 양의 정수를 받아 합이 M인 연속 구간의 개수를 출력합니다.

## 5. 복잡도와 입력 크기 가이드

- 두 포인터가 각각 최대 n번씩만 움직이므로 **O(n)** 입니다. n = 10^6도 가능합니다. (정렬이 필요하면 O(n log n))
- 모든 쌍·구간을 보는 O(n²)은 n = 10^5에서 불가능합니다. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))

## 6. 자주 하는 실수

- **음수 원소에 구간 방식 사용**: 단조성이 깨져 틀립니다. 누적 합 + 해시로 바꾸세요.
- **정렬하지 않고 양 끝 방식**: 정렬된 배열이 전제입니다.
- **`start`가 `end`를 넘어감**: 합이 `target`보다 크다고 `start`를 줄이다가 빈 구간이 되면(`start > end`) 합이 0이어야 합니다. 조건 `start <= end`로 막습니다.
- **구간이 없을 때의 출력**: "조건을 만족하는 구간이 없으면 0"인지 확인하세요. 최소 길이 초깃값을 `n + 1`로 두고 마지막에 바꾸는 방법도 있습니다.
- **같은 원소를 두 번 사용**: 두 수의 합에서 `left < right`여야 서로 다른 위치입니다.

## 7. 변형과 응용

- **슬라이딩 윈도우**: 고정 길이/가변 길이 구간을 훑으며 값 유지 → [슬라이딩 윈도우](../../../lv2-intermediate/08-search-techniques/sliding-window/)
- **정렬 + 투 포인터**: 세 수의 합(하나를 고정하고 나머지를 양 끝으로)
- **두 용액처럼 "0에 가장 가까운 합"**: 양 끝 방식에서 합의 절댓값이 최소인 쌍을 갱신
- **병합**: [병합 정렬](../../02-sorting/merge-sort/)의 합치기

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [배열](../../../lv0-basics/01-data-structures/array/)
- 이어서: [슬라이딩 윈도우](../../../lv2-intermediate/08-search-techniques/sliding-window/), [매개변수 탐색](../../../lv2-intermediate/08-search-techniques/parametric-search/)
