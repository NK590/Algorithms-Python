# 연습문제 — 기울기 트릭

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — NarrowRectangles](https://atcoder.jp/contests/arc070/tasks/arc070_e) | 핵심 연습 | 이웃한 구간의 겹침 제약을 볼록 DP의 이동으로 표현한다 |
| 2 | [AtCoder — Snuketoon](https://atcoder.jp/contests/abc217/tasks/abc217_h) | 핵심 연습 | 기울기가 변하는 점을 두 힙과 오프셋으로 유지한다 |
| 3 | [Codeforces 713C - Sonya and Problem Wihtout a Legend](https://codeforces.com/problemset/problem/713/C) | 수열을 순증가하게 만드는 최소 ±1 횟수 | [solution.py](solution.py)의 `main()`이 같은 형식. `aᵢ − i`로 바꿔 비감소 문제로 |
| 4 | [Codeforces 865D - Buy Low Sell High](https://codeforces.com/problemset/problem/865/D) | 하루 한 주씩 사고팔기, 마지막에 주식이 없어야 함 | 힙 하나로 푸는 그리디가 기울기 트릭의 `L` 힙과 같다 (`max_profit_buy_sell`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
