# 연습문제 — 리 차오 트리 심화

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Line Add Get Min](https://judge.yosupo.jp/problem/line_add_get_min) | 핵심 연습 | 중점에서 좋은 직선을 남기고 교차할 수 있는 쪽으로 내려간다 |
| 2 | [Library Checker — Segment Add Get Min](https://judge.yosupo.jp/problem/segment_add_get_min) | 핵심 연습 | 직선이 유효한 x 구간을 함께 제한한다 |
| 3 | [Codeforces 678F Lena and Queries](https://codeforces.com/problemset/problem/678/F) | 직선을 넣고 빼며 `x = q`에서 최댓값 질의 | 삭제가 있는 문제. 오프라인 시간 구간 트리 + 롤백 (`min_over_time`의 형태). 삭제를 직접 구현하지 않고 우회 |
| 4 | [Codeforces 932F Escape Through Leaf](https://codeforces.com/problemset/problem/932/F) | 트리 DP: `dp[v] = min (a_v · b_u + dp[u])`, `u`는 `v`의 서브트리 | 리 차오 트리 병합 또는 작은 쪽을 큰 쪽에 합치기. 서브트리가 연속 구간이 되는 오일러 투어 + 선분 트리와도 푼다 |
| 5 | [Codeforces 1303G Sum of Prefix Sums](https://codeforces.com/problemset/problem/1303/G) | 트리의 모든 경로에 대한 접두사 합의 합 최대화 | [센트로이드 분해](../../02-tree-decomposition/centroid-decomposition/) + 직선으로 바꿔 질의. 경로를 센트로이드에서 양쪽으로 나눠 `직선 ∪ 질의` 구조 |
| 6 | [Codeforces 1175G Yet Another Partiton Problem](https://codeforces.com/problemset/problem/1175/G) | 수열을 `k`개로 나눠 `(구간 길이 × 구간 최솟값)`의 합 최소화 | 단조 스택 + **퍼시스턴트 리 차오 트리**(스택 팝 시 되돌리기). 이 단원에서 가장 어려운 응용 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
