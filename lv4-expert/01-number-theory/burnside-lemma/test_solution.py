"""solution.py 검증: 모든 색칠을 나열해 궤도를 직접 세는 방법, 알려진 수열(OEIS), 닫힌 식과 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_count_cycles():
    assert solution.count_cycles([]) == 0
    assert solution.count_cycles([0, 1, 2]) == 3
    assert solution.count_cycles([1, 2, 0]) == 1
    assert solution.count_cycles([1, 0, 3, 2, 4]) == 3
    assert solution.count_cycles([1, 2, 3, 0]) == 1


def test_compose_and_group_generation():
    rotate = (1, 2, 3, 0)
    assert solution.compose(rotate, rotate) == (2, 3, 0, 1)
    assert solution.generate_group([rotate]) == sorted(solution.cyclic_group(4))
    reflect = (3, 2, 1, 0)
    group = solution.generate_group([rotate, reflect])
    assert len(group) == 8 and set(group) == set(solution.dihedral_group(4))
    assert len(solution.generate_group([(1, 0, 2, 3), (1, 2, 3, 0)])) == 24  # 대칭군 S4
    with pytest.raises(ValueError, match="생성원"):
        solution.generate_group([])


def test_burnside_matches_brute_force_for_rotations_and_dihedral_groups():
    for n in range(1, 8):
        for colors in (1, 2, 3):
            cyclic = solution.cyclic_group(n)
            dihedral = solution.dihedral_group(n)
            assert solution.burnside_count(cyclic, colors) == solution.brute_force_orbits(cyclic, n, colors), (n, colors)
            assert solution.burnside_count(dihedral, colors) == solution.brute_force_orbits(dihedral, n, colors), (n, colors)


def test_burnside_on_random_permutation_groups():
    rng = random.Random(0)
    for _ in range(60):
        n = rng.randint(2, 6)
        generators = []
        for _ in range(rng.randint(1, 3)):
            perm = list(range(n))
            rng.shuffle(perm)
            generators.append(perm)
        group = solution.generate_group(generators)
        colors = rng.randint(1, 3)
        assert solution.burnside_count(group, colors) == solution.brute_force_orbits(group, n, colors), (generators, colors)
    with pytest.raises(ValueError, match="비어"):
        solution.burnside_count([], 2)
    with pytest.raises(ValueError, match="군이 아닌"):
        solution.burnside_count([(0, 1, 2), (1, 0, 2), (0, 2, 1)], 2)  # 닫혀 있지 않아 평균이 정수가 아니다


def test_necklaces_and_bracelets_match_burnside_and_known_sequences():
    for n in range(1, 13):
        for k in range(1, 5):
            assert solution.necklaces(n, k) == solution.burnside_count(solution.cyclic_group(n), k), (n, k)
            assert solution.bracelets(n, k) == solution.burnside_count(solution.dihedral_group(n), k), (n, k)
    assert [solution.necklaces(n, 2) for n in range(1, 7)] == [2, 3, 4, 6, 8, 14]  # OEIS A000031
    assert [solution.necklaces(n, 3) for n in range(1, 7)] == [3, 6, 11, 24, 51, 130]  # A001867
    assert [solution.bracelets(n, 2) for n in range(1, 7)] == [2, 3, 4, 6, 8, 13]  # A000029
    assert [solution.bracelets(n, 3) for n in range(1, 7)] == [3, 6, 10, 21, 39, 92]  # A027671
    with pytest.raises(ValueError, match="1 이상"):
        solution.necklaces(0, 2)
    with pytest.raises(ValueError, match="1 이상"):
        solution.bracelets(3, 0)


def test_necklaces_mod_matches_the_exact_value_and_handles_huge_n():
    for n in range(1, 200):
        for k in (2, 3, 10):
            for mod in (1_000_000_007, 998244353):
                assert solution.necklaces_mod(n, k, mod) == solution.necklaces(n, k) % mod, (n, k, mod)
    with pytest.raises(ValueError, match="배수"):
        solution.necklaces_mod(1_000_000_007 * 3, 2, 1_000_000_007)
    with pytest.raises(ValueError, match="1 이상"):
        solution.necklaces_mod(0, 2, 7)
    # n = 10^12 (약수 169 개) 도 즉시 계산된다. 결과는 mod 안의 값
    value = solution.necklaces_mod(10**12, 5, 998244353)
    assert 0 <= value < 998244353
    # 소수 n 에서의 간단한 식: (k^p + (p - 1)·k) / p
    p = 1_000_003
    assert solution.necklaces_mod(p, 7, 998244353) == (pow(7, p, 998244353) + (p - 1) * 7) * pow(p, -1, 998244353) % 998244353


def test_cube_rotations_form_a_group_of_24_and_count_face_colorings():
    rotations = solution.cube_rotations()
    assert len(rotations) == 24 and len(set(rotations)) == 24
    assert all(sorted(g) == list(range(6)) for g in rotations)
    # 위-아래 면은 서로 맞은편이므로 회전해도 (0, 1) 은 (0, 1) 이나 (1, 0) 이나 다른 맞은편 쌍으로 간다: 맞은편 쌍 {0,1}, {2,3}, {4,5} 보존
    opposite = {frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5))}
    for g in rotations:
        assert {frozenset((g[a], g[b])) for a, b in ((0, 1), (2, 3), (4, 5))} == opposite
    assert [solution.cube_face_colorings(k) for k in range(1, 5)] == [1, 10, 57, 240]
    for k in range(1, 8):
        assert solution.cube_face_colorings(k) == (k**6 + 3 * k**4 + 12 * k**3 + 8 * k**2) // 24
    for colors in (1, 2, 3):
        assert solution.brute_force_orbits(rotations, 6, colors) == solution.cube_face_colorings(colors)


def test_unlabeled_graph_counts_match_oeis():
    assert [solution.count_unlabeled_graphs(n) for n in range(0, 7)] == [1, 1, 2, 4, 11, 34, 156]  # A000088
    with pytest.raises(ValueError, match="n 은"):
        solution.count_unlabeled_graphs(-1)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6 3\n"))
    solution.main()
    assert capsys.readouterr().out == "130\n92\n"
