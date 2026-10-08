# 연습문제 — 재귀 함수의 구조

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10872 팩토리얼](https://www.acmicpc.net/problem/10872) | 기본형 | [solution.py](solution.py)의 `factorial`/`main()`이 그대로 풀이다. `0! = 1`인 기저 조건 |
| 2 | [백준 10870 피보나치 수 5](https://www.acmicpc.net/problem/10870) | 두 갈래 재귀 | n이 작아서 순진한 재귀로도 풀린다. 호출이 어떻게 늘어나는지 `fibonacci_call_count`로 확인해 보자 |
| 3 | [백준 17478 재귀함수가 뭔가요?](https://www.acmicpc.net/problem/17478) | 깊이에 따른 출력 | 깊이에 따라 들여쓰기가 늘어나는 출력. 재귀 호출 전후에 하는 일을 구분한다 |
| 4 | [백준 25501 재귀의 귀재](https://www.acmicpc.net/problem/25501) | 호출 횟수 세기 | 팰린드롬 판별 재귀가 몇 번 호출되는지 센다 |
| 5 | [백준 4779 칸토어 집합](https://www.acmicpc.net/problem/4779) | 프랙탈 | [solution.py](solution.py)의 `cantor_string`. 가운데 1/3을 비우는 재귀 |
| 6 | [백준 2447 별 찍기 - 10](https://www.acmicpc.net/problem/2447) | 2차원 프랙탈 | 같은 아이디어를 2차원으로. 크기 n을 3으로 나눠 가운데를 비운다 |

## 풀이 메모

- 5번은 입력이 `N`이면 길이 3^N의 문자열입니다. N이 작아서 재귀로 충분합니다.
- 깊이가 큰 문제에서 `RecursionError`가 나면 [파이썬으로 PS 하기](../../../docs/python-for-ps.md)의 재귀 항목을 참고하세요.
