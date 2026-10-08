# 구간 다루기 (Range Techniques)

배열의 **연속된 구간**에 대한 질문을 빠르게 처리하는 기법을 모았습니다. 모든 구간을 직접 보면 O(n²)이지만, 미리 계산해 두거나 두 위치를 영리하게 움직이면 O(n)에 끝납니다.

## 한눈에 비교

| 개념 | 풀 수 있는 질문 | 조건 | 시간 |
|---|---|---|---|
| [누적 합](prefix-sum/) | 구간 합을 **여러 번** 묻기, 합이 K인 구간 개수, 구간 더하기(차이 배열) | 값이 바뀌지 않음 | 전처리 O(n), 질문 O(1) |
| [2차원 누적 합](two-dimensional-prefix-sum/) | 격자의 **부분 직사각형** 합 | 값이 바뀌지 않음 | 전처리 O(R×C), 질문 O(1) |
| [투 포인터](two-pointers/) | 합이 K인 두 수, 합이 K인/K 이상인 **연속 구간** | 정렬됨, 또는 **모두 양수** | O(n) |

## 무엇을 쓸까

| 상황 | 선택 |
|---|---|
| 구간 합 질문이 많다 (값은 고정) | **누적 합** |
| 격자의 부분 합 | **2차원 누적 합** |
| 합이 K인 구간의 **개수**, 원소에 **음수가 있다** | 누적 합 + 해시 (`count_subarrays_with_sum`) |
| 합이 K인 구간의 개수, 원소가 **모두 양수** | **투 포인터** (메모리 O(1)) |
| 정렬된 배열에서 합이 K인 두 수 | **투 포인터** (양 끝에서 안쪽으로) |
| 값이 **자주 바뀌며** 구간 합을 묻는다 | [세그먼트 트리](../../lv3-advanced/01-range-query-structures/segment-tree/)·[펜윅 트리](../../lv3-advanced/01-range-query-structures/fenwick-tree/) |

## 읽는 순서

1. [누적 합](prefix-sum/) → [2차원 누적 합](two-dimensional-prefix-sum/)
2. [투 포인터](two-pointers/)

이후 Lv2에서 [슬라이딩 윈도우](../../lv2-intermediate/08-search-techniques/sliding-window/), [모노톤 스택](../../lv2-intermediate/08-search-techniques/monotonic-stack/) 같은 구간 기법으로 이어집니다.
