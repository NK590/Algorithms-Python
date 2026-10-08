### Insertion Sort (삽입 정렬)

# k번째 원소를 1 ~ k-1번째 원소와 비교해서 정렬 순서에 맞는 적절한 위치에 끼위넣는 알고리즘
# 시간복잡도는 O(n^2)이나, n이 작을 떄는 매우 좋은 퍼포먼스를 보여줌
# 단, 자료 구조에 따라 원소를 끼워넣는 과정에서 다른 원소를 밀어내는 데 많은 시간이 걸릴 수 있음

### 예시 코드

def Insertion_Sort(li: list):
    n = len(li)
    for i in range(1, n):
        # i부터 0까지 거꾸로 비교해나감
        for j in range(i, 0, -1):
            if li[j - 1] > li[j]:
                li[j - 1], li[j] = li[j], li[j - 1]
    return li

### 예제

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
Insertion_Sort(li)
print("after :", li)