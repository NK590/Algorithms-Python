# Algorithms-Python

PS/CP 알고리즘을 **낮은 난이도부터 매우 높은 난이도까지** 개념 설명과 Python 예시 코드로 차근차근 배우는 학습 리포지토리입니다.

*A Korean-language, level-based study repository for competitive programming (PS/CP), with explanations, Python implementations, tests, and practice references from several judges.*

## 특징

- **난이도 순 커리큘럼** — Lv0(입문)부터 Lv5(마스터)까지, 위에서 아래로 읽으면 선행 지식이 자연스럽게 쌓이도록 구성합니다.
- **개념 하나 = 폴더 하나** — 설명(`README.md`), 구현(`solution.py`), 테스트, 연습문제를 한곳에 둡니다.
- **"언제 쓰는가"를 함께 설명** — 구현법뿐 아니라 문제의 어떤 신호에서 이 알고리즘을 떠올려야 하는지를 다룹니다.
- **코드 검증** — 완성된 개념은 브루트 포스와 비교하는 랜덤 테스트를 갖추고, CI가 자동으로 실행합니다.
- **연습문제는 링크로** — CSES·AtCoder·AOJ·LeetCode·Library Checker 등에서 개념에 맞는 문제를 선정하고, 링크와 배울 점을 정리합니다.

## 레벨

레벨은 선수 지식과 구현 복잡도를 기준으로 한 학습 순서입니다. Bronze부터 Ruby까지의 이름은 단계 구분용 표기이며, 외부 사이트의 문제 등급과 일대일로 대응하지 않습니다. 표의 숫자는 지금까지 추가된 개념 수입니다.

<!-- INDEX:START -->
| 레벨 | 이름 | 난이도 표기 | 개념 | `stub` | `migrated` | `draft` | `done` | 목표 |
|---|---|---|---:|---:|---:|---:|---:|---|
| [Lv0](lv0-basics/) | 입문 | Bronze | 14 | 0 | 0 | 0 | 14 | 입출력과 구현, 완전 탐색으로 쉬운 문제를 푼다 |
| [Lv1](lv1-elementary/) | 기초 | Silver | 39 | 0 | 0 | 0 | 39 | 기본 자료구조와 정렬·탐색, DFS/BFS, DP·그리디 입문을 익힌다 |
| [Lv2](lv2-intermediate/) | 중급 | Gold | 31 | 0 | 0 | 0 | 31 | 최단 경로·위상 정렬 같은 그래프 알고리즘과 DP 심화를 익힌다 |
| [Lv3](lv3-advanced/) | 고급 | Platinum | 27 | 0 | 0 | 0 | 27 | 구간 질의 자료구조, 고급 그래프(SCC·플로우), 문자열·기하 도구를 익힌다 |
| [Lv4](lv4-expert/) | 최상급 | Diamond | 21 | 0 | 0 | 0 | 21 | 트리 분해, 영속·고급 자료구조, FFT, 정수론 심화 등 대회 상위권 도구를 다룬다 |
| [Lv5](lv5-master/) | 마스터 | Ruby | 9 | 0 | 0 | 0 | 9 | 링크-컷 트리, 블로섬, 다항식 연산 등 논문·대회 해설 수준의 최상위 알고리즘을 다룬다 |
<!-- INDEX:END -->

각 레벨을 눌러 개념 목록을 볼 수 있고, 앞으로 추가할 주제는 [ROADMAP](ROADMAP.md)에 정리되어 있습니다.

### 상태 표기

| 상태 | 의미 |
|---|---|
| `stub` | 개념 설명만 있고 구현 코드는 없음 |
| `migrated` | 기존 코드·설명을 새 구조로 옮겨 둔 상태 (문서 템플릿 미적용) |
| `draft` | 문서 템플릿에 맞춰 작성 중 |
| `done` | 상태·정당성·검산 설명, 구현, 실행되는 테스트, 학습 포인트가 있는 문제 목록을 갖춤 |

> **현재 진행 상황**: Lv0~Lv5의 141개 개념에 설명·구현·테스트·연습문제가 있습니다. `done`은 필수 자료와 검증을 갖췄다는 상태이며 모든 입력의 정확성이나 모든 채점기의 통과를 보장하는 표시가 아닙니다. 수정한 오류는 [검증 이력](ROADMAP.md#검증과-보강-이력)에 정리합니다.

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
│   ├── algorithm-reading-guide.md  # 상태·전이·정당성·복잡도를 읽는 법
│   ├── reference-guide.md          # 문제 사이트와 제출 형식 안내
│   └── TEMPLATE/                    # 새 개념 문서 템플릿
├── tools/                           # 구조 검증·목차 생성 (gen_index.py), 테스트 로더
├── ROADMAP.md                       # 전체 커리큘럼과 개념 선행 관계
└── CONTRIBUTING.md                  # 새 개념 추가 방법
```

## 학습하는 법

1. 처음이라면 [알고리즘 설명을 읽는 법](docs/algorithm-reading-guide.md), [파이썬으로 PS 하기](docs/python-for-ps.md), [복잡도 치트시트](docs/complexity-cheatsheet.md)를 먼저 읽어 보세요.
2. 자신의 레벨에서 시작해 그룹 단위로 읽습니다. 각 개념 문서의 `prerequisites`가 먼저 알아야 할 개념입니다.
3. 개념을 읽은 뒤 `problems.md`의 추천 순서를 따라 연습합니다. [사이트 이용 안내](docs/reference-guide.md)에서 원문과 참고 구현의 입력·출력 차이를 확인하세요.
4. 문제를 풀다 막히면 [문제 신호 → 알고리즘 가이드](docs/problem-to-algorithm.md)로 후보를 좁혀 보세요.

## 직접 실행하기

개발과 CI의 기준은 **Python 3.12**입니다. 테스트 의존성은 `requirements-dev.txt`에 고정합니다. 알고리즘 구현은 표준 라이브러리만 사용합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python tools/gen_index.py --check           # 구성·설명·링크·앵커·목차 검증
python -m compileall -q tools lv*/          # 구문 검사
python -m pytest -q                        # 구현·도구·실행 가능한 문서 예제
```

Windows에서는 `source` 대신 `.venv\Scripts\activate`를 사용합니다. 개념별 `solution.py`의 직접 실행 형식은 해당 문서의 4절에 설명돼 있습니다. 입력을 읽는 예제는 표준 입력도 함께 제공해야 합니다.

외부 페이지의 응답 확인은 `python tools/check_external_links.py`로 별도 실행합니다. 로그인·요청 제한·네트워크 차단을 삭제된 링크와 구분합니다.

새 개념을 추가하려면 [CONTRIBUTING](CONTRIBUTING.md)을 참고하세요.
