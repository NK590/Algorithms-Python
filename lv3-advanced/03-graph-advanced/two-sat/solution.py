"""2-SAT — 각 절이 변수 두 개의 OR 인 논리식 (a ∨ b) ∧ (c ∨ d) ∧ … 이 참이 되게 하는 값 배정을 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 절 (A ∨ B) 는 두 개의 함의 ¬A → B 와 ¬B → A 와 같습니다. 변수마다 정점 두 개(참, 거짓)를 둔 함의 그래프를 만들면
  식이 만족 가능 ⟺ 어떤 변수 x 도 x 와 ¬x 가 같은 SCC 에 있지 않다.
- 배정: SCC 를 위상 정렬 순서로 보아 x 가 ¬x 보다 뒤에 있으면 x = 참 (Tarjan 번호는 위상 정렬의 역순이므로 comp[x] < comp[¬x] 이면 참).
- 정점 번호: 변수 i 의 "참" 은 2i, "거짓" 은 2i + 1. 변수는 0 부터 n-1.
- 이 파일은 단독으로 실행되도록 반복문 Tarjan SCC 를 포함합니다.
- 직접 실행하면 `N M` 과 M 개의 절 `a b` (a ∨ b, 음수는 부정, 변수는 1 부터)를 받아 만족 가능하면 `1` 과 각 변수의 값(0/1)을, 아니면 `0` 을 출력합니다.
"""
import sys


def _scc_ids(node_count: int, adjacency: list[list[int]]) -> list[int]:
    """반복문 Tarjan. 정점별 SCC 번호(완성되는 순서, 즉 위상 정렬의 역순)."""
    order = [-1] * node_count
    low = [0] * node_count
    on_stack = [False] * node_count
    ids = [-1] * node_count
    stack: list[int] = []
    counter = 0
    component_count = 0
    for start in range(node_count):
        if order[start] != -1:
            continue
        order[start] = low[start] = counter
        counter += 1
        stack.append(start)
        on_stack[start] = True
        call_stack = [(start, 0)]
        while call_stack:
            v, i = call_stack.pop()
            if i < len(adjacency[v]):
                call_stack.append((v, i + 1))
                w = adjacency[v][i]
                if order[w] == -1:
                    order[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack[w] = True
                    call_stack.append((w, 0))
                elif on_stack[w]:
                    low[v] = min(low[v], order[w])
            else:
                if low[v] == order[v]:
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        ids[w] = component_count
                        if w == v:
                            break
                    component_count += 1
                if call_stack:
                    parent = call_stack[-1][0]
                    low[parent] = min(low[parent], low[v])
    return ids


class TwoSat:
    def __init__(self, n: int):
        self.n = n
        self.adjacency: list[list[int]] = [[] for _ in range(2 * n)]

    @staticmethod
    def _node(variable: int, value: bool) -> int:
        """리터럴 "variable == value" 의 정점 번호."""
        return 2 * variable + (0 if value else 1)

    def add_clause(self, i: int, a: bool, j: int, b: bool) -> None:
        """(x_i == a) ∨ (x_j == b). 예: add_clause(0, True, 1, False) 는 (x0 ∨ ¬x1)."""
        self.adjacency[self._node(i, not a)].append(self._node(j, b))  # ¬A → B
        self.adjacency[self._node(j, not b)].append(self._node(i, a))  # ¬B → A

    def force(self, i: int, value: bool) -> None:
        """x_i == value 로 고정한다. (x_i == value) ∨ (x_i == value)."""
        self.add_clause(i, value, i, value)

    def add_implication(self, i: int, a: bool, j: int, b: bool) -> None:
        """(x_i == a) → (x_j == b)."""
        self.add_clause(i, not a, j, b)

    def add_equal(self, i: int, j: int) -> None:
        """x_i == x_j. (x_i → x_j) 와 (x_j → x_i) 두 절이면 충분하다 (각 절이 대우 간선까지 함께 넣는다)."""
        self.add_implication(i, True, j, True)
        self.add_implication(j, True, i, True)

    def add_not_equal(self, i: int, j: int) -> None:
        """x_i != x_j."""
        self.add_clause(i, True, j, True)
        self.add_clause(i, False, j, False)

    def solve(self):
        """만족하는 배정(길이 n 의 bool 리스트) 하나, 불가능하면 None."""
        ids = _scc_ids(2 * self.n, self.adjacency)
        assignment = []
        for i in range(self.n):
            true_id, false_id = ids[2 * i], ids[2 * i + 1]
            if true_id == false_id:
                return None
            assignment.append(true_id < false_id)
        return assignment


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    sat = TwoSat(n)
    for k in range(m):
        a, b = int(data[2 + 2 * k]), int(data[3 + 2 * k])
        sat.add_clause(abs(a) - 1, a > 0, abs(b) - 1, b > 0)
    assignment = sat.solve()
    if assignment is None:
        print(0)
    else:
        print(1)
        print(" ".join("1" if value else "0" for value in assignment))


if __name__ == "__main__":
    main()
