# Algorithms-Python

PS/CP 알고리즘을 **낮은 난이도부터 매우 높은 난이도까지** 개념 설명과 Python 예시 코드로 차근차근 배우는 학습 리포지토리입니다.

*A Korean-language, level-based study repository for competitive programming (PS/CP). Concepts are ordered from beginner (≈ solved.ac Bronze) to expert (≈ Ruby), each with an explanation and a Python implementation, with tests and practice problems added as the repository grows.*

## 특징

- **난이도 순 커리큘럼** — Lv0(입문)부터 Lv5(마스터)까지, 위에서 아래로 읽으면 선행 지식이 자연스럽게 쌓이도록 구성합니다.
- **개념 하나 = 폴더 하나** — 설명(`README.md`), 구현(`solution.py`), 테스트, 연습문제를 한곳에 둡니다.
- **"언제 쓰는가"를 함께 설명** — 구현법뿐 아니라 문제의 어떤 신호에서 이 알고리즘을 떠올려야 하는지를 다룹니다.
- **코드 검증** — 완성된 개념은 브루트 포스와 비교하는 랜덤 테스트를 갖추고, CI가 자동으로 실행합니다.
- **연습문제는 링크로** — 백준·Codeforces 등의 문제는 지문을 옮기지 않고 링크와 배울 점만 정리합니다.

## 레벨

난이도는 [solved.ac](https://solved.ac) 티어를 대략적인 기준으로 합니다. 표의 숫자는 지금까지 추가된 개념 수입니다.

<!-- INDEX:START -->
| 레벨 | 이름 | solved.ac | 개념 | `stub` | `migrated` | `draft` | `done` | 목표 |
|---|---|---|---:|---:|---:|---:|---:|---|
| [Lv0](lv0-basics/) | 입문 | Bronze | 14 | 0 | 0 | 0 | 14 | 입출력과 구현, 완전 탐색으로 쉬운 문제를 푼다 |
| [Lv1](lv1-elementary/) | 기초 | Silver | 39 | 0 | 0 | 0 | 39 | 기본 자료구조와 정렬·탐색, DFS/BFS, DP·그리디 입문을 익힌다 |
| [Lv2](lv2-intermediate/) | 중급 | Gold | 31 | 0 | 0 | 0 | 31 | 최단 경로·위상 정렬 같은 그래프 알고리즘과 DP 심화를 익힌다 |
| [Lv3](lv3-advanced/) | 고급 | Platinum | 27 | 0 | 0 | 0 | 27 | 구간 질의 자료구조, 고급 그래프(SCC·플로우), 문자열·기하 도구를 익힌다 |
| [Lv4](lv4-expert/) | 최상급 | Diamond | 6 | 0 | 0 | 0 | 6 | 트리 분해, 영속·고급 자료구조, FFT, 정수론 심화 등 대회 상위권 도구를 다룬다 |
| [Lv5](lv5-master/) | 마스터 | Ruby | 0 | 0 | 0 | 0 | 0 | Link-Cut Tree, Blossom 등 소수만 쓰는 최상위 알고리즘을 다룬다 |
<!-- INDEX:END -->

각 레벨을 눌러 개념 목록을 볼 수 있고, 앞으로 추가할 주제는 [ROADMAP](ROADMAP.md)에 정리되어 있습니다.

### 상태 표기

| 상태 | 의미 |
|---|---|
| `stub` | 개념 설명만 있고 구현 코드는 없음 |
| `migrated` | 기존 코드·설명을 새 구조로 옮겨 둔 상태 (문서 템플릿 미적용) |
| `draft` | 문서 템플릿에 맞춰 작성 중 |
| `done` | 설명 · 구현 · 테스트 · 연습문제를 모두 갖춤 |

> **현재 진행 상황**: Lv0~Lv3의 모든 개념이 `done`입니다(설명 · 구현 · 브루트 포스와 비교하는 테스트 · 연습문제). Lv4~Lv5를 작성하는 중이고, 아직 `stub`·`migrated`인 개념은 코드 주석을 옮긴 초안입니다. 기존 코드에서 발견했던 문제는 모두 고쳤습니다([알려진 이슈](ROADMAP.md#알려진-이슈-기존-코드)).

## 저장소 구조

```
.
├── lv0-basics/ … lv5-master/       # 레벨별 폴더
│   └── NN-<그룹>/                   # 토픽 그룹 (정렬, 최단 경로 …) + 알고리즘 비교표
│       └── <개념>/                  # README.md · solution.py · test_solution.py · problems.md
├── docs/
│   ├── python-for-ps.md             # 파이썬으로 PS 하기 (입출력, 재귀, PyPy, 함정)
│   ├── complexity-cheatsheet.md     # 입력 크기 → 허용 복잡도, 내장 연산 시간 복잡도
│   ├── problem-to-algorithm.md      # 문제 신호 → 알고리즘 가이드
│   └── TEMPLATE/                    # 새 개념 문서 템플릿
├── tools/                           # 구조 검증·목차 생성 (gen_index.py), 테스트 로더
├── ROADMAP.md                       # 전체 커리큘럼과 개념 선행 관계
└── CONTRIBUTING.md                  # 새 개념 추가 방법
```

## 학습하는 법

1. 처음이라면 [파이썬으로 PS 하기](docs/python-for-ps.md)와 [복잡도 치트시트](docs/complexity-cheatsheet.md)를 먼저 읽어 보세요.
2. 자신의 레벨에서 시작해 그룹 단위로 읽습니다. 각 개념 문서의 `prerequisites`가 먼저 알아야 할 개념입니다.
3. 개념을 읽은 뒤 `problems.md`의 문제를 쉬운 것부터 풀어 보세요.
4. 문제를 풀다 막히면 [문제 신호 → 알고리즘 가이드](docs/problem-to-algorithm.md)로 후보를 좁혀 보세요.

## 직접 실행하기

```bash
python lv2-intermediate/01-shortest-path/dijkstra/solution.py   # 개념별 예제 실행
python tools/gen_index.py --check                                # 구조·링크·목차 검증
python -m pip install pytest && python -m pytest                 # 테스트
```

새 개념을 추가하려면 [CONTRIBUTING](CONTRIBUTING.md)을 참고하세요.
