"""solution.py 검증: 라벨 전파·단계별 확장 같은 전혀 다른 느린 방법과의 랜덤 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_grid(rng, max_side=6, open_prob=0.6):
    rows, cols = rng.randint(1, max_side), rng.randint(1, max_side)
    return [[1 if rng.random() < open_prob else 0 for _ in range(cols)] for _ in range(rows)]


def neighbors(r, c, rows, cols):
    return [(r + dr, c + dc) for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if 0 <= r + dr < rows and 0 <= c + dc < cols]


def region_sizes_by_label_propagation(grid):
    """칸마다 자기 번호를 라벨로 가진 뒤, 이웃 중 가장 작은 라벨로 바꾸는 일을 변화가 없을 때까지 반복한다."""
    rows, cols = len(grid), len(grid[0])
    label = {(r, c): r * cols + c for r in range(rows) for c in range(cols) if grid[r][c] == 1}
    changed = True
    while changed:
        changed = False
        for (r, c), value in list(label.items()):
            for n in neighbors(r, c, rows, cols):
                if n in label and label[n] < label[(r, c)]:
                    label[(r, c)] = label[n]
                    changed = True
    sizes = {}
    for value in label.values():
        sizes[value] = sizes.get(value, 0) + 1
    return sorted(sizes.values())


def distances_by_relaxation(grid, start):
    """"k 번 이동해서 갈 수 있는 칸" 집합을 k = 0, 1, 2 … 로 넓혀 가며 처음 닿는 k 를 거리로 한다."""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    if grid[start[0]][start[1]] != 1:
        return dist
    frontier = {start}
    dist[start[0]][start[1]] = 0
    k = 0
    while frontier:
        k += 1
        nxt = set()
        for r, c in frontier:
            for nr, nc in neighbors(r, c, rows, cols):
                if grid[nr][nc] == 1 and dist[nr][nc] == -1:
                    dist[nr][nc] = k
                    nxt.add((nr, nc))
        frontier = nxt
    return dist


def test_readme_example_regions():
    grid = [
        [1, 1, 0, 0, 1],
        [0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
    ]
    assert solution.region_sizes(grid) == [1, 3, 3, 3]
    assert solution.count_regions(grid) == 4


def test_regions_match_label_propagation():
    rng = random.Random(0)
    for _ in range(300):
        grid = random_grid(rng)
        before = [row[:] for row in grid]
        assert solution.region_sizes(grid) == region_sizes_by_label_propagation(grid), grid
        assert grid == before


def test_flood_fill():
    grid = [[1, 1, 0], [1, 0, 0], [0, 0, 1]]
    assert solution.flood_fill(grid, 0, 0, 7) == 3
    assert grid == [[7, 7, 0], [7, 0, 0], [0, 0, 1]]
    assert solution.flood_fill(grid, 0, 0, 7) == 0  # 이미 같은 값이면 아무것도 하지 않는다 (무한 반복 방지)
    assert solution.flood_fill(grid, 1, 1, 5) == 5  # 벽(0)으로 이어진 영역도 칠할 수 있다


def test_distances_match_relaxation():
    rng = random.Random(1)
    for _ in range(300):
        grid = random_grid(rng)
        start = (rng.randrange(len(grid)), rng.randrange(len(grid[0])))
        assert solution.distances_from(grid, start) == distances_by_relaxation(grid, start), (grid, start)


def test_shortest_path_length_examples():
    maze = [[1, 0, 1, 1], [1, 1, 1, 0], [0, 0, 1, 1]]
    assert solution.shortest_path_length(maze, (0, 0), (2, 3)) == 5
    assert solution.shortest_path_length([[1, 0], [0, 1]], (0, 0), (1, 1)) == -1
    assert solution.shortest_path_length([[1]], (0, 0), (0, 0)) == 0
    assert solution.shortest_path_length([[0, 1]], (0, 0), (0, 1)) == -1  # 시작이 벽


def test_large_open_grid():
    n = 300
    grid = [[1] * n for _ in range(n)]
    assert solution.shortest_path_length(grid, (0, 0), (n - 1, n - 1)) == 2 * (n - 1)
    assert solution.count_regions(grid) == 1
    assert solution.flood_fill(grid, 0, 0, 2) == n * n


def test_main_counts_cells_on_the_path(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 4\n1011\n1110\n0011\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "6"
    monkeypatch.setattr("sys.stdin", io.StringIO("2 2\n10\n01\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "-1"
