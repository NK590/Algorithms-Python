### Heap Sort (힙 정렬)

# 힙 트리(Heap Tree) 자료 구조를 이용한 정렬 방식으로, 주어진 리스트를 힙 트리 형태로 만든 뒤,
# 이를 바탕으로 원소를 정렬하는 방식. 시간복잡도는 O(nlogn)으로 퀵 정렬과 동일하나, 
# 실제로는 퀵 정렬이 빠른 경우가 많고 반면 힙 정렬은 비교적 편차가 적은 안정적인 성능을 보여줌
# 선택 정렬의 최적화 버전이라고도 볼 수 있음

### 예시 코드 1

def Heapify(li: list, index: int, len_li: int):
    left = index * 2
    right = index * 2 + 1
    largest = index
    
    # index 번째 노드의 각 자식들을 비교하면서 힙 순서에 맞게 largest를 갱신
    if left < len_li and li[left] > li[largest]:
        largest = left
    if right < len_li and li[right] > li[largest]:
        largest = right
    
    # 만약 largest 값과 초기 index 값이 불일치할 시 li 내 두 값을 스왑
    if largest != index:
        li[largest], li[index] = li[index], li[largest]
        # 위 과정까지 끝내면 국소적으로 힙 구조를 완성했으므로, 이를 자식에게 재귀적으로 수행
        Heapify(li, largest, len_li)
        
def Heap_Sort(li: list):
    len_li = len(li)
    
    # leaf 노드부터 밑에서부터 순차적으로 heapify 연산을 하여 입력 리스트를 min heap으로 만듬
    for i in range((len_li // 2) - 1, -1, -1):
        Heapify(li, i, len_li)
    
    # min heap에서 root 노드와 leaf 노드를 비교하면서 제일 작은 값을 앞으로 빼고, heapify로
    # min heap 구조를 유지함
    for i in range(len_li - 1, 0, -1):
        li[0], li[i] = li[i], li[0]
        Heapify(li, 0, i)
    
    return li

### 예시 코드 2
# 파이썬 내장 라이브러리인 heapq를 이용하면 다음과 같이 매우 간단하게 구현이 가능하다.

import heapq

def Heap_Sort_2(li: list):
    heapq.heapify(li)
    
    ans = []
    
    while li:
        ans.append(heapq.heappop(li))
    
    return ans

### 예제

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
Heap_Sort(li)
print("after :", li)

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
ans = Heap_Sort_2(li)
print("after :", ans)

