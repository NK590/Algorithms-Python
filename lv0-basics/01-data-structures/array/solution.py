"""배열 — 연속된 칸에 원소를 순서대로 저장하는 자료구조 (파이썬에서는 list)

README.md 의 설명과 짝을 이루는 참고 구현입니다.
배열의 연산이 왜 그만한 비용이 드는지 보여 주려고 삽입·삭제·뒤집기·회전을 직접 구현했습니다.
실전에서는 내장 연산(list.insert, list.pop, 슬라이싱, min/max)을 쓰세요.

직접 실행하면 첫 줄에 N, 둘째 줄에 N개의 정수를 받아 최솟값과 최댓값을 한 줄에 출력합니다.
"""
import sys


def insert_at(arr: list, index: int, value) -> None:
    """arr[index] 자리에 value 를 끼워 넣는다. 뒤쪽 원소를 한 칸씩 밀어야 하므로 O(n)."""
    if not 0 <= index <= len(arr):
        raise IndexError("index 가 범위를 벗어났습니다")
    arr.append(value)  # 한 칸 늘린다 (이 값은 아래에서 덮어쓴다)
    for i in range(len(arr) - 1, index, -1):  # 뒤에서부터 밀어야 아직 안 옮긴 값을 덮어쓰지 않는다
        arr[i] = arr[i - 1]
    arr[index] = value


def delete_at(arr: list, index: int):
    """arr[index] 를 지우고 그 값을 반환한다. 뒤쪽 원소를 한 칸씩 당겨야 하므로 O(n)."""
    if not 0 <= index < len(arr):
        raise IndexError("index 가 범위를 벗어났습니다")
    value = arr[index]
    for i in range(index, len(arr) - 1):
        arr[i] = arr[i + 1]
    arr.pop()  # 맨 뒤의 남는 칸을 지운다
    return value


def reverse_in_place(arr: list, left: int = 0, right: int | None = None) -> None:
    """arr[left..right] 구간을 제자리에서 뒤집는다. right 를 생략하면 끝까지."""
    if right is None:
        right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


def rotate_left(arr: list, k: int) -> None:
    """arr 를 왼쪽으로 k칸 돌린다. [앞 k개 뒤집기] → [나머지 뒤집기] → [전체 뒤집기] 로 추가 메모리 없이 O(n)."""
    n = len(arr)
    if n == 0:
        return
    k %= n
    reverse_in_place(arr, 0, k - 1)
    reverse_in_place(arr, k, n - 1)
    reverse_in_place(arr)


def max_with_index(arr: list) -> tuple:
    """(최댓값, 그 값이 처음 나오는 인덱스) 를 반환한다. 모든 칸을 한 번씩 봐야 하므로 O(n)."""
    if not arr:
        raise ValueError("빈 배열입니다")
    best = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[best]:  # 엄격하게 클 때만 갱신해야 가장 앞의 인덱스가 남는다
            best = i
    return arr[best], best


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))[:n]
    print(min(arr), max_with_index(arr)[0])


if __name__ == "__main__":
    main()
