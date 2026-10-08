"""크루스칼 알고리즘 — 가중치가 작은 간선부터 사이클을 만들지 않는 것만 골라 최소 신장 트리(MST)를 만들기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 무방향 그래프를 간선 목록 `edges = [(u, v, w), ...]` 와 정점 수 `n` 으로 받고, 정점 번호는 0 ~ n-1 입니다.
- 간선을 가중치순으로 정렬한 뒤, 두 끝점이 아직 다른 집합이면 채택하고 합칩니다. (같은 집합이면 사이클이 되므로 버립니다)
  "같은 집합인가" 판정에 유니온 파인드를 씁니다. 이 파일에는 필요한 만큼만 들어 있습니다.
- 그래프가 연결되어 있지 않으면 연결 요소마다 하나씩의 최소 신장 트리(최소 신장 숲)를 만듭니다.
- 직접 실행하면 아래 형식의 입력(최소 스패닝 트리)을 받아 MST 의 가중치 합을 출력합니다. (정점은 1부터)

      V E          정점 수, 간선 수
      A B C        (E 줄) A 와 B 를 잇는 가중치 C 의 간선
"""
import sys

Edge = tuple[int, int, int]


def _find(parent: list[int], x: int) -> int:
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:  # 경로 압축
        parent[x], x = root, parent[x]
    return root


def kruskal(n: int, edges: list[Edge], maximize: bool = False) -> tuple[int, list[Edge]]:
    """(가중치 합, 채택한 간선들) 을 반환한다. maximize=True 면 최대 신장 트리.

    정점 n 개가 연결되어 있으면 채택한 간선은 n-1 개다. 연결되어 있지 않으면 n - (연결 요소 수) 개(최소 신장 숲)."""
    parent = list(range(n))
    size = [1] * n
    total = 0
    chosen = []
    for u, v, w in sorted(edges, key=lambda e: e[2], reverse=maximize):
        ru, rv = _find(parent, u), _find(parent, v)
        if ru == rv:
            continue  # 이미 연결된 두 정점: 이 간선을 넣으면 사이클
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        total += w
        chosen.append((u, v, w))
        if len(chosen) == n - 1:  # 더 채택할 수 없다 (연결된 그래프에서의 조기 종료)
            break
    return total, chosen


def kruskal_until_components(n: int, edges: list[Edge], k: int) -> int | None:
    """연결 요소가 k 개가 될 때까지만 크루스칼을 돌려 얻은 간선의 가중치 합. 그래프를 k 개의 마을로 나누는 최소 비용.

    MST 에서 가장 비싼 k-1 개의 간선을 빼는 것과 같다. 처음부터 k 개보다 연결 요소가 많으면 None."""
    parent = list(range(n))
    components = n
    total = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if components <= k:
            break
        ru, rv = _find(parent, u), _find(parent, v)
        if ru != rv:
            parent[rv] = ru
            total += w
            components -= 1
    return total if components <= k else None


def main() -> None:
    input = sys.stdin.readline
    v, e = map(int, input().split())
    edges = []
    for _ in range(e):
        a, b, c = map(int, input().split())
        edges.append((a - 1, b - 1, c))
    print(kruskal(v, edges)[0])


if __name__ == "__main__":
    main()
