"""다항식 연산(Polynomial Operations) — 곱셈 하나를 빠르게 만든 뒤 뉴턴 방법으로 역수·로그·지수·거듭제곱·제곱근·나눗셈을, 부분곱 트리로 다점 계산·보간을 O(n log n) ~ O(n log² n) 에 하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 다항식(형식적 거듭제곱 급수)은 낮은 차수부터의 계수 리스트이고, 계수는 소수 mod 위에서 다룬다. n 은 "x^n 으로 나눈 나머지까지만 구한다" (항의 개수).
- multiply(a, b): 작으면 학교 방법, 크면 크로네커 치환 — 계수를 일정한 간격으로 늘어놓아 하나의 큰 정수로 만들고 파이썬의 큰 정수 곱셈을 쓴다. NTT 가 필요하지 않아 *어떤* 소수 mod 에서도 된다.
- 뉴턴 방법: g 가 f(g) = 0 의 근을 x^m 까지 맞게 알고 있으면 g - f(g)/f'(g) 는 x^{2m} 까지 맞다. 정밀도가 두 배씩 늘어 마지막 곱셈의 비용이 지배한다.
  poly_inverse: g ← g(2 - f g).  poly_log: f'/f 를 적분.  poly_exp: g ← g(1 - log g + f).  poly_sqrt: g ← (g + f/g)/2.  poly_pow: f^k = exp(k log f) (앞의 0 과 상수항은 따로 처리).
- poly_divmod: a = b q + r 에서 뒤집은 다항식의 역수로 몫을 한 번에 구한다 (몫은 뒤집으면 x^{deg a - deg b + 1} 의 나머지로 정해진다).
- multipoint_evaluate: ∏(x - x_i) 의 부분곱 트리를 만들고 f 를 루트에서 잎으로 나머지를 내려 보낸다. interpolate: P'(x_i) 로 가중치를 구하고 부분곱 트리를 올라가며 합친다. taylor_shift: f(x + c) 를 컨볼루션 한 번으로.
- 응용: bell_numbers (exp(e^x - 1)), partition_numbers (오일러의 오각수 급수의 역수), catalan_numbers (제곱근).
- 직접 실행하면 Library Checker "Exp of Formal Power Series" 형식 — `N`, 이어서 a_0 … a_{N-1} (a_0 = 0) — 를 받아 exp(f) 의 처음 N 개 계수를 mod 998244353 으로 출력합니다.
"""
import sys
from typing import Optional, Sequence

MOD = 998244353
_NAIVE_LIMIT = 24  # 짧은 쪽이 이만큼 이하면 학교 방법이 더 빠르다


def _trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def multiply(a: Sequence[int], b: Sequence[int], mod: int = MOD) -> list[int]:
    """다항식 곱 (계수는 mod 로 줄여서 돌려준다)."""
    if not a or not b:
        return []
    if min(len(a), len(b)) <= _NAIVE_LIMIT:
        result = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    result[i + j] += x * y
        return [c % mod for c in result]
    # 크로네커 치환: 곱의 계수는 (mod-1)² · min(len) 보다 작으므로 그만큼의 비트 칸에 담는다
    slot = (2 * mod.bit_length() + min(len(a), len(b)).bit_length() + 7) // 8
    big_a = int.from_bytes(b"".join((x % mod).to_bytes(slot, "little") for x in a), "little")
    big_b = int.from_bytes(b"".join((y % mod).to_bytes(slot, "little") for y in b), "little")
    count = len(a) + len(b) - 1
    raw = (big_a * big_b).to_bytes(count * slot, "little")
    return [int.from_bytes(raw[i * slot:(i + 1) * slot], "little") % mod for i in range(count)]


