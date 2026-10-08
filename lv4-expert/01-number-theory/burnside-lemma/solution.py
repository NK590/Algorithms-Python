"""번사이드 보조정리(Burnside's Lemma) — 회전·뒤집기로 같아지는 배치를 한 가지로 보고 서로 다른 것의 수를 세기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 군 G 가 대상(색칠 등) 에 작용할 때, 서로 다른 궤도(같은 것끼리 묶은 종류) 의 수 = (1/|G|) Σ_{g∈G} (g 로 변하지 않는 대상의 수).
- n 개 자리를 k 가지 색으로 칠할 때, 자리의 순열 g 로 변하지 않는 색칠은 g 의 각 순환(cycle) 안의 자리가 모두 같은 색이어야 하므로 k^(순환의 수).
- burnside_count(group, k): 자리 순열의 모임 group 이 군일 때 서로 다른 색칠의 수.  generate_group: 생성원들로 군을 만든다.
- necklaces(n, k): 회전만 같다고 볼 때 (1/n)·Σ_{d|n} φ(d)·k^(n/d).  bracelets(n, k): 뒤집기도 같다고 볼 때.  necklaces_mod: n 이 매우 클 때의 나머지.
- cube_rotations / cube_face_colorings: 정육면체의 24 가지 회전과 면 색칠.  count_unlabeled_graphs(n): 정점 이름을 지운 그래프의 수 (n! 개의 순열이 변 쌍에 작용).
- 직접 실행하면 `n k` 를 받아 구슬 n 개를 k 가지 색으로 꿴 목걸이의 수를 (회전만 / 회전과 뒤집기까지) 두 줄로 출력합니다.
"""
import sys
from fractions import Fraction
from itertools import combinations, permutations, product
from typing import Iterable, Sequence

Permutation = tuple[int, ...]


def count_cycles(perm: Sequence[int]) -> int:
    """순열의 순환(cycle) 의 수 (고정점도 길이 1 의 순환)."""
    seen = [False] * len(perm)
    cycles = 0
    for start in range(len(perm)):
        if not seen[start]:
            cycles += 1
            i = start
            while not seen[i]:
                seen[i] = True
                i = perm[i]
    return cycles


def compose(a: Sequence[int], b: Sequence[int]) -> Permutation:
    """(a ∘ b)(i) = a[b[i]]."""
    return tuple(a[i] for i in b)


def generate_group(generators: Iterable[Sequence[int]]) -> list[Permutation]:
    """생성원들로 만들어지는 순열군 전체 (너비 우선으로 곱해 가며 닫는다)."""
    gens = [tuple(g) for g in generators]
    if not gens:
        raise ValueError("생성원이 하나 이상 필요합니다")
    n = len(gens[0])
    identity = tuple(range(n))
    group = {identity}
    frontier = [identity]
    while frontier:
        next_frontier = []
        for g in frontier:
            for h in gens:
                product_ = compose(h, g)
                if product_ not in group:
                    group.add(product_)
                    next_frontier.append(product_)
        frontier = next_frontier
    return sorted(group)


def cyclic_group(n: int) -> list[Permutation]:
    """원형으로 놓인 n 자리의 회전 n 개."""
    return [tuple((i + j) % n for i in range(n)) for j in range(n)]


def dihedral_group(n: int) -> list[Permutation]:
    """회전 n 개와 뒤집기 n 개 (n ≤ 2 에서는 겹치는 것을 한 번만)."""
    rotations = [tuple((i + j) % n for i in range(n)) for j in range(n)]
    reflections = [tuple((j - i) % n for i in range(n)) for j in range(n)]
    return sorted(set(rotations) | set(reflections))


def burnside_count(group: Sequence[Sequence[int]], colors: int) -> int:
    """군 group 이 자리에 작용할 때 colors 가지 색으로 칠한 것을 같은 것끼리 묶은 종류의 수. 군의 모든 원소를 훑는다."""
    if not group:
        raise ValueError("군이 비어 있습니다")
    total = sum(colors ** count_cycles(g) for g in group)
    orbits = Fraction(total, len(group))
    if orbits.denominator != 1:
        raise ValueError("입력이 군이 아닌 것 같습니다 (평균이 정수가 아닙니다)")
    return int(orbits)


