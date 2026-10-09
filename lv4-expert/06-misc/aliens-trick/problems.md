# 연습문제 — 에일리언 트릭

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Projects](https://cses.fi/problemset/task/1140) | 선행 연습 | 선행으로 구간 선택 DP를 만들고 선택 개수 상태의 비용을 살핀다 |
| 2 | [Codeforces 958E2 Guard Duty (medium)](https://codeforces.com/problemset/problem/958/E2) | 인접하지 않은 간선 `k`개 고르기, 합 최소 (`k` 큼) | 최소화 + 볼록. 간선이 양 끝점을 공유하지 않아야 하므로 완화 DP는 `i`번째 간선을 쓰는지만 추적 |
| 3 | [Codeforces 321E Ciel and Gondolas](https://codeforces.com/problemset/problem/321/E) | 수열을 `k`개 구간으로 나눠 구간 비용 합 최소 | 비용의 사각 부등식과 개수별 최적 비용의 볼록성을 확인한다. 벌점 DP는 같은 층의 이전 상태에 의존하므로, 일반적인 분할 정복 DP 최적화를 그대로 적용하지 않는다 |
| 4 | [Codeforces 739E Gosha is hunting](https://codeforces.com/problemset/problem/739/E) | 두 종류의 포획 도구를 각각 `a`개, `b`개 쓰는 기대값 최대화 | **제약이 두 개**: 한 종류는 `λ`로 완화하고 다른 종류는 `O(n²)` DP, 또는 `λ` 두 개(중첩 이분 탐색). 동점 처리가 특히 까다롭다 |
| 5 | [Codeforces 1279F New Year and Handle Change](https://codeforces.com/problemset/problem/1279/F) | 길이 `l`짜리 구간 `k`개로 문자열 덮기 | 덮은 구간 수 `k` 이하 제약. 개수가 늘수록 이득이 줄어드는 볼록 구조. 완화 DP `O(n)` |
| 6 | [IOI 2016 Aliens (oj.uz)](https://oj.uz/problem/view/IOI16_aliens) | 점들을 `k`개의 정사각형으로 덮는 최소 총 면적 | 에일리언 트릭의 원조. 점을 정렬·불필요한 점 제거 → 완화 DP를 볼록 껍질 트릭으로 `O(n)` → 이분 탐색 (제곱합 구간 나누기와 같은 구조) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
