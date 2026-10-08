---
level: 4
order: 10
tags: [data-structure, segment-tree, merge-sort-tree, range-query, order-statistics, bisect]
prerequisites: [segment-tree, binary-search, lower-upper-bound, sort-with-key]
time: 준비 O(n log n), 질의 O(log² n), 갱신 O(n) (C 속도의 리스트 이동), 구간 k 번째 O(log³ n)
space: O(n log n)
status: done
---

# 머지 소트 트리 (Merge Sort Tree)

> **한 줄 요약**: 구간 트리의 각 노드가 **자기 구간의 원소를 정렬한 리스트** 를 들고 있게 한다. 질의 구간을 `O(log n)`개 노드로 쪼개고 각 노드의 리스트에서 이분 탐색하면 "구간에서 `x`보다 작은 수의 개수" 가 `O(log² n)`. 구현이 가장 단순하고 **점 갱신도 된다**.

## 1. 언제 쓰나 (문제 신호)

- "구간 `[l, r]`에서 `x`보다 큰(작은, 이하인) 수의 개수" — 값 조건이 질의마다 달라서 누적 합 하나로는 안 된다
- 같은 구간에서 `x`의 **이전/다음 값**(predecessor / successor), `x`보다 작은 수들의 **합**
- 위의 질의 **사이에 한 원소 값을 바꾼다** (퍼시스턴트·웨이블릿 트리는 갱신을 못 한다)
- 질의가 **온라인** (앞의 답으로 다음 질의를 복원) 이라 오프라인 정렬이 안 된다
- 질의를 모아 정렬할 수 있으면 [펜윅 트리](../../../lv3-advanced/01-range-query-structures/fenwick-tree/)를 쓰는 오프라인 풀이가 더 빠르다
- 정적 배열에서 속도가 중요하면 [웨이블릿 트리](../wavelet-tree/)나 [퍼시스턴트 세그먼트 트리](../persistent-segment-tree/)가 `O(log n)`이다

## 2. 핵심 아이디어

일반 구간 트리의 노드에는 합이나 최솟값처럼 *두 자식의 값에서 곧바로 계산되는 요약* 이 들어간다. 머지 소트 트리의 노드에는 **구간 전체를 정렬한 리스트** 가 들어간다. 요약이 아니라 *원본의 정렬된 사본* 이라서 "임의의 값 `x`와의 비교" 같은 요약으로 못 하는 질문에도 답할 수 있다.

1. **만들기**: 잎은 원소 하나짜리 리스트. 부모의 리스트 = 두 자식 리스트를 **병합** (병합 정렬의 병합 단계. 이미 정렬된 둘이라 선형). 한 층의 리스트 길이 합이 `n`이고 층이 `log n`개라 전체 `O(n log n)` 시간·메모리.
2. **질의 `count_less(l, r, x)`**: 구간 `[l, r)`은 구간 트리의 `O(log n)`개 노드로 정확히 덮인다. 각 노드의 정렬된 리스트에서 `bisect_left(리스트, x)` = "그 노드에서 `x`보다 작은 수의 개수" → 합한다. `O(log n)`개 노드 × 이분 탐색 `O(log n)` = `O(log² n)`.
3. **갱신 `update(i, v)`**: 잎에서 루트까지 `O(log n)`개 조상의 리스트에서 옛 값을 지우고 새 값을 정렬된 자리에 끼워 넣는다. 리스트 원소 이동이 필요해 최악 `O(n)`(루트 리스트)이지만 C 속도의 메모리 이동이라 `n = 10⁵`에서도 가볍다.
4. **구간 `k`번째**: 정렬된 전체 값 중에서 `count_at_most(l, r, 값) ≥ k`인 가장 작은 값을 이분 탐색 → `O(log n)`번 × `O(log² n)` = `O(log³ n)`. 느리지만 갱신이 있는 `k`번째 질의를 구현이 간단하게 처리한다.
5. **합 `sum_less`**: 노드마다 리스트의 접두사 합을 두면 `x`보다 작은 수들의 합도 같은 방식 (이분 탐색한 위치의 접두사 합).

## 3. 손으로 따라가기

배열 `a = [5, 2, 8, 1, 9, 3, 7, 4]` (`n = 8`). 노드 번호는 루트 1, 왼쪽 자식 `2i`, 오른쪽 자식 `2i + 1`, 잎은 8~15.

| 노드 | 구간 | 정렬된 리스트 |
|---|---|---|
| 1 | [0, 8) | 1 2 3 4 5 7 8 9 |
| 2 | [0, 4) | 1 2 5 8 |
| 3 | [4, 8) | 3 4 7 9 |
| 4 | [0, 2) | 2 5 |
| 5 | [2, 4) | 1 8 |
| 6 | [4, 6) | 3 9 |
| 7 | [6, 8) | 4 7 |
| 8~15 | 잎 | 5, 2, 8, 1, 9, 3, 7, 4 |

