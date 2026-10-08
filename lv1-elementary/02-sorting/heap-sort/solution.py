"""힙 정렬 — 최대 힙을 만든 뒤, 가장 큰 값을 맨 뒤로 보내는 일을 반복하는 정렬

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 입력 리스트를 제자리에서 오름차순으로 정렬합니다. (안정 정렬이 아님)
- 배열을 완전 이진 트리로 봅니다. 0번 시작 배열에서 i 번 원소의 자식은 2*i+1, 2*i+2 번입니다.
- 직접 실행하면 첫 줄에 N, 둘째 줄부터 N개의 정수를 받아 오름차순으로 한 줄에 하나씩 출력합니다.
"""
import sys


def _sift_down(arr: list, i: int, size: int) -> None:
    """arr[:size] 를 힙으로 볼 때, i 번 원소를 자식과 비교해 아래로 내려 보내 최대 힙 성질을 회복한다."""
    while True:
        child = 2 * i + 1
        if child >= size:  # 자식이 없으면 끝
            return
        if child + 1 < size and arr[child + 1] > arr[child]:  # 두 자식 중 더 큰 쪽을 고른다
            child += 1
        if arr[i] >= arr[child]:  # 부모가 자식보다 크면 이미 힙 성질을 만족한다
            return
        arr[i], arr[child] = arr[child], arr[i]
        i = child


def heap_sort(arr: list) -> None:
    """arr 을 제자리에서 오름차순으로 정렬한다."""
    n = len(arr)
    # 1단계: 마지막 부모부터 거슬러 올라가며 내려 보내면 전체가 최대 힙이 된다. (O(n))
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n)
    # 2단계: 루트(가장 큰 값)를 힙의 맨 뒤와 바꿔 확정하고, 줄어든 힙을 다시 정리한다.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end)


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = [int(input()) for _ in range(n)]
    heap_sort(arr)
    print("\n".join(map(str, arr)))


if __name__ == "__main__":
    main()
