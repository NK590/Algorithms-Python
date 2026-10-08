---
level: 1
order: 7
tags: [sorting, key, counting-sort]
prerequisites: [merge-sort, set-and-dict]
time: 정렬 O(n log n), 계수 정렬 O(n + k)
space: O(n)
status: done
---

# Sorting in Practice (정렬 활용)

> **한 줄 요약**: 직접 정렬을 구현하는 대신 파이썬의 **`sorted(key=…)`** 로 여러 기준을 걸어 정렬한다. 값의 범위가 작으면 **계수 정렬**이 더 빠르다.

## 1. 언제 쓰나 (문제 신호)

- "**길이순, 같으면 사전순**", "x 오름차순, x가 같으면 y 오름차순", "나이순, 같으면 **가입한 순서**", "큰 수가 되도록 이어 붙이기"
- 정렬한 뒤에 그리디나 이분 탐색, 투 포인터로 이어지는 문제의 첫 단계
- 값의 범위가 작고(예: 1 ~ 10,000) 개수가 많을 때(10^7개) → **계수 정렬**

## 2. 핵심 아이디어

**`sorted(iterable, key=함수)`**: 각 원소에 `key` 함수를 적용한 값으로 비교해서 정렬합니다. 원소 자체는 바뀌지 않습니다. 파이썬의 정렬은 **안정 정렬**(같은 key의 원래 순서 유지)이고 O(n log n)입니다.

- **여러 기준**: key가 **튜플**이면 앞 원소부터 차례로 비교합니다. `key=lambda w: (len(w), w)` → "길이순, 같으면 사전순".
- **내림차순**: `reverse=True`, 또는 숫자라면 key에 `-x`를 씁니다. 기준마다 방향이 다르면 `(−len(w), w)`처럼 부호로 맞춥니다.
- **안정성 이용**: 나이순으로만 정렬해도 같은 나이는 입력 순서(가입 순서)가 유지됩니다. 기준이 여럿이면 **덜 중요한 기준부터 차례로** 여러 번 정렬해도 됩니다.
- **비교 함수가 필요할 때**: "두 수 a, b를 이어 붙인 `ab`와 `ba` 중 큰 쪽이 앞"처럼 key 하나로 표현하기 어려운 규칙은 `functools.cmp_to_key`로 비교 함수를 만들어 넘깁니다.
- **계수 정렬**: 값을 비교하지 않고 **값별 개수**만 세서 순서대로 펼칩니다. 값이 `0..k`이면 O(n + k)입니다.

## 3. 손으로 따라가기

**길이순, 같으면 사전순 + 중복 제거** `["fig", "apple", "fig", "kiwi", "plum", "banana"]`:

| 단계 | 결과 |
|---|---|
| `set`으로 중복 제거 | `{fig, apple, kiwi, plum, banana}` |
| key `(길이, 단어)` | `fig (3,"fig")`, `kiwi (4,"kiwi")`, `plum (4,"plum")`, `apple (5,"apple")`, `banana (6,"banana")` |
| 정렬 | `fig, kiwi, plum, apple, banana` |

**가장 큰 수 만들기** `[3, 30, 34, 5, 9]`: 쌍마다 `a+b`와 `b+a`를 비교합니다. `"3"+"30" = "330"` > `"30"+"3" = "303"`이므로 3이 30보다 앞. `34`와 `3`: `"343"` > `"334"`이므로 34가 3보다 앞. 결국 `9, 5, 34, 3, 30` → **`9534330`**. (단순히 문자열 사전순 내림차순으로 정렬하면 `9, 5, 34, 30, 3`이 되어 `9534303`이고, 이는 정답 `9534330`보다 작습니다)

**계수 정렬** `[3, 1, 3, 0, 1, 3]` (값 범위 0~3): 개수 `count = [1, 2, 0, 3]`(0이 1개, 1이 2개, 2가 0개, 3이 3개) → `[0, 1, 1, 3, 3, 3]`.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def sort_words(words):
    return sorted(set(words), key=lambda word: (len(word), word))   # 길이순, 같으면 사전순

def largest_number(numbers):
    def compare(a, b):
        if a + b > b + a:
            return -1                    # a 가 앞에 오는 쪽이 더 크다
        if a + b < b + a:
            return 1
        return 0
    result = "".join(sorted(map(str, numbers), key=cmp_to_key(compare)))
    return "0" if result.startswith("0") else result

def counting_sort(values, max_value):
    counts = [0] * (max_value + 1)
    for value in values:
        counts[value] += 1
    return [v for v, c in enumerate(counts) for _ in range(c)]
```

`sort_points`, `sort_by_age`(안정 정렬), `sort_digits_descending`도 있습니다. 직접 실행하면 N개의 단어를 받아 정렬·중복 제거한 결과를 출력합니다.

## 5. 복잡도와 입력 크기 가이드

- `sorted`는 **O(n log n)**, 안정 정렬입니다. n = 10^6도 문제없습니다. (key 함수 호출이 n번 더 있으니 가벼워야 합니다)
- **계수 정렬 O(n + k)**: n = 10^7, 값 ≤ 10,000이라면 일반 정렬보다 훨씬 빠르고 메모리도 작습니다. 하지만 k가 크면(10^9) 쓸 수 없습니다.
- 정렬 알고리즘들의 비교는 [정렬 그룹 개요](README.md)를 보세요. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))

## 6. 자주 하는 실수

- **`list.sort()`와 `sorted()` 혼동**: `a.sort()`는 제자리 정렬이고 `None`을 돌려줍니다. `b = a.sort()`로 받으면 `None`입니다.
- **문자열인 숫자를 사전순으로**: `"10" < "9"`입니다. 숫자 기준이면 `int`로 바꿔서 정렬하세요.
- **내림차순과 안정성**: `reverse=True`는 같은 key의 **원래 순서를 유지**합니다. (결과를 단순히 뒤집은 것과 다릅니다)
- **cmp 함수를 `key=`에 직접 전달**: 파이썬 3에는 `cmp=`가 없습니다. `cmp_to_key`로 감싸세요.
- **모두 0인 경우의 "가장 큰 수"**: `"000"`이 아니라 `"0"`이어야 합니다.
- **계수 정렬의 범위**: 음수나 아주 큰 값은 그대로 인덱스로 못 씁니다. 최솟값을 빼서 이동하거나 [좌표 압축](../../../lv2-intermediate/08-search-techniques/coordinate-compression/)을 쓰세요.

## 7. 변형과 응용

- **좌표 압축**: 정렬한 뒤 각 값에 순번을 붙이기 → [좌표 압축](../../../lv2-intermediate/08-search-techniques/coordinate-compression/)
- **정렬 + 이분 탐색 / 투 포인터**: 먼저 정렬해서 다른 기법을 쓸 수 있게 한다 → [이분 탐색](../../03-binary-search/binary-search/), [투 포인터](../../04-range-techniques/two-pointers/)
- **정렬 + 그리디**: 가장 큰/작은 것부터 짝짓기, 마감 순서대로 처리 → [그리디](../../07-algorithm-paradigms/greedy/)

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [병합 정렬](../merge-sort/) (안정 정렬), [set과 dict 활용](../../01-data-structures/set-and-dict/)
- 이어서: [그리디](../../07-algorithm-paradigms/greedy/), [좌표 압축](../../../lv2-intermediate/08-search-techniques/coordinate-compression/)
