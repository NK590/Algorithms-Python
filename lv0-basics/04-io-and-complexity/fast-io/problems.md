# 연습문제 — 빠른 입출력

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 15552 빠른 A+B](https://www.acmicpc.net/problem/15552) | 기본형 | 테스트 케이스가 많다. `input()`과 `print()`를 그대로 쓰면 시간 초과가 날 수 있다. [solution.py](solution.py)의 `main()`이 이 형태를 처리한다 |
| 2 | [백준 10951 A+B - 4](https://www.acmicpc.net/problem/10951) | EOF 읽기 | 입력의 끝까지 읽는다. `read_pairs_until_eof` |
| 3 | [백준 11021 A+B - 7](https://www.acmicpc.net/problem/11021) | 출력 형식 | `Case #x: y` 형식으로 많은 줄을 출력한다. 문자열을 모아 한 번에 출력한다 |
| 4 | [백준 11718 그대로 출력하기](https://www.acmicpc.net/problem/11718) | EOF 줄 단위 | 줄 수를 모르는 입력을 그대로 출력한다 |
| 5 | [백준 11719 그대로 출력하기 2](https://www.acmicpc.net/problem/11719) | 공백 보존 | 앞뒤 공백까지 그대로 출력해야 한다. `rstrip()`을 함부로 쓰면 틀린다 |

## 풀이 메모

- 1번은 처음에 `input()`으로 풀어 보고, `sys.stdin.readline`으로 바꾼 뒤 시간을 비교해 보세요.
- 5번은 줄바꿈 문자(`\n`)만 제거하고 공백은 남겨야 하므로 `rstrip("\n")`을 사용합니다.
