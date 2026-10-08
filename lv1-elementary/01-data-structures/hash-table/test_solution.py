"""solution.py 검증: 내장 dict 와 무작위 연산 비교 + 모든 키가 충돌하는 최악의 경우"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


class AlwaysCollides:
    """해시 값이 항상 같아서 모든 키가 같은 칸에 들어가는 키. 체이닝이 충돌을 올바르게 처리하는지 본다."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, AlwaysCollides) and self.name == other.name

    def __repr__(self):
        return f"K({self.name})"


def test_matches_dict_under_random_operations():
    rng = random.Random(0)
    for _ in range(200):
        table, model = solution.HashMap(capacity=rng.randint(1, 8)), {}
        for _ in range(150):
            key = rng.randint(0, 40)
            action = rng.choice(["put", "put", "get", "remove", "contains"])
            if action == "put":
                value = rng.randint(0, 99)
                table.put(key, value)
                model[key] = value
            elif action == "get":
                assert table.get(key, "none") == model.get(key, "none")
            elif action == "remove":
                assert table.remove(key) == (key in model)
                model.pop(key, None)
            else:
                assert (key in table) == (key in model)
            assert len(table) == len(model)
        assert sorted(table.items()) == sorted(model.items())


def test_colliding_keys_are_still_distinguished():
    table = solution.HashMap()
    keys = [AlwaysCollides(i) for i in range(50)]
    for i, key in enumerate(keys):
        table.put(key, i)
    assert len(table) == 50
    assert all(table.get(key) == i for i, key in enumerate(keys))
    assert table.remove(keys[10]) and keys[10] not in table and keys[11] in table


def test_resizing_keeps_the_load_factor_low_and_all_items():
    table = solution.HashMap(capacity=2)
    for i in range(1000):
        table.put(i, i * i)
        assert len(table) <= solution.HashMap.LOAD_FACTOR_LIMIT * table.capacity + 1
    assert table.capacity >= 1000 / 0.75 / 2
    assert all(table.get(i) == i * i for i in range(1000))


def test_overwriting_does_not_grow_the_table():
    table = solution.HashMap()
    for _ in range(100):
        table.put("a", 1)
    assert len(table) == 1 and table.get("a") == 1


def test_two_sum_matches_brute_force():
    rng = random.Random(1)
    for _ in range(500):
        numbers = [rng.randint(-5, 5) for _ in range(rng.randint(0, 8))]
        target = rng.randint(-8, 8)
        result = solution.two_sum(numbers, target)
        exists = any(numbers[i] + numbers[j] == target for i in range(len(numbers)) for j in range(i + 1, len(numbers)))
        if exists:
            i, j = result
            assert i < j and numbers[i] + numbers[j] == target
        else:
            assert result is None


def test_group_anagrams():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    assert solution.group_anagrams(words) == [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    assert solution.group_anagrams([]) == []


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n6 3 2 10\n5\n10 9 -5 2 3\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "0", "0", "1", "1"]
