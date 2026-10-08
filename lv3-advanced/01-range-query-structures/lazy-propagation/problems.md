# 연습문제 — 느리게 갱신되는 세그먼트 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 16975 수열과 쿼리 21](https://www.acmicpc.net/problem/16975) | 구간 더하기 + 점 질의 | 질의가 한 칸이라 차분 배열 + 펜윅 트리로도 풀린다. 느리게 갱신되는 트리와 비교 |
| 2 | [백준 10999 구간 합 구하기 2](https://www.acmicpc.net/problem/10999) | 구간 더하기 + 구간 합 | 기본형. [solution.py](solution.py)의 `main()`이 같은 형태 (`range_add_range_sum`) |
| 3 | [백준 1395 스위치](https://www.acmicpc.net/problem/1395) | 구간 뒤집기 + 개수 | 갱신 `flip`, `apply = 길이 − x`, `compose = xor`. 항등원은 `False` |
| 4 | [백준 12844 XOR](https://www.acmicpc.net/problem/12844) | 구간 XOR + 구간 XOR 합 | 구간 길이가 홀수일 때만 질의 값이 바뀐다 |
| 5 | [LeetCode 699 Falling Squares](https://leetcode.com/problems/falling-squares/) | 구간 대입 + 구간 최댓값 | 떨어진 사각형의 윗면이 구간의 높이가 된다. 좌표 압축 + 대입 갱신 |
| 6 | [LeetCode 732 My Calendar III](https://leetcode.com/problems/my-calendar-iii/) | 구간 더하기 + 전체 최댓값 | 겹치는 일정의 최대 개수. 동적 개설이거나 좌표 압축 |
| 7 | [백준 12895 화려한 마을](https://www.acmicpc.net/problem/12895) | 구간 대입 + 비트마스크 | 칠한 색 집합을 비트마스크로 저장한 `or` 트리 + 대입 갱신 |
| 8 | [백준 13925 수열과 쿼리 13](https://www.acmicpc.net/problem/13925) | 아핀 갱신 | 더하기·곱하기·대입이 섞인 갱신을 `(a, b)`로 일반화. 합성 순서 연습 |

## 풀이 메모

- 2번은 [`RangeAddFenwick`](../fenwick-tree/solution.py)로도 풀립니다. 두 구현의 속도를 비교해 보세요 ([README](README.md#5-복잡도와-입력-크기-가이드)에서 약 5배 차이).
- 3번에서 불리언 갱신의 합성은 `xor`입니다. 같은 구간을 두 번 뒤집으면 원래대로 돌아오므로 표시가 사라져야 합니다.
- 5번, 6번은 좌표가 크므로 [좌표 압축](../../../lv2-intermediate/08-search-techniques/coordinate-compression/)이 먼저 필요합니다 (오프라인으로 모든 구간의 끝점을 모은다).
- 대입과 더하기를 섞는 8번을 풀 때, 합성 공식 `compose((a₁, b₁), (a₂, b₂)) = (a₁a₂, a₁b₂ + b₁)`을 종이에 먼저 유도해 보세요. [테스트](test_solution.py)의 `test_non_commutative_affine_updates`가 같은 구성을 확인합니다.
- 입력이 크면 재귀 구현은 파이썬에서 시간 초과가 날 수 있으니, 질의 수가 10⁵를 넘는 문제는 반복문 구현이나 다른 접근(제곱근 분할 등)을 고려하세요.
