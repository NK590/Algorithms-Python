# 연습문제 — 아호-코라식

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 9250 문자열 집합 판별](https://www.acmicpc.net/problem/9250) | 하나라도 포함? | 기본형. [solution.py](solution.py)의 `main()`이 같은 형태. `contains_any` |
| 2 | [LeetCode 1032 Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | 글자 스트림 | 글자를 하나씩 넣으며 현재 노드를 유지하고, 그 노드에서 패턴이 끝나는지(`has_output`)를 답한다 |
| 3 | [백준 10256 돌연변이](https://www.acmicpc.net/problem/10256) | 많은 패턴의 등장 횟수 | 마커의 모든 부분 뒤집기가 만드는 패턴을 모두 넣고 DNA에서 센다. 중복되는 패턴 처리 |
| 4 | [Codeforces 963D Frequency of String](https://codeforces.com/problemset/problem/963/D) | 패턴별 모든 위치 | 패턴 총 길이의 제약 덕분에 서로 다른 길이가 적다는 점을 쓴다. `find_all`의 출력량 |
| 5 | [Codeforces 346B Lucky Common Subsequence](https://codeforces.com/problemset/problem/346/B) | 패턴 하나의 오토마톤 + DP | 금지 문자열 하나를 부분 문자열로 포함하지 않는 LCS. 오토마톤 노드를 DP 상태에 넣는다 |
| 6 | [Codeforces 86C Genetic engineering](https://codeforces.com/problemset/problem/86/C) | 길이 `L` 문자열 개수 | 패턴이 나타난 곳들로 모든 글자가 덮이는 문자열의 수. 노드와 "아직 덮이지 않은 끝 길이"를 상태로 |
| 7 | [Codeforces 696D Legen...](https://codeforces.com/problemset/problem/696/D) | 오토마톤 + 행렬 거듭제곱 | 길이가 매우 큰 경우. (max, +) 행렬의 거듭제곱. [행렬 거듭제곱](../../07-dp-advanced/matrix-exponentiation/)을 읽은 뒤에 |

## 풀이 메모

- 1번은 `contains_any`면 충분합니다. 먼저 패턴마다 `in`으로 검사하는 풀이와 시간을 비교해 보세요(질의가 크고 패턴이 많으면 차이가 큽니다).
- 2번은 질의된 글자들의 **접미사**가 단어인지를 묻습니다. 단어를 그대로 오토마톤에 넣고 현재 노드를 계속 유지하면, 새 글자를 읽은 뒤 `has_output`이 곧 답입니다.
- 5번, 6번, 7번은 "오토마톤의 노드 = DP 상태"를 연습하는 문제입니다. 먼저 [KMP 오토마톤](../../../lv2-intermediate/07-strings/kmp/)으로 패턴 하나만 처리해 보고 여러 개로 늘리세요.
- 같은 문제를 [트라이](../../../lv2-intermediate/07-strings/trie/)만으로 풀 수 있는 경우와 없는 경우(패턴이 본문의 어디에서 시작하는지 모를 때)를 구분해 보세요.
