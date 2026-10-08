"""solution.py 검증: 손으로 따라간 예제 + 요세푸스는 시뮬레이션과 점화식을 서로 비교"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_robot_examples():
    assert solution.simulate_robot("", 3, 3) == (0, 0, "E")
    assert solution.simulate_robot("FF", 3, 3) == (0, 2, "E")
    assert solution.simulate_robot("FFF", 3, 3) == (0, 2, "E")  # 오른쪽 벽에 막힌다
    assert solution.simulate_robot("RFF", 3, 3) == (2, 0, "S")
    assert solution.simulate_robot("LF", 3, 3) == (0, 0, "N")  # 위쪽 벽에 막힌다
    # (0,0)동 → F (0,1) → R 남 → F (1,1) → R 서 → F (1,0) → L 남 → F (2,0)
    assert solution.simulate_robot("FRFRFLF", 3, 3) == (2, 0, "S")


def test_robot_spiral_path():
    # 3×3 을 한 바퀴 도는 명령: 오른쪽 2칸, 아래 2칸, 왼쪽 2칸, 위 1칸
    assert solution.simulate_robot("FF" + "RFF" + "RFF" + "RF", 3, 3) == (1, 0, "N")


def test_four_turns_restore_facing_and_robot_stays_inside():
    rng = random.Random(0)
    for _ in range(500):
        commands = "".join(rng.choice("FLR") for _ in range(rng.randint(0, 30)))
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        r, c, facing = solution.simulate_robot(commands, rows, cols)
        assert 0 <= r < rows and 0 <= c < cols and facing in "NESW"
        assert solution.simulate_robot(commands + "RRRR", rows, cols) == (r, c, facing)


def test_josephus_order_example():
    assert solution.josephus_order(7, 3) == [3, 6, 2, 7, 5, 1, 4]
    assert solution.josephus_order(1, 5) == [1]
    assert solution.josephus_order(5, 1) == [1, 2, 3, 4, 5]


def test_josephus_simulation_agrees_with_recurrence():
    for n in range(1, 60):
        for k in range(1, 12):
            order = solution.josephus_order(n, k)
            assert sorted(order) == list(range(1, n + 1))
            assert order[-1] == solution.josephus_last(n, k), (n, k)


def test_add_minutes():
    assert solution.add_minutes(14, 30, 20) == (14, 50)
    assert solution.add_minutes(23, 40, 30) == (0, 10)
    assert solution.add_minutes(0, 0, 0) == (0, 0)
    assert solution.add_minutes(0, 5, -10) == (23, 55)
    assert solution.add_minutes(10, 0, 24 * 60) == (10, 0)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("7 3\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "<3, 6, 2, 7, 5, 1, 4>"