def _inverses(n: int, mod: int) -> list[int]:
    """1..n 의 역원 (0 번 칸은 비워 둔다)."""
    inv = [0, 1] + [0] * max(0, n - 1)
    for i in range(2, n + 1):
        inv[i] = (mod - (mod // i) * inv[mod % i] % mod) % mod
    return inv[:n + 1]


def poly_derivative(f: Sequence[int], mod: int = MOD) -> list[int]:
    return [i * f[i] % mod for i in range(1, len(f))]


def poly_integral(f: Sequence[int], mod: int = MOD) -> list[int]:
    inv = _inverses(len(f) + 1, mod)
    return [0] + [f[i] * inv[i + 1] % mod for i in range(len(f))]


def poly_inverse(f: Sequence[int], n: int, mod: int = MOD) -> list[int]:
    """1/f 를 x^n 까지 (f[0] != 0)."""
    if not f or f[0] % mod == 0:
        raise ValueError("상수항이 0 인 급수는 역수가 없습니다")
    g = [pow(f[0], mod - 2, mod)]
    size = 1
    while size < n:
        size *= 2
        fg = multiply(f[:size], g, mod)[:size]
        two_minus = [(-x) % mod for x in fg]
        two_minus[0] = (two_minus[0] + 2) % mod
        g = multiply(g, two_minus, mod)[:size]
    return g[:n] + [0] * (n - len(g))


def poly_log(f: Sequence[int], n: int, mod: int = MOD) -> list[int]:
    """ln f 를 x^n 까지 (f[0] = 1)."""
    if not f or f[0] % mod != 1:
        raise ValueError("log 는 상수항이 1 인 급수에서만 정의됩니다")
    quotient = multiply(poly_derivative(f[:n], mod), poly_inverse(f, n - 1, mod), mod)[:n - 1]
    result = poly_integral(quotient, mod)[:n]
    return result + [0] * (n - len(result))


def poly_exp(f: Sequence[int], n: int, mod: int = MOD) -> list[int]:
    """e^f 를 x^n 까지 (f[0] = 0)."""
    if f and f[0] % mod != 0:
        raise ValueError("exp 는 상수항이 0 인 급수에서만 정의됩니다")
    g = [1]
    size = 1
    padded = list(f) + [0] * max(0, n - len(f))
    while size < n:
        size *= 2
        log_g = poly_log(g + [0] * (size - len(g)), size, mod)
        h = [(padded[i] if i < len(padded) else 0) - log_g[i] for i in range(size)]
        h[0] += 1
        g = multiply(g, [x % mod for x in h], mod)[:size]
    return g[:n] + [0] * (n - len(g))


def poly_pow(f: Sequence[int], k: int, n: int, mod: int = MOD) -> list[int]:
    """f^k 를 x^n 까지 (k ≥ 0 은 임의로 커도 된다)."""
    if k < 0:
        raise ValueError("k 는 0 이상이어야 합니다")
    if n == 0:
        return []
    if k == 0:
        return [1] + [0] * (n - 1)
    first = next((i for i, c in enumerate(f) if c % mod), None)
    if first is None or first * k >= n:
        return [0] * n
    lead = f[first] % mod
    lead_inv = pow(lead, mod - 2, mod)
    normalized = [c * lead_inv % mod for c in f[first:]]
    length = n - first * k
    log_g = poly_log(normalized + [0] * max(0, length - len(normalized)), length, mod)
    powered = poly_exp([c * k % mod for c in log_g], length, mod)
    factor = pow(lead, k, mod)
    return [0] * (first * k) + [c * factor % mod for c in powered]


def mod_sqrt(a: int, mod: int) -> Optional[int]:
    """x² ≡ a (mod p) 의 해 중 작은 쪽 (토넬리-섕크스). 없으면 None."""
    a %= mod
    if a == 0:
        return 0
    if pow(a, (mod - 1) // 2, mod) != 1:
        return None
    q, s = mod - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (mod - 1) // 2, mod) != mod - 1:
        z += 1
    m, c, t, r = s, pow(z, q, mod), pow(a, q, mod), pow(a, (q + 1) // 2, mod)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % mod
            i += 1
        b = pow(c, 1 << (m - i - 1), mod)
        m, c, t, r = i, b * b % mod, t * b * b % mod, r * b % mod
    return min(r, mod - r)


def poly_sqrt(f: Sequence[int], n: int, mod: int = MOD) -> Optional[list[int]]:
    """g² = f (mod x^n) 인 g (상수항이 작은 쪽). 없으면 None."""
    if n == 0:
        return []
    first = next((i for i, c in enumerate(f) if c % mod), None)
    if first is None or first >= n:
        return [0] * n
    if first % 2:
        return None
    root = mod_sqrt(f[first], mod)
    if root is None:
        return None
    shifted = list(f[first:])
    length = n - first // 2
    g = [root]
    size = 1
    half = pow(2, mod - 2, mod)
    shifted += [0] * max(0, length - len(shifted))
    while size < length:
        size *= 2
        inverse_g = poly_inverse(g, size, mod)
        correction = multiply(shifted[:size], inverse_g, mod)[:size]
        padded_g = g + [0] * (size - len(g))
        g = [(padded_g[i] + (correction[i] if i < len(correction) else 0)) * half % mod for i in range(size)]
    return [0] * (first // 2) + g[:length]


def poly_divmod(a: Sequence[int], b: Sequence[int], mod: int = MOD) -> tuple[list[int], list[int]]:
    """a = b·q + r (deg r < deg b) 인 (q, r). b 는 0 이 아니어야 한다."""
    a = _trim([c % mod for c in a])
    b = _trim([c % mod for c in b])
    if not b:
        raise ValueError("0 으로 나눌 수 없습니다")
    if len(a) < len(b):
        return [], a
    count = len(a) - len(b) + 1
    inverse = poly_inverse(b[::-1], count, mod)
    quotient = multiply(a[::-1][:count], inverse, mod)[:count][::-1]
    product = multiply(b, quotient, mod)
    remainder = [(a[i] - (product[i] if i < len(product) else 0)) % mod for i in range(len(b) - 1)]
    return quotient, _trim(remainder)


class _Node:
    __slots__ = ("poly", "left", "right", "lo", "hi")

    def __init__(self, poly, left, right, lo, hi):
        self.poly, self.left, self.right, self.lo, self.hi = poly, left, right, lo, hi


def _product_tree(xs: Sequence[int], lo: int, hi: int, mod: int) -> _Node:
    """xs[lo:hi] 에 대한 ∏(x - x_i) 의 부분곱 트리."""
    if hi - lo == 1:
        return _Node([(-xs[lo]) % mod, 1], None, None, lo, hi)
    mid = (lo + hi) // 2
    left, right = _product_tree(xs, lo, mid, mod), _product_tree(xs, mid, hi, mod)
    return _Node(multiply(left.poly, right.poly, mod), left, right, lo, hi)


def _horner(f: Sequence[int], x: int, mod: int) -> int:
    value = 0
    for c in reversed(f):
        value = (value * x + c) % mod
    return value


def multipoint_evaluate(f: Sequence[int], xs: Sequence[int], mod: int = MOD) -> list[int]:
    """f(x_i) 를 모든 i 에 대해 (O(n log² n))."""
    if not xs:
        return []
    f = _trim([c % mod for c in f])
    result = [0] * len(xs)

    def descend(node: _Node, poly: list[int]) -> None:
        if node.hi - node.lo <= 16:
            for i in range(node.lo, node.hi):
                result[i] = _horner(poly, xs[i], mod)
            return
        for child in (node.left, node.right):
            descend(child, poly_divmod(poly, child.poly, mod)[1])

    root = _product_tree(xs, 0, len(xs), mod)
    descend(root, poly_divmod(f, root.poly, mod)[1])
    return result


def interpolate(xs: Sequence[int], ys: Sequence[int], mod: int = MOD) -> list[int]:
    """(x_i, y_i) 를 모두 지나는 차수 < n 의 다항식 (x_i 는 서로 달라야 한다)."""
    if len(xs) != len(ys):
        raise ValueError("xs 와 ys 의 길이가 다릅니다")
    xs = [x % mod for x in xs]
    if len(set(xs)) != len(xs):
        raise ValueError("x 좌표가 서로 달라야 합니다")
    if not xs:
        return []
    root = _product_tree(xs, 0, len(xs), mod)
    slopes = multipoint_evaluate(poly_derivative(root.poly, mod), xs, mod)
    weights = [y % mod * pow(s, mod - 2, mod) % mod for y, s in zip(ys, slopes)]

    def combine(node: _Node) -> list[int]:
        if node.hi - node.lo == 1:
            return [weights[node.lo]]
        left, right = combine(node.left), combine(node.right)
        a, b = multiply(left, node.right.poly, mod), multiply(right, node.left.poly, mod)
        size = max(len(a), len(b))
        return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % mod for i in range(size)]

    return _trim(combine(root))


def taylor_shift(f: Sequence[int], c: int, mod: int = MOD) -> list[int]:
    """g(x) = f(x + c) 의 계수."""
    n = len(f)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % mod
    a = [f[i] % mod * fact[i] % mod for i in range(n)][::-1]  # a[n-1-i] = f_i · i!
    powers = [1] * n
    for k in range(1, n):
        powers[k] = powers[k - 1] * (c % mod) % mod
    b = [powers[k] * inv_fact[k] % mod for k in range(n)]
    product = multiply(a, b, mod)  # 곱의 n-1-j 번 칸 = Σ_i f_i i! · c^{i-j}/(i-j)!
    return [product[n - 1 - j] * inv_fact[j] % mod for j in range(n)]


def bell_numbers(n: int, mod: int = MOD) -> list[int]:
    """B_0 … B_{n-1} (mod): 지수 생성함수 exp(e^x - 1) 의 계수에 k! 를 곱한다."""
    if n == 0:
        return []
    fact = [1] * n
    for i in range(1, n):
        fact[i] = fact[i - 1] * i % mod
    inv_fact = [pow(fact[-1], mod - 2, mod)]
    for i in range(n - 1, 0, -1):
        inv_fact.append(inv_fact[-1] * i % mod)
    inv_fact.reverse()
    exponent = [0] + inv_fact[1:]
    series = poly_exp(exponent, n, mod)
    return [series[i] * fact[i] % mod for i in range(n)]


def partition_numbers(n: int, mod: int = MOD) -> list[int]:
    """p(0) … p(n-1) (mod): 1 / ∏(1 - x^k), 분모는 오일러의 오각수 정리 Σ (-1)^k x^{k(3k-1)/2}."""
    if n == 0:
        return []
    pentagonal = [0] * n
    k = 0
    while True:
        done = True
        for kk in ((k, -k) if k else (0,)):
            index = kk * (3 * kk - 1) // 2
            if index < n:
                pentagonal[index] = (pentagonal[index] + (-1) ** (abs(kk) % 2)) % mod
                done = False
        if done:
            break
        k += 1
    return poly_inverse(pentagonal, n, mod)


def catalan_numbers(n: int, mod: int = MOD) -> list[int]:
    """C_0 … C_{n-1} (mod): sqrt(1 - 4x) = 1 - 2 Σ C_k x^{k+1}."""
    if n == 0:
        return []
    root = poly_sqrt([1, (-4) % mod], n + 1, mod)
    half = pow(2, mod - 2, mod)
    return [(-root[k + 1]) * half % mod for k in range(n)]


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    print(" ".join(map(str, poly_exp([int(x) for x in data[1:1 + n]], n))))


if __name__ == "__main__":
    main()
