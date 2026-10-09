# 연습문제 — 퍼시스턴트 세그먼트 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Range Kth Smallest](https://judge.yosupo.jp/problem/range_kth_smallest) | 핵심 연습 | 두 접두 버전의 개수 차이로 k번째 값을 찾는다 |
| 2 | [SPOJ MKTHNUM - K-th Number](https://www.spoj.com/problems/MKTHNUM/) | 구간 `k`번째로 작은 수 | 가장 기본형. 값 압축 + 앞의 `i`개를 넣은 버전 |
| 3 | [Codeforces 707D Persistent Bookcase](https://codeforces.com/problemset/problem/707/D) | 격자 위 연산들과 "`k`번째 연산 직후 상태로 돌아가기" | 버전이 트리처럼 분기. 오프라인 DFS + 되돌리기, 또는 퍼시스턴트 구조 |
| 4 | [Codeforces 484E Sign on Fence](https://codeforces.com/problemset/problem/484/E) | 구간 안에서 높이 `h` 이상이 이어진 가장 긴 구간 | 높이 순으로 버전을 쌓고 노드에 "왼쪽 연속, 오른쪽 연속, 최대 연속" 을 저장. 답에 대한 이분 탐색 |
| 5 | [Codeforces 464E The Classic Problem](https://codeforces.com/problemset/problem/464/E) | 간선 가중치가 `2^x`인 최단 경로 | 큰 수를 이진수 구간 트리로 표현하고 버전 비교(해시) — 퍼시스턴트 + 해시 + 다익스트라 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
