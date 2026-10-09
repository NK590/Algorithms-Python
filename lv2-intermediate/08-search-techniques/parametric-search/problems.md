# 연습문제 — 매개변수 탐색

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Factory Machines](https://cses.fi/problemset/task/1620) | 핵심 연습 | 생산량 판정이 답의 시간에 대해 단조임을 증명한다 |
| 2 | [CSES — Apartments](https://cses.fi/problemset/task/1084) | 선행 연습 | 선행으로 정렬된 후보의 경계를 다룬다 |
| 3 | [LeetCode 875 Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | 최소화 (`first_true`) | 시간 `h` 안에 다 먹을 수 있는 최소 속도. 올림 나눗셈 `ceil` 처리 |
| 4 | [LeetCode 1011 Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | 최대를 최소화 | 하루 적재량의 하한은 가장 무거운 짐, 상한은 전체 합 |
| 5 | [LeetCode 410 Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | 최대를 최소화 | 구간 합의 상한을 정하고 필요한 분할 수가 k 이하인지 판정한다. 원소가 음이 아니어야 이 그리디 판정이 맞다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
