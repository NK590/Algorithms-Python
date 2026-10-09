"""FFT / NTT — 두 다항식(수열) 의 합성곱을 O(n²) 대신 O(n log n) 에 구하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 합성곱 c[k] = Σ_{i+j=k} a[i]·b[j]  (다항식의 곱). 계수 표현을 "점 값 표현" 으로 바꾸면 곱이 원소끼리의 곱이 되고, 변환은 분할 정복으로 O(n log n).
- ntt(a): 정수 mod p 위의 변환 (수치 오차가 없다). p = 998244353 = 119·2²³ + 1 은 2²³ 개의 1의 거듭제곱근을 가지고 원시근은 3.
  역변환은 근을 역원으로 바꾸고 n 으로 나눈다.
- convolution(a, b, mod): 결과를 mod 로 나눈 나머지로. NTT 에 맞는 소수가 아니면 서로 다른 세 소수로 구한 뒤 가르너(Garner) 방법으로 합친다.
- convolution_exact(a, b): 계수가 (음수여도) 정수일 때의 정확한 결과. 세 소수의 곱(≈ 7.8·10²⁵) 안에 결과 계수가 들어야 한다.
- fft_convolution(a, b): 복소수 부동소수점 FFT 로 구한 뒤 반올림 (계수가 작을 때만 정확).
- multiply_decimal_strings: 아주 긴 십진수의 곱 (자릿수를 계수로). max_cyclic_dot_product, count_pair_sums: 합성곱의 대표 응용.
- 직접 실행하면 큰 정수 곱 예제 형식 — 한 줄에 두 개의 자연수 — 를 받아 곱을 출력합니다 (NTT 로 구함).
"""
import cmath
import sys
from typing import Sequence

MOD = 998244353
ROOT = 3
PRIMES = ((998244353, 3), (167772161, 3), (469762049, 3))  # 모두 원시근 3, 2^23 이상의 길이를 지원
EXACT_LIMIT = PRIMES[0][0] * PRIMES[1][0] * PRIMES[2][0] // 2  # 세 소수로 정확히 복원할 수 있는 결과의 절댓값 상한 (≈ 3.9·10²⁵)


def _bit_reverse(a: list) -> None:
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]


