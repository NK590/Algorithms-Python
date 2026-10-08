"""solution.py 검증: 파이썬 list 를 모델로 한 무작위 연산 비교 + 사이클 판별은 방문 집합 방식과 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_operations_match_a_list_model():
    rng = random.Random(0)
    for _ in range(300):
        linked, model = solution.LinkedList(), []
        for _ in range(40):
            action = rng.choice(["append", "prepend", "remove", "insert_after", "reverse"])
            value = rng.randint(0, 5)
            if action == "append":
                linked.append(value)
                model.append(value)
            elif action == "prepend":
                linked.prepend(value)
                model.insert(0, value)
            elif action == "remove":
                expected = value in model
                if expected:
                    model.remove(value)
                assert linked.remove(value) == expected
            elif action == "insert_after" and model:
                target = rng.choice(model)
                node = linked.find(target)
                linked.insert_after(node, value)
                model.insert(model.index(target) + 1, value)
            elif action == "reverse":
                linked.reverse()
                model.reverse()
            assert linked.to_list() == model and len(linked) == len(model)


def test_find_and_remove_head_and_tail():
    linked = solution.LinkedList([1, 2, 3])
    assert linked.find(2).value == 2 and linked.find(9) is None
    assert linked.remove(1) and linked.to_list() == [2, 3]  # 머리를 지우면 head 가 바뀐다
    assert linked.remove(3) and linked.to_list() == [2]
    assert not linked.remove(7)
    assert linked.remove(2) and linked.to_list() == [] and linked.head is None


def test_middle_matches_index_n_over_2():
    for n in range(1, 30):
        values = list(range(n))
        assert solution.LinkedList(values).middle() == values[n // 2]
    with pytest.raises(IndexError):
        solution.LinkedList().middle()


def make_chain(n, cycle_to):
    """n 개의 노드를 잇고, cycle_to 가 None 이 아니면 마지막 노드를 cycle_to 번 노드에 이어 사이클을 만든다."""
    nodes = [solution.Node(i) for i in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if cycle_to is not None and nodes:
        nodes[-1].next = nodes[cycle_to]
    return nodes[0] if nodes else None


def has_cycle_by_visited_set(head):
    seen = set()
    while head is not None:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False


def test_has_cycle_matches_visited_set():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(0, 12)
        cycle_to = rng.randrange(n) if n and rng.random() < 0.6 else None
        head = make_chain(n, cycle_to)
        assert solution.has_cycle(head) == has_cycle_by_visited_set(head) == (cycle_to is not None)


def test_merge_sorted():
    rng = random.Random(2)
    for _ in range(300):
        a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
        b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
        merged = solution.merge_sorted(solution.LinkedList(a), solution.LinkedList(b))
        assert merged.to_list() == sorted(a + b) and len(merged) == len(a) + len(b)


def test_long_list_does_not_use_recursion():
    linked = solution.LinkedList(range(3000))
    linked.reverse()
    assert linked.to_list()[:3] == [2999, 2998, 2997]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n1 2 3 4\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["4", "3", "2", "1"]
