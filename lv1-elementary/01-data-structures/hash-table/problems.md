# 연습문제 — 해시 테이블

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10815 숫자 카드](https://www.acmicpc.net/problem/10815) | 존재 확인 | 카드 N장을 해시에 넣고 M개의 질문에 O(1)씩 답한다. [solution.py](solution.py)의 `main()`이 그대로 풀이다. 리스트의 `in`은 시간 초과다 |
| 2 | [백준 1620 나는야 포켓몬 마스터 이다솜](https://www.acmicpc.net/problem/1620) | 양방향 찾기 | 이름 → 번호, 번호 → 이름을 모두 O(1)에 찾으려면 딕셔너리와 리스트를 함께 쓴다 |
| 3 | [백준 14425 문자열 집합](https://www.acmicpc.net/problem/14425) | 문자열 존재 확인 | 집합에 있는 문자열이 질문 중 몇 개인지 센다 |
| 4 | [LeetCode 1 Two Sum](https://leetcode.com/problems/two-sum/) | 보수 찾기 | 이미 본 값을 기록하고 `target − x`가 있는지 본다 (`two_sum`) |
| 5 | [LeetCode 49 Group Anagrams](https://leetcode.com/problems/group-anagrams/) | 키 설계 | 글자를 정렬한 문자열을 키로 써서 같은 구성끼리 묶는다 (`group_anagrams`) |

## 풀이 메모

- 1번은 입력이 많아서 `sys.stdin.readline`이 필요합니다. 내장 `set`으로 풀면 가장 간단합니다.
- 직접 만든 `HashMap`은 원리를 보이는 용도이고, 제출할 때는 내장 `dict`/`set`을 쓰세요.
