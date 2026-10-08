"""아호-코라식(Aho-Corasick) — 여러 패턴을 본문에서 한꺼번에 O(본문 + 패턴 합 + 찾은 개수) 에 찾기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 모든 패턴을 트라이에 넣고, 노드마다 "실패 링크" fail[v] 를 둡니다: v 가 나타내는 문자열의 가장 긴 진 접미사 중 트라이에 있는 것(KMP 의 실패 함수를 트라이로 일반화).
- 본문을 한 글자씩 읽으며 현재 노드에서 그 글자로 갈 수 없으면 실패 링크를 따라 올라갑니다. 포인터가 늘어난 만큼만 내려가므로 전체 O(본문).
- 어떤 노드에 도착하면 그 노드가 끝인 패턴뿐 아니라 실패 링크로 이어진 접미사 노드들이 끝인 패턴도 함께 나온 것입니다.
  output_link[v] = 실패 링크를 따라가며 처음 만나는 "끝나는 패턴이 있는 노드" 로 건너뛰어, 나온 패턴만 순서대로 방문합니다.
- 같은 패턴이 여러 번 주어져도 되고(모두 따로 보고), 다른 패턴의 부분 문자열인 패턴도 됩니다. 빈 패턴은 허용하지 않습니다.
- 직접 실행하면 `N`, N 개의 패턴, `Q`, Q 개의 질의 문자열을 받아 각 질의가 어떤 패턴이라도 부분 문자열로 포함하면 YES, 아니면 NO 를 출력합니다.
"""
import sys
from collections import deque


class AhoCorasick:
    def __init__(self, patterns: list[str]):
        self.patterns = list(patterns)
        self.children: list[dict[str, int]] = [{}]
        self.ends: list[list[int]] = [[]]  # 노드에서 정확히 끝나는 패턴 번호들
        self.pattern_node: list[int] = []  # 패턴 번호 -> 끝나는 노드
        for index, pattern in enumerate(self.patterns):
            if not pattern:
                raise ValueError("빈 패턴은 허용하지 않습니다")
            node = 0
            for ch in pattern:
                nxt = self.children[node].get(ch)
                if nxt is None:
                    nxt = len(self.children)
                    self.children.append({})
                    self.ends.append([])
                    self.children[node][ch] = nxt
                node = nxt
            self.ends[node].append(index)
            self.pattern_node.append(node)
        size = len(self.children)
        self.fail = [0] * size
        self.output_link = [0] * size  # 실패 링크를 따라 처음 만나는, 끝나는 패턴이 있는 노드 (없으면 0)
        self.has_output = [False] * size  # 이 노드에 도착했을 때 어떤 패턴이든 끝났는가 (자기 자신 또는 접미사)
        self.bfs_order: list[int] = []
        queue = deque(self.children[0].values())  # 깊이 1 의 노드는 실패 링크가 루트
        self.bfs_order.extend(queue)
        for v in queue:
            self.has_output[v] = bool(self.ends[v])
        while queue:
            u = queue.popleft()
            for ch, v in self.children[u].items():
                f = self.fail[u]
                while f and ch not in self.children[f]:
                    f = self.fail[f]
                self.fail[v] = self.children[f].get(ch, 0)
                link = self.fail[v]
                self.output_link[v] = link if self.ends[link] else self.output_link[link]
                self.has_output[v] = bool(self.ends[v]) or self.has_output[link]
                queue.append(v)
                self.bfs_order.append(v)

    def _next(self, node: int, ch: str) -> int:
        while node and ch not in self.children[node]:
            node = self.fail[node]
        return self.children[node].get(ch, 0)

    def find_all(self, text: str) -> list[tuple[int, int]]:
        """(시작 위치, 패턴 번호) 목록. 끝 위치 순으로, 같은 끝에서는 긴 패턴이 먼저(가장 깊은 노드부터 실패 링크를 따라) 나온다."""
        result = []
        node = 0
        for i, ch in enumerate(text):
            node = self._next(node, ch)
            v = node  # 끝나는 패턴이 없는 노드는 ends 가 비어 있어 건너뛰고, output_link 로 곧장 다음 후보에 간다
            while v:
                for index in self.ends[v]:
                    result.append((i - len(self.patterns[index]) + 1, index))
                v = self.output_link[v]
        return result

    def count_occurrences(self, text: str) -> list[int]:
        """패턴 번호별로 본문에 (겹쳐도) 나오는 횟수. 노드 방문 횟수를 센 뒤 BFS 의 역순으로 실패 링크를 따라 전파해 O(본문 + 노드 수)."""
        visits = [0] * len(self.children)
        node = 0
        for ch in text:
            node = self._next(node, ch)
            visits[node] += 1
        for v in reversed(self.bfs_order):
            visits[self.fail[v]] += visits[v]
        return [visits[self.pattern_node[index]] for index in range(len(self.patterns))]

    def contains_any(self, text: str) -> bool:
        """어떤 패턴이라도 본문의 부분 문자열인가. 처음 발견하면 바로 끝낸다."""
        node = 0
        for ch in text:
            node = self._next(node, ch)
            if self.has_output[node]:
                return True
        return False


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    automaton = AhoCorasick(data[1 : 1 + n])
    q = int(data[1 + n])
    print("\n".join("YES" if automaton.contains_any(data[2 + n + i]) else "NO" for i in range(q)))


if __name__ == "__main__":
    main()
