"""빠른 입출력 — 입력이 많을 때 시간을 잡아먹지 않고 읽고 쓰기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 함수들은 `sys.stdin` 대신 입력 스트림(파일 객체)을 인자로 받아서 테스트할 수 있게 했습니다.
- 직접 실행하면 첫 줄에 T, 다음 T줄에 `A B` 를 받아 A+B 를 한 줄씩 출력합니다.
"""
import sys


def read_ints(stream) -> list:
    """스트림 전체를 한 번에 읽어 공백·줄바꿈 기준으로 쪼개 정수 리스트로 만든다. 입력이 아주 클 때 가장 빠른 방법."""
    return list(map(int, stream.read().split()))


def read_pairs_until_eof(stream) -> list:
    """입력이 끝날 때까지 줄마다 `A B` 를 읽는다. 테스트 케이스 수가 주어지지 않는 문제에 쓴다."""
    pairs = []
    for line in stream:  # 줄 단위로 읽다가 EOF 에서 자연스럽게 끝난다
        parts = line.split()
        if not parts:
            continue  # 끝에 붙은 빈 줄은 건너뛴다
        pairs.append((int(parts[0]), int(parts[1])))
    return pairs


def sum_each_test(stream) -> list:
    """첫 줄 T, 이후 T줄의 `A B` 에 대해 A+B 의 리스트를 반환한다. 줄마다 readline 으로 읽는 일반적인 형태."""
    readline = stream.readline
    t = int(readline())
    results = []
    for _ in range(t):
        a, b = map(int, readline().split())
        results.append(a + b)
    return results


def format_lines(values) -> str:
    """값을 줄 단위로 합친 하나의 문자열로 만든다. print 를 값마다 부르는 것보다 훨씬 빠르다."""
    return "\n".join(map(str, values))


def main() -> None:
    print(format_lines(sum_each_test(sys.stdin)))


if __name__ == "__main__":
    main()
