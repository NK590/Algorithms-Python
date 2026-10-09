# 연습문제 — 모스 알고리즘

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Distinct Numbers](https://cses.fi/problemset/task/1621) | 선행 연습 | 선행으로 서로 다른 값의 수를 빈도 상태로 유지한다 |
| 2 | [SPOJ DQUERY](https://www.spoj.com/problems/DQUERY/) | 서로 다른 값의 수 | 모스의 기본형. 입력이 1부터이고 양 끝을 포함한다 |
| 3 | [Codeforces 220B Little Elephant and Array](https://codeforces.com/problemset/problem/220/B) | `값 == 등장 횟수`인 값의 수 | 횟수가 바뀔 때마다 조건을 만족하는 값의 수를 같이 갱신한다 |
| 4 | [Codeforces 617E XOR and Favorite Number](https://codeforces.com/problemset/problem/617/E) | 구간 XOR이 `k`인 부분 구간의 수 | 접두사 XOR을 만들고 쌍의 수를 센다. `add` 때 `count[x ^ k]`를 더한다 |
| 5 | [Codeforces 86D Powerful array](https://codeforces.com/problemset/problem/86/D) | `Σ (등장 횟수)² × 값` | 값이 큰 정수일 때 오버플로가 없는 파이썬의 이점. `add`/`remove`의 증분 계산 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
