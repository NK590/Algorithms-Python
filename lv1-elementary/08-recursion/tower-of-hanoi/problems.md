# 연습문제 — 하노이의 탑과 재귀

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 4779 칸토어 집합](https://www.acmicpc.net/problem/4779) | 재귀로 쪼개기 | 길이 3ⁿ 문자열을 가운데를 비우며 3등분. 기저 조건이 길이 1 |
| 2 | [백준 11729 하노이 탑 이동 순서](https://www.acmicpc.net/problem/11729) | 기본형 | 이동 횟수와 순서 출력. 출력이 많으므로 `join`으로 한 번에. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 3 | [백준 1914 하노이 탑](https://www.acmicpc.net/problem/1914) | 큰 n | 횟수는 `2ⁿ − 1` (파이썬 큰 정수), 순서는 n이 작을 때만 출력 |
| 4 | [LeetCode 779 K-th Symbol in Grammar](https://leetcode.com/problems/k-th-symbol-in-grammar/) | k번째만 | 전체를 만들지 않고 위 줄의 어느 칸에서 왔는지로 내려간다. `hanoi_kth_move`와 같은 발상 |
| 5 | [백준 2447 별 찍기 - 10](https://www.acmicpc.net/problem/2447) | 패턴 재귀 | 3×3으로 나눈 가운데 칸을 비우는 재귀 |
| 6 | [백준 1074 Z](https://www.acmicpc.net/problem/1074) | 분할 정복 | 4등분 중 어느 사분면에 있는지로 방문 순서를 센다 |
| 7 | [LeetCode 50 Pow(x, n)](https://leetcode.com/problems/powx-n/) | 반으로 줄이기 | `x^n = (x^(n/2))²`. 재귀 깊이가 log n → [빠른 거듭제곱](../../../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/) |
| 8 | [백준 5904 Moo 게임](https://www.acmicpc.net/problem/5904) | k번째 문자 | 점점 커지는 문자열의 n번째 글자. 어느 구간에 속하는지로 내려간다 |

## 풀이 메모

- 1~3번은 "기저 조건 → 줄이기 → 작은 문제를 믿기" 세 단계를 직접 말로 써 본 뒤 코드를 쓰세요.
- 3번은 입력이 100까지라 이동을 출력할 수 없습니다. 문제의 출력 조건(n ≤ 20일 때만)을 확인하세요.
- 4번과 8번은 **전체를 만들지 않고 목표 위치만 따라 내려가는** 재귀입니다. [solution.py](solution.py)의 `hanoi_kth_move`가 그 예입니다.
