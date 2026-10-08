# 연습문제 — 기울기 트릭

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Codeforces 713C - Sonya and Problem Wihtout a Legend](https://codeforces.com/problemset/problem/713/C) | 수열을 순증가하게 만드는 최소 ±1 횟수 | [solution.py](solution.py)의 `main()`이 같은 형식. `aᵢ − i`로 바꿔 비감소 문제로 |
| 2 | [Codeforces 865D - Buy Low Sell High](https://codeforces.com/problemset/problem/865/D) | 하루 한 주씩 사고팔기, 마지막에 주식이 없어야 함 | 힙 하나로 푸는 그리디가 기울기 트릭의 `L` 힙과 같다 (`max_profit_buy_sell`) |
| 3 | [AtCoder ARC070 E - NarrowRectangles](https://atcoder.jp/contests/arc070/tasks/arc070_e) | 층마다 구간을 옮겨 이웃과 닿게 하는 최소 이동 거리 | 구간 최솟값 연산 (`window_min`)과 `narrow_rectangles` |
| 4 | [AtCoder ABC217 H - Snuketoon](https://atcoder.jp/contests/abc217/tasks/abc217_h) | 시각마다 한 점을 향해 최소 비용으로 위치 유지 | 이동 제한(`window_min`)과 절댓값 더하기(`add_abs`)의 반복 |
| 5 | (직접 만들어 보는 문제) 이웃 차 제한이 있는 수열 | 이웃한 값의 차가 `d` 이하일 때 `aᵢ`와 `bᵢ`의 차이의 합의 최소 | `min_cost_bounded_difference`를 `O(n · 값 범위)` DP와 비교 (테스트가 같은 방식) |

## 풀이 메모

- 1번은 `min_cost_strictly_increasing` 한 줄입니다. 구현을 보지 않고 `add_abs`와 `prefix_min`만 가지고 직접 짜 보세요.
- 2번은 "비싼 날에 팔고, 팔았던 가격을 다시 힙에 넣어 더 비싼 날에 번복할 수 있게 한다" 가 핵심입니다. 이 구현의 `max_profit_buy_sell`이 그 그리디입니다.
- 3, 4번은 변화의 한도가 있는 DP입니다. `window_min(lo, hi)`의 부호(`L`이 `−hi`, `R`이 `−lo`)를 식에서 직접 유도하세요.
