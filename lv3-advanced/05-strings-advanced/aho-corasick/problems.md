# 연습문제 — 아호-코라식

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Counting Patterns](https://cses.fi/problemset/task/2103) | 핵심 연습 | 여러 패턴의 등장 여부를 실패 링크로 전달한다 |
| 2 | [CSES — Pattern Positions](https://cses.fi/problemset/task/2104) | 핵심 연습 | 첫 등장 위치도 상태 정보로 누적한다 |
| 3 | [LeetCode 1032 Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | 글자 스트림 | 글자를 하나씩 넣으며 현재 노드를 유지하고, 그 노드에서 패턴이 끝나는지(`has_output`)를 답한다 |
| 4 | [Codeforces 963D Frequency of String](https://codeforces.com/problemset/problem/963/D) | 패턴별 모든 위치 | 패턴 총 길이의 제약 덕분에 서로 다른 길이가 적다는 점을 쓴다. `find_all`의 출력량 |
| 5 | [Codeforces 346B Lucky Common Subsequence](https://codeforces.com/problemset/problem/346/B) | 패턴 하나의 오토마톤 + DP | 금지 문자열 하나를 부분 문자열로 포함하지 않는 LCS. 오토마톤 노드를 DP 상태에 넣는다 |
| 6 | [Codeforces 86C Genetic engineering](https://codeforces.com/problemset/problem/86/C) | 길이 `L` 문자열 개수 | 패턴이 나타난 곳들로 모든 글자가 덮이는 문자열의 수. 노드와 "아직 덮이지 않은 끝 길이"를 상태로 |
| 7 | [Codeforces 696D Legen...](https://codeforces.com/problemset/problem/696/D) | 오토마톤 + 행렬 거듭제곱 | 길이가 매우 큰 경우. (max, +) 행렬의 거듭제곱. [행렬 거듭제곱](../../07-dp-advanced/matrix-exponentiation/)을 읽은 뒤에 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
