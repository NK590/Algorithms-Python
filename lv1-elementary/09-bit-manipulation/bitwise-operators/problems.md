# 연습문제 — 비트 연산자

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 191 Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | popcount | `x & (x−1)` 반복 (`popcount`) |
| 2 | [백준 1094 막대기](https://www.acmicpc.net/problem/1094) | popcount | 막대를 반으로 쪼개는 규칙은 결국 켜진 비트의 수 |
| 3 | [LeetCode 231 Power of Two](https://leetcode.com/problems/power-of-two/) | 판별 | `x > 0 and x & (x−1) == 0` (`is_power_of_two`) |
| 4 | [LeetCode 136 Single Number](https://leetcode.com/problems/single-number/) | XOR | 모두 XOR하면 한 번만 나온 수가 남는다 (`single_number`) |
| 5 | [LeetCode 338 Counting Bits](https://leetcode.com/problems/counting-bits/) | DP | `bits[i] = bits[i >> 1] + (i & 1)` (`count_bits_table`) |
| 6 | [LeetCode 461 Hamming Distance](https://leetcode.com/problems/hamming-distance/) | XOR + popcount | 다른 비트의 수 = `popcount(a ^ b)` |
| 7 | [LeetCode 268 Missing Number](https://leetcode.com/problems/missing-number/) | XOR | 0..n과 배열을 모두 XOR하면 빠진 수만 남는다 |
| 8 | [LeetCode 190 Reverse Bits](https://leetcode.com/problems/reverse-bits/) | 비트 뒤집기 | 폭을 고정해 한 비트씩 옮긴다 (`reverse_bits`) |
| 9 | [백준 13701 중복 제거](https://www.acmicpc.net/problem/13701) | 정수를 비트셋으로 | 값을 비트 위치로 쓰는 매우 큰 정수로 중복 판정. 메모리 제한이 작다 |
| 10 | [백준 11723 집합](https://www.acmicpc.net/problem/11723) | 집합 | 비트마스크로 집합 연산. [비트마스크](../bitmask/) 참고. 이 폴더의 `process_commands`와 같은 형태 |

## 풀이 메모

- 1~3번은 `x & (x−1)`을 손으로 써서 어느 비트가 꺼지는지 확인하세요. [README](README.md)의 표(`x = 12`)가 예입니다.
- 4번과 7번은 "같은 수를 두 번 XOR하면 사라진다"는 한 가지 성질만 쓰는 문제입니다. 해시 테이블 풀이(O(n) 공간)와 비교해 공간이 O(1)인 이유를 확인하세요.
- 6번은 1번과 합치면 한 줄입니다: `bin(a ^ b).count("1")`.
- 9번은 `set`을 쓰면 메모리가 부족한 환경을 가정합니다. 정수 하나의 `i`번째 비트를 "값 `i`를 이미 봤는가"로 사용합니다.
