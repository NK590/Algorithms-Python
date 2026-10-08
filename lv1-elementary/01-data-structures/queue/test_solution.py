"""solution.py 검증: 세 가지 큐를 같은 무작위 연산으로 리스트 모델과 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


@pytest.mark.parametrize("make", [solution.Queue, solution.TwoStackQueue])
def test_unbounded_queues_match_a_list_model(make):
    rng = random.Random(0)
    for _ in range(200):
        queue, model = make(), []
        for _ in range(80):
            if model and rng.random() < 0.5:
                assert queue.front() == model[0]
                assert queue.dequeue() == model.pop(0)
            else:
                value = rng.randint(0, 99)
                queue.enqueue(value)
                model.append(value)
            assert len(queue) == len(model)


def test_circular_queue_matches_a_bounded_list_model_and_wraps_around():
    rng = random.Random(1)
    for _ in range(200):
        capacity = rng.randint(1, 6)
        queue, model = solution.CircularQueue(capacity), []
        for _ in range(100):
            if model and rng.random() < 0.5:
                assert queue.dequeue() == model.pop(0)
            else:
                value = rng.randint(0, 99)
                accepted = queue.enqueue(value)
                assert accepted == (len(model) < capacity)
                if accepted:
                    model.append(value)
            assert len(queue) == len(model)


@pytest.mark.parametrize("make", [solution.Queue, solution.TwoStackQueue, lambda: solution.CircularQueue(3)])
def test_empty_queue_raises(make):
    with pytest.raises(IndexError):
        make().dequeue()


def test_fifo_order_example():
    queue = solution.Queue()
    for x in (1, 2, 3):
        queue.enqueue(x)
    assert [queue.dequeue() for _ in range(3)] == [1, 2, 3]


def test_last_card_matches_formula():
    for n in range(1, 300):
        assert solution.last_card(n) == solution.last_card_formula(n), n
    assert [solution.last_card(n) for n in (1, 2, 3, 4, 5, 6)] == [1, 2, 2, 4, 2, 4]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "4"
