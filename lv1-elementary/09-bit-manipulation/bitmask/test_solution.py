"""solution.py 검증: 파이썬 set / itertools 와 비교"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def test_from_and_to_elements_roundtrip():
    rng = random.Random(0)
    for _ in range(300):
        elements = sorted(rng.sample(range(0, 20), rng.randint(0, 10)))
        mask = solution.from_elements(elements)
        assert solution.to_elements(mask) == elements
        assert solution.size(mask) == len(elements)
    assert solution.from_elements([0, 2, 3]) == 0b1101
    assert solution.from_elements([1, 1, 3, 3, 3]) == 0b1010  # 중복된 원소는 한 번만
    assert solution.to_elements(0) == []


def test_set_operations_match_python_sets():
    rng = random.Random(1)
    for _ in range(500):
        a = set(rng.sample(range(10), rng.randint(0, 10)))
        b = set(rng.sample(range(10), rng.randint(0, 10)))
        ma, mb = solution.from_elements(list(a)), solution.from_elements(list(b))
        assert solution.to_elements(ma | mb) == sorted(a | b)
        assert solution.to_elements(ma & mb) == sorted(a & b)
        assert solution.to_elements(ma & ~mb) == sorted(a - b)
        assert solution.to_elements(ma ^ mb) == sorted(a ^ b)
        assert solution.to_elements(solution.complement(ma, 10)) == sorted(set(range(10)) - a)
        k = rng.randint(0, 9)
        assert solution.contains(ma, k) == (k in a)
        assert solution.to_elements(solution.add(ma, k)) == sorted(a | {k})
        assert solution.to_elements(solution.remove(ma, k)) == sorted(a - {k})
        assert solution.to_elements(solution.toggle(ma, k)) == sorted(a ^ {k})


def test_full_mask_and_complement_are_nonnegative():
    assert solution.full_mask(0) == 0 and solution.full_mask(4) == 0b1111
    assert solution.complement(0b0101, 4) == 0b1010
    assert solution.complement(0, 5) == 31 and solution.complement(31, 5) == 0


def test_submasks_enumerates_exactly_the_subsets():
    for mask in range(0, 200):
        expected = sorted((sub for sub in range(mask + 1) if sub & mask == sub), reverse=True)
        assert solution.submasks(mask) == expected, mask
    assert solution.submasks(0) == [0]
    assert solution.submasks(0b101) == [0b101, 0b100, 0b001, 0b000]
    assert len(solution.submasks(0b1111111111)) == 2**10


def test_total_submasks_over_all_masks_is_three_to_the_n():
    n = 8
    assert sum(len(solution.submasks(mask)) for mask in range(1 << n)) == 3**n


def test_masks_with_k_bits_matches_combinations():
    for n in range(0, 9):
        for k in range(0, n + 2):
            expected = sorted(sum(1 << i for i in combo) for combo in itertools.combinations(range(n), k))
            if k == 0:
                expected = [0]
            assert solution.masks_with_k_bits(n, k) == expected, (n, k)
    assert solution.masks_with_k_bits(4, 2) == [0b0011, 0b0101, 0b0110, 0b1001, 0b1010, 0b1100]


def test_count_subsets_with_sum_matches_combinations():
    rng = random.Random(2)
    for _ in range(200):
        numbers = [rng.randint(-5, 5) for _ in range(rng.randint(0, 9))]
        target = rng.randint(-5, 5)
        expected = sum(
            1
            for r in range(1, len(numbers) + 1)
            for combo in itertools.combinations(numbers, r)
            if sum(combo) == target
        )
        assert solution.count_subsets_with_sum(numbers, target) == expected, (numbers, target)
    assert solution.count_subsets_with_sum([-7, -3, -2, 5, 8], 0) == 1
    # 합이 0 이어도 공집합은 세지 않는다
    assert solution.count_subsets_with_sum([1, 2], 0) == 0


def test_min_team_difference_matches_all_splits():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.choice([2, 4, 6, 8])
        s = [[0 if i == j else rng.randint(1, 20) for j in range(n)] for i in range(n)]
        best = None
        for team in itertools.combinations(range(n), n // 2):
            other = [i for i in range(n) if i not in team]
            a = sum(s[i][j] for i in team for j in team if i != j)
            b = sum(s[i][j] for i in other for j in other if i != j)
            best = abs(a - b) if best is None else min(best, abs(a - b))
        assert solution.min_team_difference(s) == best, s
    assert solution.min_team_difference([[0, 1, 2, 3], [4, 0, 5, 6], [7, 1, 0, 2], [3, 4, 5, 0]]) == 0


def test_process_commands_matches_python_set():
    rng = random.Random(4)
    for _ in range(100):
        commands, truth, expected = [], set(), []
        for _ in range(60):
            op = rng.choice(["add", "remove", "check", "toggle", "all", "empty"])
            if op in ("all", "empty"):
                commands.append(op)
                truth = set(range(1, 21)) if op == "all" else set()
            else:
                x = rng.randint(1, 20)
                commands.append(f"{op} {x}")
                if op == "add":
                    truth.add(x)
                elif op == "remove":
                    truth.discard(x)
                elif op == "toggle":
                    truth ^= {x}
                else:
                    expected.append(1 if x in truth else 0)
        assert solution.process_commands(commands) == expected


def test_all_command_only_fills_one_to_twenty():
    assert solution.process_commands(["all", "check 0", "check 1", "check 20", "check 21"]) == [0, 1, 1, 0]
    assert solution.process_commands(["all", "remove 5", "check 5", "toggle 5", "check 5"]) == [0, 1]


def test_main(monkeypatch, capsys):
    commands = "add 1\nadd 2\ncheck 1\ncheck 2\ncheck 3\nremove 2\ncheck 2\ntoggle 3\ncheck 3\nall\ncheck 10\nempty\ncheck 1\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("13\n" + commands))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "1", "0", "0", "1", "1", "0"]
