"""비트 연산자 — 정수를 0 과 1 의 나열로 보고 &, |, ^, ~, <<, >> 로 다루기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 한 비트 읽기/켜기/끄기/뒤집기, 켜진 비트 세기, 2 의 거듭제곱 판별, 가장 낮은/높은 켜진 비트, XOR 의 성질.
- 파이썬의 정수는 크기 제한이 없고, 음수는 "앞이 무한히 1 로 채워진" 2 의 보수처럼 동작합니다. (~x == -x - 1)
- 직접 실행하면 두 수 `A B` 를 받아 A&B, A|B, A^B, ~A, A<<1, A>>1 을 한 줄씩 출력합니다.
"""
import sys


def get_bit(x: int, i: int) -> int:
    """x 의 i 번째 비트(0 번이 가장 낮은 자리)."""
    return (x >> i) & 1


def set_bit(x: int, i: int) -> int:
    """i 번째 비트를 1 로."""
    return x | (1 << i)


def clear_bit(x: int, i: int) -> int:
    """i 번째 비트를 0 으로. 1 << i 를 뒤집은 마스크(…1110111…)와 AND 한다."""
    return x & ~(1 << i)


def toggle_bit(x: int, i: int) -> int:
    """i 번째 비트를 뒤집는다."""
    return x ^ (1 << i)


def popcount(x: int) -> int:
    """켜진 비트의 수 (x ≥ 0). x & (x-1) 은 가장 낮은 켜진 비트 하나를 끄므로, 켜진 비트 수만큼만 반복한다."""
    count = 0
    while x:
        x &= x - 1
        count += 1
    return count


def is_power_of_two(x: int) -> bool:
    """2 의 거듭제곱인가. 켜진 비트가 정확히 하나면 x & (x-1) 이 0 이다."""
    return x > 0 and x & (x - 1) == 0


def lowest_set_bit(x: int) -> int:
    """가장 낮은 켜진 비트만 남긴 값 (x = 0 이면 0). -x 는 ~x + 1 이라 가장 낮은 켜진 비트까지만 x 와 같다."""
    return x & -x


def highest_set_bit(x: int) -> int:
    """가장 높은 켜진 비트만 남긴 값 (x ≤ 0 이면 0)."""
    return 1 << (x.bit_length() - 1) if x > 0 else 0


def xor_upto(n: int) -> int:
    """0 ^ 1 ^ 2 ^ … ^ n. 네 개씩 묶으면 0 이 되는 규칙이 있어 n % 4 로 O(1). n < 0 이면 0."""
    if n < 0:
        return 0
    return (n, 1, n + 1, 0)[n % 4]


def xor_range(lo: int, hi: int) -> int:
    """lo ^ (lo+1) ^ … ^ hi. 누적 XOR 두 개를 XOR 하면 겹친 앞부분이 사라진다."""
    return xor_upto(hi) ^ xor_upto(lo - 1)


def single_number(numbers: list) -> int:
    """모든 수가 두 번씩 나오고 하나만 한 번 나올 때 그 수. x ^ x = 0, x ^ 0 = x 이므로 모두 XOR 하면 남는다."""
    result = 0
    for x in numbers:
        result ^= x
    return result


def xor_swap(a: int, b: int) -> tuple:
    """임시 변수 없이 두 수 바꾸기 (원리 설명용. 파이썬에서는 a, b = b, a 가 더 낫다)."""
    a ^= b
    b ^= a
    a ^= b
    return a, b


def count_bits_table(n: int) -> list:
    """bits[i] = i 의 켜진 비트 수 (0 ≤ i ≤ n). i 에서 맨 아래 비트를 뺀 i >> 1 의 값을 재사용한다. DP O(n)."""
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits


def gray_code(n: int) -> list:
    """n 비트 그레이 코드. 이웃한 두 수는 정확히 한 비트만 다르다. i ^ (i >> 1)."""
    return [i ^ (i >> 1) for i in range(1 << n)]


def reverse_bits(x: int, width: int) -> int:
    """x 를 width 비트로 보고 비트 순서를 뒤집는다. 예: width=8 에서 0b00000110 → 0b01100000."""
    result = 0
    for _ in range(width):
        result = (result << 1) | (x & 1)
        x >>= 1
    return result


def to_binary(x: int, width: int) -> str:
    """width 비트의 이진 문자열. 음수는 2 의 보수(마스크로 아래 width 비트만 남김)로 보여 준다."""
    return format(x & ((1 << width) - 1), f"0{width}b")


def main() -> None:
    a, b = map(int, sys.stdin.readline().split())
    print(a & b)
    print(a | b)
    print(a ^ b)
    print(~a)
    print(a << 1)
    print(a >> 1)


if __name__ == "__main__":
    main()
