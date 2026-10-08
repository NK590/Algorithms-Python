"""solution.py 검증: collections.deque 와 무작위 연산으로 비교 (배열이 꽉 차서 커지는 순간과 한 바퀴 도는 순간 포함)"""
import io
import random
from collections import deque as reference_deque

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_matches_collections_deque():
    rng = random.Random(0)
    for _ in range(300):
        mine, model = solution.Deque(capacity=rng.randint(1, 5)), reference_deque()
        for _ in range(120):
            action = rng.choice(["pf", "pb", "of", "ob", "pf", "pb"])
            if action == "pf":
                v = rng.randint(0, 99)
                mine.push_front(v)
                model.appendleft(v)
            elif action == "pb":
                v = rng.randint(0, 99)
                mine.push_back(v)
                model.append(v)
            elif model and action == "of":
                assert mine.pop_front() == model.popleft()
            elif model and action == "ob":
                assert mine.pop_back() == model.pop()
            assert mine.to_list() == list(model) and len(mine) == len(model)
            if model:
                assert mine.front() == model[0] and mine.back() == model[-1]


def test_works_as_stack_and_as_queue():
    deque = solution.Deque()
    for x in (1, 2, 3):
        deque.push_back(x)
    assert [deque.pop_back() for _ in range(3)] == [3, 2, 1]  # 한쪽 끝에서만 쓰면 스택
    for x in (1, 2, 3):
        deque.push_back(x)
    assert [deque.pop_front() for _ in range(3)] == [1, 2, 3]  # 반대쪽에서 꺼내면 큐


def test_empty_deque_raises():
    for operation in ("pop_front", "pop_back", "front", "back"):
        with pytest.raises(IndexError):
            getattr(solution.Deque(), operation)()


def test_growth_keeps_order_when_head_is_in_the_middle():
    deque = solution.Deque(capacity=2)
    deque.push_back(2)
    deque.push_front(1)  # 머리가 배열 끝으로 돌아간 상태에서
    deque.push_back(3)   # 가득 차서 커진다
    deque.push_back(4)
    assert deque.to_list() == [1, 2, 3, 4]


def test_is_palindrome_matches_slicing():
    rng = random.Random(1)
    for _ in range(500):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 9)))
        assert solution.is_palindrome(s) == (s == s[::-1])


def test_process_commands_example():
    commands = ["push_back 1", "push_front 2", "front", "back", "size", "empty", "pop_front", "pop_back",
                "pop_front", "size", "empty", "pop_back", "push_front 3", "empty", "front"]
    assert solution.process_commands(commands) == ["2", "1", "2", "0", "2", "1", "-1", "0", "1", "-1", "0", "3"]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\npush_back 5\npush_front 7\nback\npop_front\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["5", "7"]
