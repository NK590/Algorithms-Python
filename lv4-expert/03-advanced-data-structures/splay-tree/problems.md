# 연습문제 — 스플레이 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [SPOJ ORDERSET - Order statistic set](https://www.spoj.com/problems/ORDERSET/) | 삽입·삭제·`k`번째·순위 | `SplaySet`의 기본 연산. [트립](../treap/)의 `OrderedMultiset`과 같은 문제를 두 구조로 풀어 비교 |
| 2 | [Luogu P3369 【模板】普通平衡树](https://www.luogu.com.cn/problem/P3369) | 삽입·삭제(중복 허용)·순위·`k`번째·이전·다음 | 정렬된 **다중**집합. `SplaySet`은 중복을 허용하지 않으므로 키 옆에 개수를 두거나 `(값, 번호)` 쌍으로 만들어야 한다 |
| 3 | [Luogu P3391 【模板】文艺平衡树](https://www.luogu.com.cn/problem/P3391) | 구간 뒤집기 후 최종 배열 | [solution.py](solution.py)의 `main()`이 같은 형태. 보초 노드와 지연 뒤집기의 기본 |
| 4 | [Library Checker - Range Reverse Range Sum](https://judge.yosupo.jp/problem/range_reverse_range_sum) | 구간 뒤집기 + 구간 합 | `reverse`와 `range_sum`을 번갈아. 트립과 속도 비교 |
| 5 | [HDU 3487 Play with Chain](https://acm.hdu.edu.cn/showproblem.php?pid=3487) | 구간을 잘라 다른 곳에 붙이기 + 구간 뒤집기 | `SplaySequence`에 잘라 붙이기(`move`)를 직접 추가해 보는 연습: 구간 서브트리를 떼어 다른 자리의 빈 서브트리에 단다 |
| 6 | [POJ 3580 SuperMemo](http://poj.org/problem?id=3580) | 구간 더하기·뒤집기·순환 이동·삽입·삭제·최솟값 | 스플레이 시퀀스의 종합 문제. 구간 더하기 태그와 최솟값 요약을 추가 |

## 풀이 메모

- 1번과 2번의 차이는 *중복 허용* 입니다. 이 구현의 `SplaySet`은 서로 다른 키만 받습니다. 다중집합이 필요하면 노드에 개수 필드를 추가하거나 `(값, 삽입 번호)`를 키로 쓰세요.
- 3번과 4번은 구조는 같고 질의만 다릅니다. 둘 다 `n`이 `10⁵`이면 파이썬에서 몇 초 안에 들어옵니다 ([README](README.md)의 측정표).
- 5번과 6번은 `SplaySequence`에 기능을 더하는 문제입니다. 구간 서브트리를 `O(1)`에 떼어 내고 붙일 수 있다는 것(스플레이 두 번)이 이 구조의 장점입니다. 6번은 구간 더하기 태그(`lazy_add`)와 `low`(최솟값) 요약을 [트립](../treap/)에서 가져오면 됩니다.
- 모든 문제에서 구현 후 순진한 리스트 연산과 무작위로 비교하는 테스트를 만드세요. 스플레이는 모양이 계속 바뀌어 눈으로 디버깅하기 어렵습니다 ([test_solution.py](test_solution.py)가 부모 포인터·크기·합의 불변식도 확인합니다).
