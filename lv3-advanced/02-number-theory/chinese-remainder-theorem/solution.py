"""중국인의 나머지 정리(Chinese Remainder Theorem) — 여러 합동식 x ≡ rᵢ (mod mᵢ) 를 하나로 합치기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 모듈러들이 서로소이면 해는 mod M = m₁·m₂·…·m_k 에서 유일하게 존재합니다.
- 서로소가 아니어도 두 식씩 합치면 됩니다: 해가 있는 조건은 rᵢ ≡ rⱼ (mod gcd(mᵢ, mⱼ)) 이고, 합친 모듈러는 lcm 입니다.
- 두 식을 합치는 핵심은 확장 유클리드 호제법입니다 (이 파일은 단독으로 실행되도록 extended_gcd 를 포함합니다).
- Garner 알고리즘은 큰 수 x 를 직접 만들지 않고 "x mod 임의의 수" 만 구합니다 (서로 다른 소수 모듈러로 얻은 결과를 합칠 때).
- 직접 실행하면 `T` 와 T 개의 테스트(`M N x y`)를 받아, 마지막 해가 <M:N> 인 달력에서 <x:y> 가 몇 번째 해인지 출력합니다(없으면 -1).
"""
import math
import sys


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """(g, x, y): g = gcd(a, b) ≥ 0, a·x + b·y = g."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def crt_pair(r1: int, m1: int, r2: int, m2: int):
    """x ≡ r1 (mod m1), x ≡ r2 (mod m2) 를 합친 (x, lcm(m1, m2)) (0 ≤ x < lcm). 해가 없으면 None.

    x = r1 + m1·t 로 두면 m1·t ≡ r2 − r1 (mod m2). g = gcd(m1, m2) 로 나누어 m1/g · t ≡ (r2 − r1)/g (mod m2/g) 를 풀고,
    m1/g 의 역원은 확장 유클리드가 준다 (m1·p + m2·q = g 이면 m1/g · p ≡ 1 (mod m2/g))."""
    g, p, _ = extended_gcd(m1, m2)
    if (r2 - r1) % g:
        return None
    lcm = m1 // g * m2
    t = (r2 - r1) // g * p % (m2 // g)
    return (r1 + m1 * t) % lcm, lcm


def crt(remainders: list[int], moduli: list[int]):
    """연립합동식 x ≡ remainders[i] (mod moduli[i]) 의 해 (x, L): 모든 해는 x + L·k. L 은 모듈러들의 lcm. 해가 없으면 None. moduli 는 모두 양수."""
    x, lcm = 0, 1
    for r, m in zip(remainders, moduli):
        merged = crt_pair(x, lcm, r % m, m)
        if merged is None:
            return None
        x, lcm = merged
    return x, lcm


def crt_coprime(remainders: list[int], moduli: list[int]) -> tuple[int, int]:
    """모듈러가 서로소일 때의 고전적인 공식: x = Σ rᵢ · Mᵢ · (Mᵢ⁻¹ mod mᵢ), Mᵢ = M / mᵢ. (x, M) 을 돌려준다."""
    total = math.prod(moduli)
    x = 0
    for r, m in zip(remainders, moduli):
        partial = total // m
        g, inverse, _ = extended_gcd(partial % m, m)
        if g != 1:
            raise ValueError("모듈러가 서로소가 아닙니다")
        x += r * partial * inverse
    return x % total, total


def garner(remainders: list[int], moduli: list[int], mod: int) -> int:
    """서로소인 moduli 에 대한 나머지 remainders 로 정해지는 수 x (0 ≤ x < Π moduli) 를 mod 로 나눈 나머지.

    x = c0 + c1·m0 + c2·m0·m1 + … (혼합 기수) 의 자릿수 cᵢ 를 앞에서부터 하나씩 정한다. O(k²)."""
    k = len(moduli)
    digits = [0] * k
    for i in range(k):
        m = moduli[i]
        accumulated, weight = 0, 1  # 지금까지 정한 자릿수가 m 에서 만드는 값과 가중치(m0·…·m_{i-1} mod m)
        for j in range(i):
            accumulated = (accumulated + digits[j] * weight) % m
            weight = weight * moduli[j] % m
        g, inverse, _ = extended_gcd(weight, m)
        if g != 1:
            raise ValueError("모듈러가 서로소가 아닙니다")
        digits[i] = (remainders[i] - accumulated) * inverse % m
    result, weight = 0, 1
    for i in range(k):
        result = (result + digits[i] * weight) % mod
        weight = weight * moduli[i] % mod
    return result


def calendar_year(m: int, n: int, x: int, y: int) -> int:
    """해마다 <x:y> 가 <x+1:y+1> 로 바뀌고 (x > m 이면 1, y > n 이면 1 로 돌아감) 첫 해가 <1:1> 일 때, <x:y> 는 몇 번째 해인가. 없으면 -1.

    year ≡ x (mod m), year ≡ y (mod n) 이고 1 ≤ year ≤ lcm(m, n). 합동식의 해가 0 이면 마지막 해 lcm 이다."""
    merged = crt_pair(x % m, m, y % n, n)
    if merged is None:
        return -1
    year, lcm = merged
    return year if year > 0 else lcm


def main() -> None:
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        m, n, x, y = map(int, data[1 + 4 * i : 5 + 4 * i])
        out.append(calendar_year(m, n, x, y))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
