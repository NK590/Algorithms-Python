---
level: 1
order: 1
tags: [range-query, prefix-sum, dp]
prerequisites: [array]
time: 전처리 O(n), 구간 합 쿼리 O(1)
space: O(n)
status: done
---

# Prefix Sum (누적 합)

> **한 줄 요약**: 앞에서부터의 합을 미리 구해 두면, 어떤 구간의 합이든 **두 값의 뺄셈 한 번**(O(1))으로 구할 수 있다.

## 1. 언제 쓰나 (문제 신호)

- "**i번째부터 j번째까지의 합**을 여러 번 묻는다", 질문이 10^5~10^6개
- 배열의 값이 **바뀌지 않는다** (값이 바뀌면 [세그먼트 트리](../../../lv3-advanced/01-range-query-structures/segment-tree/)나 펜윅 트리)
- "합이 K인 **구간의 개수**" (누적 합 + 해시)
- "구간에 **더하는** 연산이 여러 번이고 마지막에만 결과를 본다" (차이 배열)

## 2. 핵심 아이디어

`prefix[i]`를 `arr[0] + … + arr[i−1]`로 정의합니다. (`prefix[0] = 0`)

`arr[left..right]`의 합 = (0부터 right까지의 합) − (0부터 left−1까지의 합) = `prefix[right + 1] − prefix[left]`

맨 앞에 `prefix[0] = 0`을 두는 덕분에 `left = 0`인 구간도 같은 식이 됩니다.

**합이 K인 구간의 개수**: 오른쪽 끝 `j`에서 끝나는 구간 중 합이 K인 것의 수는 `prefix[i] = prefix[j + 1] − K`인 `i`의 수입니다. 지금까지 본 누적 합의 **개수를 딕셔너리에** 세어 두면 한 번 훑어 O(n)입니다. (음수가 섞여 있어도 됩니다)

**차이 배열**(구간 더하기): 구간 `[l, r]`에 `v`를 더하는 일을 `diff[l] += v`, `diff[r + 1] -= v` 두 칸만 바꿔 기록하고, 마지막에 `diff`의 누적 합을 구하면 각 칸의 최종 값이 나옵니다. 누적 합의 "역연산"입니다.

## 3. 손으로 따라가기

`arr = [5, 4, 3, 2, 1]`:

| i | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `prefix[i]` | 0 | 5 | 9 | 12 | 14 | 15 |

`arr[1..3]`(= 4 + 3 + 2)의 합 = `prefix[4] − prefix[1]` = 14 − 5 = **9**.

**합이 7인 구간의 개수** `[3, 4, 7, 2, -3, 1, 4, 2]`는 `[3,4]`, `[7]`, `[7,2,-3,1]`, `[1,4,2]`로 4개입니다. 누적 합을 훑으며 "지금 누적 합 − 7이 지금까지 몇 번 나왔는가"를 더합니다.

| 읽은 값 | 누적 합 | 찾는 값 (누적 합 − 7) | 이전에 나온 횟수 | 지금까지 개수 |
|---|---|---|---|---|
| (시작) | 0 | | | 0 (기록: `{0: 1}`) |
| 3 | 3 | −4 | 0 | 0 |
| 4 | 7 | 0 | 1 | 1 |
| 7 | 14 | 7 | 1 | 2 |
| 2 | 16 | 9 | 0 | 2 |
| −3 | 13 | 6 | 0 | 2 |
| 1 | 14 | 7 | 1 | 3 |
| 4 | 18 | 11 | 0 | 3 |
| 2 | 20 | 13 | 1 | **4** |

**차이 배열** (길이 5, `[0,2]`에 +3, `[1,3]`에 +2): `diff[0] += 3`, `diff[3] -= 3`, `diff[1] += 2`, `diff[4] -= 2` 이므로 `diff = [3, 2, 0, -3, -2, 0]`. 누적 합을 구하면 `[3, 5, 5, 2, 0]`입니다.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def build_prefix(arr):
    prefix = [0] * (len(arr) + 1)
    for i, value in enumerate(arr):
        prefix[i + 1] = prefix[i] + value
    return prefix

def range_sum(prefix, left, right):            # arr[left..right], 양 끝 포함
    return prefix[right + 1] - prefix[left]

def count_subarrays_with_sum(arr, k):
    seen = {0: 1}                               # prefix[0] = 0
    total = count = 0
    for value in arr:
        total += value
        count += seen.get(total - k, 0)         # 합이 k 인 구간이 여기서 끝나는 경우의 수
        seen[total] = seen.get(total, 0) + 1
    return count
```

`apply_range_adds`(차이 배열)도 있습니다. 파이썬에는 `itertools.accumulate`로 누적 합을 만들 수 있습니다. 직접 실행하면 `N M`, N개의 수, M개의 `i j`(1부터)를 받아 구간 합을 출력합니다.

## 5. 복잡도와 입력 크기 가이드

- 전처리 **O(n)**, 질문 하나 **O(1)**, 공간 O(n)입니다. n, Q가 10^6이어도 가능합니다.
- 질문마다 `sum(arr[l:r+1])`을 하면 O(Q·n)이라 n = Q = 10^5에서 시간 초과입니다. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))
- 값이 자주 바뀌면 누적 합을 매번 다시 만들어야 하니 쓰지 못합니다.

## 6. 자주 하는 실수

- **인덱스 한 칸 밀림**: `prefix`는 길이 n+1이고 `prefix[i + 1]`이 `arr[i]`까지의 합입니다. 입력이 1부터라면 `i − 1`로 바꿔 쓰세요.
- **`prefix[0] = 0` 누락**: 맨 앞에서 시작하는 구간을 따로 처리해야 합니다. (딕셔너리 풀이에서 `{0: 1}`을 빼먹으면 첫 구간을 놓칩니다)
- **합이 K인 구간을 투 포인터로**: 음수가 섞이면 투 포인터의 단조성이 깨집니다. 누적 합 + 해시를 쓰세요. ([투 포인터](../two-pointers/))
- **정수 범위**: 파이썬은 문제없지만 다른 언어에서는 누적 합이 `int`를 넘을 수 있습니다.
- **차이 배열의 끝 칸**: `diff[r + 1]`을 쓰므로 길이를 `n + 1`로 잡으세요.

## 7. 변형과 응용

- **2차원 누적 합**: 격자의 부분 직사각형 합 → [2차원 누적 합](../two-dimensional-prefix-sum/)
- **나머지가 같은 누적 합**: 구간 합이 M의 배수인 구간의 수 (같은 나머지를 가진 누적 합의 쌍을 센다)
- **XOR 누적, 개수 누적**: 합 대신 XOR이나 글자별 개수를 누적하면 구간 질의를 같은 방식으로
- **값이 바뀌는 경우**: [세그먼트 트리](../../../lv3-advanced/01-range-query-structures/segment-tree/), [펜윅 트리](../../../lv3-advanced/01-range-query-structures/fenwick-tree/)

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [배열](../../../lv0-basics/01-data-structures/array/)
- 이어서: [2차원 누적 합](../two-dimensional-prefix-sum/), [투 포인터](../two-pointers/), [세그먼트 트리](../../../lv3-advanced/01-range-query-structures/segment-tree/)
