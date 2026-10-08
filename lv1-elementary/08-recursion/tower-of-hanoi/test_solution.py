"""solution.py 검증: 규칙을 직접 시뮬레이션하고, 최소임을 BFS 로 확인하고, 세 가지 구현이 일치하는지 본다"""
import io
from collections import deque

from tools.loader import load_solution

solution = load_solution(__file__)


def play(n, moves, source=1, target=3):
    """규칙(한 번에 한 개, 큰 원판을 작은 원판 위에 올리지 않기)을 지키며 모두 옮겼는지"""
    pegs = {1: [], 2: [], 3: []}
    pegs[source] = list(range(n, 0, -1))
    for src, dst in moves:
        if not pegs[src]:
            return False
        disk = pegs[src][-1]
        if pegs[dst] and pegs[dst][-1] < disk:
            return False
        pegs[dst].append(pegs[src].pop())
    return pegs[target] == list(range(n, 0, -1))


def shortest_by_bfs(n):
    """상태 = 각 원판이 놓인 기둥 (원판 1..n). 최소 이동 횟수를 BFS 로 구한다."""
    start, goal = (1,) * n, (3,) * n
    dist = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if state == goal:
            return dist[state]
        tops = {}
        for disk in range(n, 0, -1):
            tops[state[disk - 1]] = disk  # 가장 작은 원판이 마지막에 덮어쓰므로 기둥마다 맨 위 원판이 남는다
        for src, disk in tops.items():
            for dst in (1, 2, 3):
                if dst != src and (dst not in tops or tops[dst] > disk):
                    nxt = list(state)
                    nxt[disk - 1] = dst
                    nxt = tuple(nxt)
                    if nxt not in dist:
                        dist[nxt] = dist[state] + 1
                        queue.append(nxt)


def test_readme_example_three_disks():
    assert solution.hanoi_moves(3) == [(1, 3), (1, 2), (3, 2), (1, 3), (2, 1), (2, 3), (1, 3)]
    assert solution.hanoi_moves(1) == [(1, 3)] and solution.hanoi_moves(0) == []


def test_moves_are_legal_and_have_minimum_length():
    for n in range(0, 11):
        moves = solution.hanoi_moves(n)
        assert play(n, moves), n
        assert len(moves) == solution.hanoi_count(n) == 2**n - 1


def test_minimum_matches_exhaustive_bfs():
    for n in range(1, 7):
        assert shortest_by_bfs(n) == solution.hanoi_count(n), n


def test_other_pegs_as_source_and_target():
    moves = solution.hanoi_moves(5, source=2, spare=3, target=1)
    assert play(5, moves, source=2, target=1)


def test_count_formula_matches_recurrence():
    for n in range(0, 20):
        assert solution.hanoi_count(n) == solution.hanoi_count_recursive(n) == 2**n - 1


def test_iterative_gives_the_same_moves():
    for n in range(1, 10):
        assert solution.hanoi_iterative(n) == solution.hanoi_moves(n), n


def test_kth_move_matches_full_list():
    for n in range(1, 9):
        detailed = solution.hanoi_moves_detailed(n)
        for k, expected in enumerate(detailed, start=1):
            assert solution.hanoi_kth_move(n, k) == expected, (n, k)
    # 매우 큰 n 도 O(n) 에 구한다: 가운데 이동은 가장 큰 원판
    assert solution.hanoi_kth_move(60, 2**59) == (60, 1, 3)


def test_disk_moved_at_is_the_ruler_sequence():
    assert [solution.disk_moved_at(k) for k in range(1, 16)] == [1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]
    for n in range(1, 9):
        detailed = solution.hanoi_moves_detailed(n)
        assert [d for d, _, _ in detailed] == [solution.disk_moved_at(k) for k in range(1, len(detailed) + 1)]


def test_main_prints_count_and_moves(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n"))
    solution.main()
    assert capsys.readouterr().out.splitlines() == ["7", "1 3", "1 2", "3 2", "1 3", "2 1", "2 3", "1 3"]


def test_main_prints_only_count_for_large_n(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("100\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == str(2**100 - 1)
