# 문자열 심화 (Advanced Strings)

Lv2~Lv3에서 [KMP](../../lv2-intermediate/07-strings/kmp/), [Z 알고리즘](../../lv3-advanced/05-strings-advanced/z-algorithm/), [매내처](../../lv3-advanced/05-strings-advanced/manacher/), [아호-코라식](../../lv3-advanced/05-strings-advanced/aho-corasick/), [접미사 배열](../../lv3-advanced/05-strings-advanced/suffix-array-lcp/)을 배웠습니다. 이 단원의 [접미사 자동자](suffix-automaton/)는 그 도구들이 각각 푸는 문제 대부분을 **하나의 구조** — 문자열의 모든 부분 문자열을 받아들이는 최소 DFA — 로 묶어서 온라인으로 `O(n)`에 만듭니다.

## 한눈에 비교

| 도구 | 만드는 대상 | 만드는 시간 | 잘하는 문제 |
|---|---|---|---|
| [KMP](../../lv2-intermediate/07-strings/kmp/) / [Z](../../lv3-advanced/05-strings-advanced/z-algorithm/) | 패턴(또는 문자열)의 실패/Z 함수 | O(n) | 패턴 하나를 본문에서 찾기, 주기 |
| [접미사 배열 + LCP](../../lv3-advanced/05-strings-advanced/suffix-array-lcp/) | 접미사의 사전순 정렬 | O(n log n) | 서로 다른 부분 문자열 수, 사전순 `k`번째 접미사, 최장 반복·공통 부분 문자열 |
| [아호-코라식](../../lv3-advanced/05-strings-advanced/aho-corasick/) | 패턴 **여러 개**의 트라이 + 실패 링크 | O(패턴 합) | 본문에서 패턴 여러 개를 한꺼번에 |
| [접미사 자동자](suffix-automaton/) | 본문의 모든 부분 문자열 | O(n), 온라인 | 부분 문자열 포함·출현 횟수·위치, 서로 다른 부분 문자열의 사전순 `k`번째, 여러 문자열의 공통 부분 문자열 |

## 문제 신호로 고르기

| 문제의 신호 | 선택 |
|---|---|
| 본문 하나에 **패턴이 많고** 각각 출현 횟수/위치 | [접미사 자동자](suffix-automaton/) (또는 접미사 배열 + 이진 탐색) |
| **패턴이 많고** 본문이 여러 개 | [아호-코라식](../../lv3-advanced/05-strings-advanced/aho-corasick/) |
| 글자를 붙이는 **중간마다** 답이 필요하다 (접두사별 답) | [접미사 자동자](suffix-automaton/) (온라인) |
| 접미사의 **사전순** 관련 (`k`번째 접미사, LCP 질의) | [접미사 배열](../../lv3-advanced/05-strings-advanced/suffix-array-lcp/) |
| 두 개 이상의 문자열의 최장 공통 부분 문자열 | [접미사 자동자](suffix-automaton/) (또는 접미사 배열 + 구분자) |
| 패턴 하나, 본문 하나 | [KMP](../../lv2-intermediate/07-strings/kmp/) / [Z](../../lv3-advanced/05-strings-advanced/z-algorithm/) |
| 회문 부분 문자열 | [매내처](../../lv3-advanced/05-strings-advanced/manacher/) |

## 개념 사이의 관계

- 접미사 자동자의 **접미사 링크 트리**는 뒤집은 문자열의 접미사 트리와 같습니다. 접미사 배열과 같은 정보(서로 다른 부분 문자열의 수, 공통 접두사의 길이)를 트리 모양으로 다룬다고 볼 수 있습니다.
- [아호-코라식](../../lv3-advanced/05-strings-advanced/aho-corasick/)의 실패 링크는 접미사 자동자의 접미사 링크와 같은 발상입니다: "이 상태의 문자열에서 한 글자를 줄여 가며 트라이에 남아 있는 가장 긴 접미사". 아호-코라식은 *패턴 집합* 의 트라이 위에서, 접미사 자동자는 *본문의 모든 부분 문자열* 위에서 같은 일을 합니다.
- [KMP](../../lv2-intermediate/07-strings/kmp/)의 실패 함수는 이 자동자의 링크를 한 문자열의 접두사에 대해서만 가진 특수한 경우입니다.

## 공통 원칙

- **작은 알파벳의 모든 문자열로 검증**: 모든 부분 문자열을 직접 나열·세는 순진한 방법과 무작위 비교.
- **구조적 불변식 확인**: 상태 수 `≤ 2n − 1`, 한 상태의 문자열들이 같은 끝 위치 집합을 가지는지, 길이가 `len[link] + 1 .. len`을 채우는지.
- **빈 문자열과 경계**: 빈 패턴, 길이 1 문자열, 모두 같은 글자(`aaaa`), 주기 문자열(`abab…`)을 꼭 시험.
- **파이썬의 큰 정수**: 서로 다른 부분 문자열의 수가 `n = 2·10⁵`에서 `2·10¹⁰`이어도 오버플로가 없다.

## 읽는 순서

1. [접미사 자동자](suffix-automaton/)

선행: [트라이](../../lv2-intermediate/07-strings/trie/), [KMP](../../lv2-intermediate/07-strings/kmp/), [접미사 배열과 LCP](../../lv3-advanced/05-strings-advanced/suffix-array-lcp/), [아호-코라식](../../lv3-advanced/05-strings-advanced/aho-corasick/). 이후: 회문 트리, 접미사 트리 (이 저장소에는 다루지 않습니다).
