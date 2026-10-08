# 연습문제 — 트라이

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 14425 문자열 집합](https://www.acmicpc.net/problem/14425) | 정확 일치 | 집합에 속한 문자열 세기. `set`으로도 풀리지만 트라이로 풀어 `insert`와 `in`을 익힌다. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [백준 14426 접두사 찾기](https://www.acmicpc.net/problem/14426) | 접두사 질의 | 집합의 어떤 문자열의 접두사인 질의의 수. `starts_with` |
| 3 | [LeetCode 208 Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | 구현 | `insert`, `search`, `startsWith`. 노드의 존재와 단어의 끝을 구분 |
| 4 | [LeetCode 14 Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | 공통 접두사 | 트라이에서 갈라지기 전까지 내려가기 (`longest_common_prefix`) |
| 5 | [백준 5052 전화번호 목록](https://www.acmicpc.net/problem/5052) | 접두어 검사 | 한 번호가 다른 번호의 접두어이면 NO. 정렬 후 인접 비교 또는 트라이 |
| 6 | [LeetCode 211 Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 와일드카드 | `.`이 어떤 글자든 되는 검색. 모든 자식으로 DFS |
| 7 | [백준 5670 휴대폰 자판](https://www.acmicpc.net/problem/5670) | 노드 정보 | 자동완성 때 눌러야 하는 키 수. 자식이 하나뿐이고 단어가 끝나지 않는 노드는 자동으로 넘어간다 |
| 8 | [백준 3080 아름다운 이름](https://www.acmicpc.net/problem/3080) | 트리 위의 조합 | 같은 접두사를 공유하는 형제 노드들의 순서를 바꾸는 방법의 수를 팩토리얼로 곱한다 |
| 9 | [LeetCode 421 Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | 이진 트라이 | 반대 비트 우선 탐색. `max_xor_pair`와 같다 |
| 10 | [백준 13505 두 수 XOR](https://www.acmicpc.net/problem/13505) | 이진 트라이 | 같은 문제를 입력 형식만 바꾼 것. 시간 제한이 빠듯해 구현 효율을 고민 |
| 11 | [LeetCode 212 Word Search II](https://leetcode.com/problems/word-search-ii/) | 트라이 + 백트래킹 | 격자에서 사전의 단어들을 한꺼번에 찾기. 트라이로 가지치기해서 접두사가 없으면 즉시 중단 |
| 12 | [백준 9202 Boggle](https://www.acmicpc.net/problem/9202) | 트라이 + DFS | 위와 같은 구조에 점수 계산과 여러 테스트 케이스가 붙은 응용 |

## 풀이 메모

- 1번은 `set`이 더 간단하고 빠릅니다([README](README.md#5-복잡도와-입력-크기-가이드)의 측정값). 트라이를 연습하는 목적으로만 풀어 보세요.
- 5번은 정렬한 뒤 인접한 두 번호만 보는 풀이가 더 짧습니다. 트라이로 푼다면 "삽입하는 도중에 ★ 노드를 만나는 경우"와 "삽입이 끝났는데 그 노드에 이미 자식이 있는 경우"를 모두 확인해야 합니다.
- 7번은 노드마다 "자식 수"와 "단어가 끝나는가"만 알면 됩니다. [solution.py](solution.py)의 `longest_common_prefix`와 같은 판단(자식이 하나뿐이고 끝나지 않으면 이어짐)을 모든 단어에 대해 적용합니다.
- 9번과 10번의 파이썬 풀이는 README의 측정값처럼 느립니다. 입력이 10⁵개이면 시간 제한 안에 들어오게 구현을 다듬어야 합니다(리스트 두 개로 표현한 배열 트라이, 값을 비트별 접두사의 `set`으로 처리하는 방법 등).
- 11번은 단어를 찾으면 트라이에서 그 끝 표시를 지워 같은 단어가 두 번 세어지는 것을 막고, 자식이 없어진 노드를 가지치기하면 속도가 크게 개선됩니다.