(모든 층의 리스트 길이를 더하면 `8 × 4 = 32` — 층 4개 × `n`.)

### 질의 `count_less([1, 6), x = 5)`

구간 `[1, 6) = [2, 8, 1, 9, 3]`은 노드 **9**(위치 1: `[2]`), **5**(위치 2~3: `[1, 8]`), **6**(위치 4~5: `[3, 9]`)로 덮인다.

| 노드 | 리스트 | `5` 미만의 개수 (`bisect_left`) |
|---|---|---|
| 9 | [2] | 1 |
| 5 | [1, 8] | 1 |
| 6 | [3, 9] | 1 |

합 **3** (`2, 1, 3`). 같은 노드들에서 `x = 5` 이하의 개수도 3 (`5`는 구간에 없다). `x`보다 작은 수들의 합은 `2 + 1 + 3 = 6`, 이전 값(predecessor) 3, 다음 값(successor) 8.

### 갱신 `update(3, 6)` (`a₃ = 1 → 6`)

잎 11에서 루트까지의 리스트 4개에서 `1`을 지우고 `6`을 끼워 넣는다: 노드 11 `[6]`, 노드 5 `[6, 8]`, 노드 2 `[2, 5, 6, 8]`, 노드 1 `[2, 3, 4, 5, 6, 7, 8, 9]`. 이제 `count_less([1, 6), 5)`는 노드 5에서 0이 되어 합 **2**.

### 구간 `k`번째 (`[1, 6)`, `k = 3`)

구간의 정렬은 `[1, 2, 3, 8, 9]`. 전체 정렬된 값 `[1, 2, 3, 4, 5, 7, 8, 9]` 위에서 이분 탐색: `count_at_most(≤ 4) = 3 ≥ 3`, `count_at_most(≤ 3) = 3 ≥ 3`, `count_at_most(≤ 2) = 2 < 3` → 답 **3**. 매번 `count_at_most`가 `O(log² n)`.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
class MergeSortTree:
    def __init__(self, values):
        size = 1
        while size < max(1, len(values)): size *= 2
        self.tree = [[] for _ in range(2 * size)]
        for i, v in enumerate(values): self.tree[size + i] = [v]
        for i in range(size - 1, 0, -1):
            self.tree[i] = sorted(self.tree[2*i] + self.tree[2*i + 1])   # 이미 정렬된 두 리스트의 병합

    def _nodes(self, left, right):                 # 반열린 [left, right) 를 덮는 노드들 (아래에서 위로)
        left += self.size; right += self.size
        while left < right:
            if left & 1:  yield left;  left += 1
            if right & 1: right -= 1;  yield right
            left //= 2; right //= 2

    def count_less(self, left, right, x):
        return sum(bisect_left(self.tree[node], x) for node in self._nodes(left, right))