def ntt(a: list[int], invert: bool = False, mod: int = MOD, root: int = ROOT) -> None:
    """제자리 NTT. len(a) 는 2 의 거듭제곱이어야 하고 mod - 1 이 그 길이로 나누어떨어져야 한다. invert=True 면 역변환."""
    n = len(a)
    if n & (n - 1):
        raise ValueError("길이는 2 의 거듭제곱이어야 합니다")
    if n > 1 and (mod - 1) % n:
        raise ValueError("이 소수는 이렇게 긴 변환을 지원하지 않습니다")
    _bit_reverse(a)
    length = 2
    while length <= n:
        w = pow(root, (mod - 1) // length, mod)
        if invert:
            w = pow(w, -1, mod)
        half = length >> 1
        twiddles = [1] * half
        for k in range(1, half):
            twiddles[k] = twiddles[k - 1] * w % mod
        for start in range(0, n, length):
            middle = start + half
            low = a[start:middle]
            high = [x * t % mod for x, t in zip(a[middle : start + length], twiddles)]
            a[start:middle] = [(x + y) % mod for x, y in zip(low, high)]
            a[middle : start + length] = [(x - y) % mod for x, y in zip(low, high)]
        length <<= 1
    if invert:
        n_inverse = pow(n, -1, mod)
        for i in range(n):
            a[i] = a[i] * n_inverse % mod


def _size_for(count: int) -> int:
    size = 1
    while size < count:
        size <<= 1
    return size


def _ntt_convolution(a: Sequence[int], b: Sequence[int], mod: int, root: int) -> list[int]:
    count = len(a) + len(b) - 1
    size = _size_for(count)
    fa = [x % mod for x in a] + [0] * (size - len(a))
    fb = [x % mod for x in b] + [0] * (size - len(b))
    ntt(fa, False, mod, root)
    ntt(fb, False, mod, root)
    product = [x * y % mod for x, y in zip(fa, fb)]
    ntt(product, True, mod, root)
    return product[:count]


def _naive_convolution(a: Sequence[int], b: Sequence[int], mod: int | None = None) -> list[int]:
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                result[i + j] += x * y
    return [v % mod for v in result] if mod is not None else result


def convolution_exact(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """정수 계수(음수 가능) 의 정확한 합성곱. 결과의 절댓값이 세 소수의 곱의 절반(≈ 3.9·10²⁵) 미만이어야 한다."""
    if not a or not b:
        return []
    if min(len(a), len(b)) <= 8:
        return _naive_convolution(a, b)
    residues = [_ntt_convolution(a, b, p, g) for p, g in PRIMES]
    (m1, _), (m2, _), (m3, _) = PRIMES
    m12 = m1 * m2
    inv_m1_mod_m2 = pow(m1, -1, m2)
    inv_m12_mod_m3 = pow(m12 % m3, -1, m3)
    total = m12 * m3
    result = []
    for r1, r2, r3 in zip(*residues):  # 가르너: x = x1 + m1·x2 + m1·m2·x3
        x1 = r1
        x2 = (r2 - x1) * inv_m1_mod_m2 % m2
        x3 = (r3 - x1 - m1 * x2) % m3 * inv_m12_mod_m3 % m3
        x = x1 + m1 * x2 + m12 * x3
        result.append(x - total if x > total // 2 else x)
    return result


def convolution(a: Sequence[int], b: Sequence[int], mod: int = MOD) -> list[int]:
    """합성곱을 mod 로 나눈 나머지로 (결과 길이 len(a) + len(b) - 1, 한쪽이 비면 [])."""
    if not a or not b:
        return []
    if min(len(a), len(b)) <= 8:
        return _naive_convolution(a, b, mod)
    if mod == MOD:
        return _ntt_convolution(a, b, MOD, ROOT)
    # 임의의 mod: 계수를 [0, mod) 로 줄이면 정확한 결과는 min(len)·mod² 이하 -> 세 소수로 충분한 범위에서 정확히 구한 뒤 mod
    reduced_a = [x % mod for x in a]
    reduced_b = [x % mod for x in b]
    if min(len(a), len(b)) * (mod - 1) ** 2 > EXACT_LIMIT:
        raise ValueError("mod 가 너무 커서 세 소수 방식으로 정확히 구할 수 없습니다")
    return [v % mod for v in convolution_exact(reduced_a, reduced_b)]


def fft(a: list[complex], invert: bool = False) -> None:
    """제자리 복소수 FFT. len(a) 는 2 의 거듭제곱."""
    n = len(a)
    if n & (n - 1):
        raise ValueError("길이는 2 의 거듭제곱이어야 합니다")
    _bit_reverse(a)
    length = 2
    while length <= n:
        angle = 2 * cmath.pi / length * (-1 if invert else 1)
        half = length >> 1
        twiddles = [cmath.exp(1j * angle * k) for k in range(half)]
        for start in range(0, n, length):
            middle = start + half
            low = a[start:middle]
            high = [x * t for x, t in zip(a[middle : start + length], twiddles)]
            a[start:middle] = [x + y for x, y in zip(low, high)]
            a[middle : start + length] = [x - y for x, y in zip(low, high)]
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n


def fft_convolution(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """부동소수점 FFT 로 구한 합성곱을 반올림. 결과 계수가 대략 10¹⁴ 이하일 때만 믿을 수 있다 (배정밀도의 한계)."""
    if not a or not b:
        return []
    count = len(a) + len(b) - 1
    size = _size_for(count)
    fa = [complex(x) for x in a] + [0j] * (size - len(a))
    fb = [complex(x) for x in b] + [0j] * (size - len(b))
    fft(fa)
    fft(fb)
    product = [x * y for x, y in zip(fa, fb)]
    fft(product, invert=True)
    return [round(v.real) for v in product[:count]]


def multiply_decimal_strings(x: str, y: str) -> str:
    """십진수 문자열 두 개의 곱 (자릿수를 계수로 하는 합성곱). 자릿수가 많아도 계수의 크기는 자릿수 × 81 이하."""
    if not x.isdigit() or not y.isdigit():
        raise ValueError("숫자로만 이루어진 문자열이어야 합니다")
    a = [int(ch) for ch in reversed(x)]
    b = [int(ch) for ch in reversed(y)]
    if min(len(a), len(b)) * 81 < MOD:
        coefficients = convolution(a, b, MOD)  # 정확한 계수가 MOD 보다 작으므로 나머지가 곧 값
    else:
        coefficients = convolution_exact(a, b)
    carry = 0
    digits = []
    for c in coefficients:
        carry += c
        digits.append(carry % 10)
        carry //= 10
    while carry:
        digits.append(carry % 10)
        carry //= 10
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return "".join(map(str, reversed(digits)))


def max_cyclic_dot_product(a: Sequence[int], b: Sequence[int]) -> int:
    """b 를 원형으로 s 칸 밀었을 때의 Σ a[i]·b[(i+s) mod n] 의 최댓값 (s = 0..n-1). 음수 계수도 된다."""
    n = len(a)
    if n != len(b) or n == 0:
        raise ValueError("두 수열의 길이는 같고 0 보다 커야 합니다")
    product = convolution_exact(list(reversed(a)), list(b) + list(b))
    return max(product[n - 1 + s] for s in range(n))


def count_pair_sums(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """a 에서 하나, b 에서 하나를 골라 합이 s 인 (순서 있는) 쌍의 수를 s = 0..max(a)+max(b) 에 대해. 값은 0 이상의 정수."""
    if not a or not b:
        return []
    if min(a) < 0 or min(b) < 0:
        raise ValueError("값은 0 이상이어야 합니다")
    ca = [0] * (max(a) + 1)
    cb = [0] * (max(b) + 1)
    for v in a:
        ca[v] += 1
    for v in b:
        cb[v] += 1
    return convolution_exact(ca, cb)


def main() -> None:
    x, y = sys.stdin.read().split()[:2]
    print(multiply_decimal_strings(x, y))


if __name__ == "__main__":
    main()
