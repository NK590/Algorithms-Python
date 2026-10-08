### Bubble Sort (버블 정렬)

# 인접한 두 수를 비교해 나가면서 정렬해 나가는 알고리즘.
# 두 수를 비교해서 앞 수가 뒤 수에 비해 큰 경우 둘의 위치를 바꿔가면서 큰 수를 뒤로 밀어냄
# 시간복잡도는 O(n^2)로 비교적 느린 편

### 예시 코드

def Bubble_Sort(li: list):
    n = len(li)
    for i in range(n - 1):
        # i 루프문이 한 번 돌 때마다 가장 큰 값을 하나씩 맨 뒤로 밀어내므로,
        # j 루프문은 그에 맞게 하나씩 줄여서 돌림
        for j in range(n - 1 - i):
            if li[j] > li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]
    return li

### 예제

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
Bubble_Sort(li)
print("after :", li)