```

- `MergeSortTree(values)`: `count_less`, `count_at_most`, `count_in_value_range(l, r, low, high)`, `predecessor`, `successor`, `sum_less`(접두사 합은 처음 쓸 때 만든다), `kth_smallest(l, r, k)`(1부터), `update(i, value)`. 구간은 반열린 `[l, r)`이고 범위를 벗어나면 `IndexError`.
- 정렬은 파이썬의 `sorted`가 합니다. 이미 정렬된 두 구간의 이어 붙임은 Timsort가 선형 시간에 병합하므로 직접 병합을 짜지 않아도 됩니다.
- 직접 실행하면 BOJ 13544 형식 — `N`, 수열, `M`, 질의 `a b c`(직전 답 `last`로 `i = a xor last`, `j = b xor last`, `k = c xor last`를 복원, 1부터) — 를 받아 `a[i..j]`에서 `k`보다 큰 원소의 수를 출력합니다.

## 5. 복잡도와 입력 크기 가이드

- 준비 `O(n log n)`, `count_*`/`predecessor`/`successor`/`sum_less` `O(log² n)`, `kth_smallest` `O(log³ n)`, `update` 최악 `O(n)`. 메모리 `O(n log n)`. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))
- 이 환경에서 측정한 값입니다.

| 작업 | 시간 |
|---|---|
| 준비, `n = 10⁵` (리스트 원소 합계 1,800,000개) | 0.13초 |
| `count_less` 질의 20000개, `n = 10⁵` | 0.20초 |
| `kth_smallest` 질의 2000개, `n = 10⁵` | 0.17초 |
| `update` 1000번, `n = 10⁵` | 0.11초 |

- `n = 10⁵`에서 메모리는 정수 약 180만 개 — 구간 트리 한 층이 `n`이고 층이 18개. `n = 10⁶`은 약 2000만 개로 파이썬에서 부담이 됩니다.
- 갱신 한 번이 평균 0.1밀리초인 이유: 루트 리스트의 중간에서 원소를 지우고 넣는 `list` 연산이 C의 `memmove`로 `10⁵`개 원소를 한 번에 옮기기 때문입니다. `n`이 `10⁶`을 넘으면 이 `O(n)`이 병목이 됩니다.

## 6. 자주 하는 실수

- **`bisect_left`와 `bisect_right`**: `x`보다 *작은* 수의 개수는 `bisect_left`, `x` *이하* 의 개수는 `bisect_right`. "`k`보다 큰 수의 개수" = `(길이) − count_at_most(k)`이지 `(길이) − count_less(k)`가 아닙니다.
- **구간의 열림·닫힘**: 이 구현은 반열린 `[l, r)`입니다. 1부터 닫힌 `[i, j]`로 입력받으면 `[i − 1, j)`로 바꿔서 넘깁니다.
- **크기를 2의 거듭제곱으로 올리지 않음**: 아래에서 위로 올라가는 반복형 구간 트리는 잎의 개수가 2의 거듭제곱일 때 모든 노드가 정확히 자식 두 개의 합입니다. 크기를 올린 빈 잎은 빈 리스트라 질의에 영향을 주지 않습니다.
- **갱신에서 중복 값 지우기**: 리스트에서 값을 지울 때 `bisect_left`로 *하나만* 지웁니다 (`remove`나 값으로 전부 지우면 같은 값이 다른 위치에도 있을 때 틀립니다). 전체 정렬된 값 목록(`kth_smallest`용)도 함께 고쳐야 합니다.
- **접두사 합 캐시를 갱신 후 안 지움**: `update` 뒤에 접두사 합이 낡으면 `sum_less`가 틀립니다. 이 구현은 갱신 때마다 지웁니다.
- **빈 구간**: `count_less(l, l, x)`는 0, `predecessor`는 `None`. `kth_smallest`는 `k`가 `1..길이`를 벗어나면 오류.
- **`kth_smallest`의 이분 탐색 방향**: "`count_at_most ≥ k`인 가장 작은 값" 을 찾아야 합니다. `>`로 쓰면 한 칸 어긋납니다.
- **메모리 폭발**: `n = 10⁶`에서 리스트 20개 층을 모두 들고 있는 것이 부담이면 아래 몇 층을 잘라 내고(작은 구간은 직접 훑기) 쓰거나 웨이블릿 트리로 바꿉니다.

## 7. 변형과 응용

- **분수 계단(fractional cascading)**: 부모 리스트의 각 원소에 "왼쪽/오른쪽 자식에서 이 값 이상인 첫 위치" 를 저장해 두면 루트에서 한 번만 이분 탐색하고 아래는 `O(1)`로 따라가 질의가 `O(log n)`이 됩니다 (구현은 복잡해집니다. [웨이블릿 트리](../wavelet-tree/)가 비슷한 목표를 더 깔끔하게 이룹니다).
- **2차원 점 세기 (오프라인 지배 쌍)**: 점을 `x` 순으로 정렬하고 `y`를 배열 값으로 보면 직사각형 안의 점 수 = 구간 안에서 `y`가 범위 안인 개수.
- **정렬된 블록 리스트**: 노드를 구간 트리가 아니라 크기 `√n`의 블록으로 쪼개면 [제곱근 분할](../../../lv3-advanced/06-query-techniques/sqrt-decomposition/)이 되고, 구현은 더 짧지만 질의가 `O(√n log n)`입니다.
- **BIT 안에 BIT / 정렬된 컨테이너**: 값 범위가 큰 갱신 위주 문제는 노드를 펜윅 트리나 순서 통계 트리([트립](../treap/))로 바꿔 갱신을 `O(log² n)`으로 줄입니다.
- **합 이외의 통계**: 노드 리스트에 접두사 합뿐 아니라 접두사 최솟값 등을 함께 저장해 "`x`보다 작은 수 중 위치가 가장 빠른 것" 같은 질문을 처리합니다.

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [구간 트리](../../../lv3-advanced/01-range-query-structures/segment-tree/), [이분 탐색](../../../lv1-elementary/03-binary-search/binary-search/), [lower / upper bound](../../../lv1-elementary/03-binary-search/lower-upper-bound/)
- 이어서: [웨이블릿 트리](../wavelet-tree/) (같은 질의를 `O(log n)`에), [퍼시스턴트 세그먼트 트리](../persistent-segment-tree/), [트립](../treap/)
