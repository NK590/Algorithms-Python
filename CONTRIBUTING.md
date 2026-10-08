# 새 개념 추가하기

이 문서는 개념(알고리즘·자료구조) 하나를 추가하거나 기존 문서를 템플릿에 맞춰 다시 쓰는 방법을 설명합니다.

## 1. 폴더 만들기

```
lvN-<레벨 이름>/NN-<그룹>/<개념>/
├── README.md          # 설명 (front matter 포함)
├── solution.py        # 참고 구현
├── test_solution.py   # 테스트 (status 가 done 이면 필수)
└── problems.md        # 연습문제 (status 가 done 이면 필수)
```

- 어느 레벨인지는 [로드맵](ROADMAP.md)과 각 레벨 README의 기준을 따릅니다. 같은 알고리즘도 쓰임새에 따라 난이도가 달라지므로, 처음 배우는 사람이 막히는 지점을 기준으로 정합니다.
- 그룹 안에서 읽는 순서는 개념 `README.md` front matter의 `order`(1부터)로 정합니다. 쉬운 것에서 어려운 것 순서로 매기세요.
- 폴더 이름은 `kebab-case` 영문입니다. 개념 폴더 이름(slug)은 저장소 전체에서 유일해야 하며, `prerequisites`에서 이 이름으로 참조합니다.
- 그룹 폴더에 알고리즘이 둘 이상이면 `README.md`에 **한눈에 비교**와 **고르는 기준**을 넣습니다. ([그룹 템플릿](docs/TEMPLATE/GROUP_README.md), 예: [최단 경로](lv2-intermediate/01-shortest-path/README.md))

## 2. 템플릿 복사

[`docs/TEMPLATE/`](docs/TEMPLATE/)의 파일을 새 폴더로 복사해 채웁니다.

| 파일 | 내용 |
|---|---|
| `README.md` | front matter + 설명 구조 (언제 쓰나 → 핵심 아이디어 → 손으로 따라가기 → 구현 → 복잡도 → 실수 → 변형 → 연습문제) |
| `solution.py` | 함수로 작성하고, 입력과 예제 실행은 `if __name__ == "__main__":` 아래에 둡니다 |
| `test_solution.py` | 손으로 확인한 예제 + **브루트 포스와의 랜덤 비교** |
| `problems.md` | 쉬운 것부터 어려운 순서로. 지문은 옮기지 말고 링크와 "배울 점"만 |

## 3. 상태(status) 올리기

| status | 조건 |
|---|---|
| `stub` | 설명만 있고 구현이 없음 |
| `migrated` | 기존 코드·설명을 옮겨 둔 상태 |
| `draft` | 템플릿에 맞춰 작성 중 |
| `done` | 설명 · 구현 · `test_solution.py` · `problems.md`를 모두 갖춤 |

## 4. 확인하기

```bash
python tools/gen_index.py    # 목차(README, ROADMAP 그래프) 갱신
python tools/gen_index.py --check
python -m pytest
```

- `gen_index.py`는 front matter 형식, 선행 개념(`prerequisites`) 존재 여부와 사이클, 파일 구성, 문서 안의 상대 경로 링크를 검사합니다. 같은 검사를 CI에서도 실행합니다.
- 테스트는 같은 폴더의 `solution.py`를 `tools.loader.load_solution(__file__)`로 불러옵니다. (개념 폴더마다 같은 파일 이름을 쓰기 때문에 `import solution`을 쓰면 충돌합니다)

## 5. 문서 쓰기 원칙

- **"언제 쓰나"를 반드시 씁니다.** 구현법보다 문제에서 알고리즘을 알아보는 것이 더 어렵습니다.
- 손으로 따라갈 수 있는 **작은 예제**를 하나 이상 넣습니다.
- 복잡도는 결과만이 아니라 이유를 한 줄 적습니다.
- 다른 사이트의 문제 지문은 옮기지 않습니다. 링크와 풀이 아이디어만 적습니다.
- 파이썬 특유의 함정(재귀 한도, 느린 연산 등)은 [파이썬으로 PS 하기](docs/python-for-ps.md)를 참고해서 반영합니다.
