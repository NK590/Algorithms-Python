# 연습문제 — 펜윅 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 307 Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 기본형 | 점 갱신 + 구간 합. `FenwickTree.from_list`, `set`, `range_sum` |
| 2 | [백준 2042 구간 합 구하기](https://www.acmicpc.net/problem/2042) | 기본형 | 입력이 매우 크다. [solution.py](solution.py)의 `main()`이 같은 형태. 합이 64비트를 넘지 않는지 확인 |
| 3 | [백준 12837 가계부 (Hard)](https://www.acmicpc.net/problem/12837) | 기본형 | `N`이 100만. 값을 바꾸는 대신 더하는 갱신 |
| 4 | [백준 11658 구간 합 구하기 3](https://www.acmicpc.net/problem/11658) | 2차원 | 점 갱신 + 직사각형 합. `Fenwick2D` |
| 5 | [LeetCode 315 Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 압축 + 개수 세기 | `count_smaller_after` |
| 6 | [백준 1517 버블 소트](https://www.acmicpc.net/problem/1517) | 역순쌍 | 교환 횟수 = 역순쌍의 수. `count_inversions` |
| 7 | [백준 2243 사탕상자](https://www.acmicpc.net/problem/2243) | k번째 수 | 맛 순위별 사탕 개수를 트리에 저장하고 `find_kth`로 꺼낸다 |
| 8 | [백준 12899 데이터 구조](https://www.acmicpc.net/problem/12899) | k번째 수 | 삽입과 "k번째로 작은 수 삭제". 위와 같은 틀 |
| 9 | [백준 1280 나무 심기](https://www.acmicpc.net/problem/1280) | 개수 + 합 | 이미 심은 나무와의 거리의 합. 개수를 센 트리와 좌표의 합을 센 트리 두 개 |
| 10 | [백준 3653 영화 수집](https://www.acmicpc.net/problem/3653) | 위치 관리 | 꺼낸 영화를 맨 위로 보내는 연산을 "빈 칸과 새 칸"으로 바꿔 점 갱신과 구간 합으로 |
| 11 | [백준 10999 구간 합 구하기 2](https://www.acmicpc.net/problem/10999) | 구간 갱신 | 구간 더하기 + 구간 합. `RangeAddFenwick` (또는 [느리게 갱신되는 세그먼트 트리](../lazy-propagation/)) |
| 12 | [LeetCode 493 Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | 변형된 역순쌍 | `a[i] > 2·a[j]`인 쌍. 압축할 때 `2·a[j]`도 함께 좌표에 포함 |
| 13 | [LeetCode 2179 Count Good Triplets in an Array](https://leetcode.com/problems/count-good-triplets-in-an-array/) | 두 순열 | 두 순열에서 모두 순서가 같은 세 쌍. 가운데 원소를 기준으로 왼쪽/오른쪽 개수를 곱한다 |

## 풀이 메모

- 2번과 3번은 `sys.stdin.buffer.read().split()`로 한 번에 읽고, 합 질의의 답을 모아서 한 번에 출력하세요. [solution.py](solution.py)의 `main()`이 그렇게 합니다.
- 4번은 [README](README.md)의 `Fenwick2D.rect_sum`이 포함·배제를 쓰는 방식을 먼저 손으로 확인하세요. [테스트](test_solution.py)가 작은 격자에서 모든 직사각형을 직접 합한 값과 비교합니다.
- 5번~6번은 값의 범위가 큰 경우 [좌표 압축](../../../lv2-intermediate/08-search-techniques/coordinate-compression/)이 먼저입니다. 같은 값을 어떻게 처리할지(`bisect_left`)가 역순쌍의 정의(엄격한 `>`)와 맞는지 확인하세요.
- 7번과 8번의 `find_kth`는 모든 값이 0 이상일 때만 의미가 있습니다. 삭제할 때는 `add(위치, -1)`.
- 9번은 거리 합 `Σ |x − xᵢ|`을 `x`보다 왼쪽에 있는 것과 오른쪽에 있는 것으로 나누어 개수와 좌표 합으로 계산하며, 곱의 `mod`를 주의하세요.
- 11번은 `RangeAddFenwick`가 트리 두 개로 구간 갱신을 처리합니다. 파이썬에서는 이쪽이 [느리게 갱신되는 세그먼트 트리](../lazy-propagation/)보다 훨씬 빠릅니다 (그 문서의 측정값).
