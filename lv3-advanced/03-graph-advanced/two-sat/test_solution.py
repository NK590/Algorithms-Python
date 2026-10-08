"""solution.py 검증: 모든 값 배정을 시도하는 완전탐색과 비교하고, 돌려준 배정이 모든 절을 만족하는지 직접 확인"""
import io
import itertools
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def satisfies(assignment, clauses):
    return all(assignment[i] == a or assignment[j] == b for i, a, j, b in clauses)


def brute_force_satisfiable(n, clauses):
    return any(satisfies(assignment, clauses) for assignment in itertools.product([False, True], repeat=n))


def build(n, clauses):
    sat = solution.TwoSat(n)
    for i, a, j, b in clauses:
        sat.add_clause(i, a, j, b)
    return sat


def test_satisfiability_matches_brute_force_and_assignment_is_valid():
    rng = random.Random(0)
    satisfiable_seen = unsatisfiable_seen = 0
    for _ in range(1500):
        n = rng.randint(1, 7)
        clauses = [(rng.randrange(n), rng.random() < 0.5, rng.randrange(n), rng.random() < 0.5) for _ in range(rng.randint(0, 3 * n))]
        result = build(n, clauses).solve()
        expected = brute_force_satisfiable(n, clauses)
        assert (result is not None) == expected, (n, clauses)
        if result is None:
            unsatisfiable_seen += 1
        else:
            satisfiable_seen += 1
            assert len(result) == n and satisfies(result, clauses), (n, clauses, result)
    assert satisfiable_seen > 100 and unsatisfiable_seen > 100  # 두 경우가 모두 충분히 나오는 입력인지 확인


def test_classic_unsatisfiable_formula():
    # (x ∨ y) ∧ (x ∨ ¬y) ∧ (¬x ∨ y) ∧ (¬x ∨ ¬y)
    clauses = [(0, True, 1, True), (0, True, 1, False), (0, False, 1, True), (0, False, 1, False)]
    assert build(2, clauses).solve() is None
    assert build(2, clauses[:3]).solve() == [True, True]


def test_force_equal_not_equal_and_implication():
    sat = solution.TwoSat(3)
    sat.force(0, True)
    sat.add_not_equal(0, 1)
    sat.add_equal(1, 2)
    assert sat.solve() == [True, False, False]
    sat.force(2, True)  # x1 == x2 == True 인데 x0 != x1, x0 == True 와 모순
    assert sat.solve() is None
    imp = solution.TwoSat(2)
    imp.add_implication(0, True, 1, True)
    imp.force(0, True)
    assert imp.solve() == [True, True]


def test_equal_allows_both_values_and_helpers_match_brute_force_semantics():
    eq = solution.TwoSat(2)
    eq.add_equal(0, 1)
    eq.force(0, True)
    assert eq.solve() == [True, True]  # 같다는 조건이 둘 다 참인 배정을 막지 않는다
    eq = solution.TwoSat(2)
    eq.add_equal(0, 1)
    eq.force(1, False)
    assert eq.solve() == [False, False]
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(1, 5)
        sat = solution.TwoSat(n)
        constraints = []
        for _ in range(rng.randint(0, 6)):
            kind = rng.choice(["equal", "not_equal", "implication", "force"])
            i, j = rng.randrange(n), rng.randrange(n)
            a, b = rng.random() < 0.5, rng.random() < 0.5
            if kind == "equal":
                sat.add_equal(i, j)
                constraints.append(lambda x, i=i, j=j: x[i] == x[j])
            elif kind == "not_equal":
                sat.add_not_equal(i, j)
                constraints.append(lambda x, i=i, j=j: x[i] != x[j])
            elif kind == "implication":
                sat.add_implication(i, a, j, b)
                constraints.append(lambda x, i=i, a=a, j=j, b=b: x[i] != a or x[j] == b)
            else:
                sat.force(i, a)
                constraints.append(lambda x, i=i, a=a: x[i] == a)
        result = sat.solve()
        expected = any(all(c(x) for c in constraints) for x in itertools.product([False, True], repeat=n))
        assert (result is not None) == expected, (n,)
        if result is not None:
            assert all(c(result) for c in constraints)


def test_no_variables_and_no_clauses():
    assert solution.TwoSat(0).solve() == []
    result = solution.TwoSat(3).solve()
    assert result is not None and len(result) == 3


def test_large_planted_instance_is_solved_without_recursion():
    rng = random.Random(1)
    n, m = 100_000, 200_000
    hidden = [rng.random() < 0.5 for _ in range(n)]
    sat = solution.TwoSat(n)
    clauses = []
    for _ in range(m):
        i, j = rng.randrange(n), rng.randrange(n)
        a = rng.random() < 0.5
        b = rng.random() < 0.5
        if hidden[i] != a and hidden[j] != b:  # 숨긴 배정을 만족하도록 한쪽 리터럴을 고친다
            a = hidden[i]
        clauses.append((i, a, j, b))
        sat.add_clause(i, a, j, b)
    result = sat.solve()
    assert result is not None and satisfies(result, clauses)
    # 사슬 모양의 함의 (깊은 SCC 탐색)
    chain = solution.TwoSat(n)
    for i in range(n - 1):
        chain.add_implication(i, True, i + 1, True)
    chain.force(0, True)
    assert chain.solve() == [True] * n


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"3 4\n1 2\n-1 3\n-2 -3\n1 3\n")))
    solution.main()
    lines = capsys.readouterr().out.split("\n")
    assert lines[0] == "1"
    values = list(map(int, lines[1].split()))
    x = [bool(v) for v in values]
    assert (x[0] or x[1]) and (not x[0] or x[2]) and (not x[1] or not x[2]) and (x[0] or x[2])
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(b"2 4\n1 2\n1 -2\n-1 2\n-1 -2\n")))
    solution.main()
    assert capsys.readouterr().out.strip() == "0"