def brute_force_orbits(group: Sequence[Sequence[int]], n: int, colors: int) -> int:
    """모든 색칠을 나열해 군의 작용으로 같아지는 것의 최소 대표를 세는 기준 구현 (colors^n 가지를 훑는다)."""
    representatives = set()
    for coloring in product(range(colors), repeat=n):
        representatives.add(min(tuple(coloring[g[i]] for i in range(n)) for g in group))
    return len(representatives)


def _factorize(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def _divisors_with_phi(n: int) -> list[tuple[int, int]]:
    """(d, φ(d)) 목록 — n 의 모든 약수 d."""
    result = [(1, 1)]
    for p, e in _factorize(n).items():
        extended = []
        for d, phi in result:
            extended.append((d, phi))
            for k in range(1, e + 1):
                extended.append((d * p**k, phi * (p**k - p ** (k - 1))))
        result = extended
    return sorted(result)


def _rotation_total(n: int, k: int) -> int:
    return sum(phi * k ** (n // d) for d, phi in _divisors_with_phi(n))


def necklaces(n: int, k: int) -> int:
    """회전으로 같은 것을 하나로 본, k 색 구슬 n 개 목걸이의 수 = (1/n) Σ_{d|n} φ(d)·k^(n/d)."""
    if n < 1 or k < 1:
        raise ValueError("n 과 k 는 1 이상이어야 합니다")
    return _rotation_total(n, k) // n


def bracelets(n: int, k: int) -> int:
    """회전과 뒤집기로 같은 것을 하나로 본 팔찌의 수. 뒤집기 n 개의 합: n 이 홀수면 n·k^((n+1)/2), 짝수면 (n/2)(k^(n/2+1) + k^(n/2))."""
    if n < 1 or k < 1:
        raise ValueError("n 과 k 는 1 이상이어야 합니다")
    if n % 2:
        reflections = n * k ** ((n + 1) // 2)
    else:
        reflections = (n // 2) * (k ** (n // 2 + 1) + k ** (n // 2))
    return (_rotation_total(n, k) + reflections) // (2 * n)


def necklaces_mod(n: int, k: int, mod: int) -> int:
    """necklaces(n, k) mod 소수 mod. n 이 매우 커도 약수 개수만큼의 거듭제곱으로 계산 (n 은 mod 의 배수가 아니어야 한다)."""
    if n < 1 or k < 1:
        raise ValueError("n 과 k 는 1 이상이어야 합니다")
    if n % mod == 0:
        raise ValueError("n 이 mod 의 배수면 n 의 역원이 없습니다")
    total = sum(phi % mod * pow(k, n // d, mod) for d, phi in _divisors_with_phi(n)) % mod
    return total * pow(n, -1, mod) % mod


def cube_rotations() -> list[Permutation]:
    """정육면체의 24 가지 회전을 6 개 면(0=위, 1=아래, 2=앞, 3=뒤, 4=왼, 5=오른) 의 순열로."""
    # 위-아래 축으로 90° (앞→오른→뒤→왼→앞), 앞-뒤 축으로 90° (위→오른→아래→왼→위)
    around_vertical = (0, 1, 4, 5, 3, 2)
    around_depth = (4, 5, 2, 3, 1, 0)
    return generate_group([around_vertical, around_depth])


def cube_face_colorings(k: int) -> int:
    """정육면체의 면을 k 가지 색으로 칠하는 서로 다른 방법의 수 (회전해서 같으면 같은 것) = (k⁶ + 3k⁴ + 12k³ + 8k²)/24."""
    return burnside_count(cube_rotations(), k)


def count_unlabeled_graphs(n: int) -> int:
    """정점 n 개의 단순 그래프를 정점 이름을 지우고 센 수. 정점의 순열 n! 개가 변의 쌍 (i, j) 에 작용하고, 변이 있는지 없는지 두 색."""
    if n < 0:
        raise ValueError("n 은 0 이상이어야 합니다")
    pairs = list(combinations(range(n), 2))
    index = {pair: i for i, pair in enumerate(pairs)}
    total = 0
    count = 0
    for perm in permutations(range(n)):
        pair_perm = [index[tuple(sorted((perm[a], perm[b])))] for a, b in pairs]
        total += 2 ** count_cycles(pair_perm)
        count += 1
    return total // count


def main() -> None:
    n, k = (int(x) for x in sys.stdin.read().split()[:2])
    print(necklaces(n, k))
    print(bracelets(n, k))


if __name__ == "__main__":
    main()
