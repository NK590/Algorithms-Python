---
level: 1
order: 2
tags: [range-query, prefix-sum, grid]
prerequisites: [prefix-sum, two-dimensional-array]
time: 전처리 O(R×C), 쿼리 O(1)
space: O(R×C)
status: done
---

# Two-dimensional Prefix Sum (2차원 누적 합)

> **한 줄 요약**: 격자의 "왼쪽 위 모서리부터 (r, c)까지의 직사각형 합"을 미리 구해 두면, **어떤 부분 직사각형의 합이든** 덧셈·뺄셈 네 번(O(1))으로 구한다.

## 1. 언제 쓰나 (문제 신호)

- "N × M 격자에서 **직사각형 구간의 합**을 여러 번 묻는다", 질문이 10^5개 이상
- "k × k 크기의 **정사각형 중 합이 가장 큰 것**", "격자의 부분 합 최댓값"
- 격자의 값이 바뀌지 않을 때. (바뀌면 2차원 펜윅 트리)

## 2. 핵심 아이디어

`prefix[r][c]`를 **격자의 왼쪽 위 `(0,0)`부터 `(r−1, c−1)`까지 직사각형의 합**으로 정의합니다. 위쪽 한 줄과 왼쪽 한 줄을 0으로 두면(크기 `(R+1) × (C+1)`) 가장자리도 같은 식으로 처리됩니다.

**만들기 (포함-배제)**: 한 칸 더 넓힌 직사각형의 합은

```
prefix[r+1][c+1] = prefix[r][c+1]   (위쪽 직사각형)
                 + prefix[r+1][c]   (왼쪽 직사각형)
                 − prefix[r][c]     (둘이 겹친 부분을 두 번 셌으니 한 번 뺀다)
                 + grid[r][c]       (새로 더해지는 칸)
```

**구간 합**: `(r1, c1)`~`(r2, c2)` 직사각형의 합은 큰 직사각형에서 **위쪽과 왼쪽을 빼고**, 두 번 빠진 **왼쪽 위 모서리를 한 번 되돌립니다.**

```
rect_sum = prefix[r2+1][c2+1] − prefix[r1][c2+1] − prefix[r2+1][c1] + prefix[r1][c1]
```

[1차원 누적 합](../prefix-sum/)의 `prefix[right+1] − prefix[left]`를 2차원으로 늘린 것입니다.

## 3. 손으로 따라가기

```
grid = 1 2 4
       3 4 5
       5 6 7
```

| `prefix` | c=0 | c=1 | c=2 | c=3 |
|---|---|---|---|---|
| r=0 | 0 | 0 | 0 | 0 |
| r=1 | 0 | 1 | 3 | 7 |
| r=2 | 0 | 4 | 10 | 19 |
| r=3 | 0 | 9 | 21 | 37 |

예: `prefix[2][2]` = `prefix[1][2]`(3) + `prefix[2][1]`(4) − `prefix[1][1]`(1) + `grid[1][1]`(4) = **10** (= 1+2+3+4).

**오른쪽 아래 2 × 2** (`(1,1)`~`(2,2)`, 값 4+5+6+7 = 22):

`prefix[3][3]` − `prefix[1][3]` − `prefix[3][1]` + `prefix[1][1]` = 37 − 7 − 9 + 1 = **22**.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def build_prefix_2d(grid):
    rows, cols = len(grid), len(grid[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c] + grid[r][c]
    return prefix

def rect_sum(prefix, r1, c1, r2, c2):        # 양 끝 포함, 0부터
    return prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] - prefix[r2 + 1][c1] + prefix[r1][c1]
```

`best_square_sum`(k × k 정사각형 중 합의 최댓값)도 있습니다. 직접 실행하면 `N M`, 격자, `K`, K개의 `i j x y`(1부터)를 받아 직사각형 합을 출력합니다.

## 5. 복잡도와 입력 크기 가이드

- 전처리 **O(R × C)**, 질문 **O(1)**, 공간 O(R × C)입니다.
- 1000 × 1000 격자는 100만 칸이라 파이썬에서 전처리에 1초 안팎이 걸립니다. 질문이 많을수록 이득이 큽니다. ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))
- 질문마다 이중 반복문으로 더하면 O(Q × R × C)라 시간 초과입니다.

## 6. 자주 하는 실수

- **겹친 모서리를 빼먹기**: 만들 때 `− prefix[r][c]`, 구할 때 `+ prefix[r1][c1]`을 놓치면 틀립니다. 작은 격자로 손계산과 비교하세요.
- **인덱스 한 칸 밀림**: `prefix`는 `(R+1) × (C+1)`이고 `grid[r][c]`는 `prefix[r+1][c+1]`에 대응합니다. 문제 입력이 1부터라면 `i − 1`로 바꿉니다.
- **행/열을 섞어 씀**: 입력 `i j x y`가 (행, 열, 행, 열)인지 확인하세요.
- **직사각형이 아닌 입력**: 행마다 길이가 다른 입력은 처리하지 못합니다.
- **격자 값이 바뀌는 문제**에 사용: 값이 바뀔 때마다 다시 만들면 느립니다.

## 7. 변형과 응용

- **합 대신 개수**: "특정 값이 있는 칸의 수"를 세는 격자를 따로 만들어 같은 방식으로
- **슬라이딩 직사각형 / 최대 정사각형 합**: 모든 위치를 O(1) 씩 보는 `best_square_sum`
- **2차원 차이 배열**: 직사각형에 값을 더하는 여러 번의 연산을 한꺼번에 → [누적 합](../prefix-sum/)의 차이 배열을 2차원으로

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [누적 합](../prefix-sum/), [2차원 배열](../../../lv0-basics/01-data-structures/two-dimensional-array/)
- 이어서: [투 포인터](../two-pointers/), [세그먼트 트리](../../../lv3-advanced/01-range-query-structures/segment-tree/)
