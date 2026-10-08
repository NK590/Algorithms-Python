### Segment Tree (세그먼트 트리, 구간 트리)

# 트리의 특수한 케이스로, 각각의 노드가 특정 '구간값'을 보존하고 있는 이진 트리 자료구조
# 특정 구간의 구간값이 수시로 변경되며 임의의 구간값을 구해야 되는 쿼리에 유리하며,
# 특정 구간값의 갱신과 계산을 각각 시간복잡도 O(logn)으로 수행할 수 있음

### 예시 코드

# 각각의 노드는 특정 값을 가지고 있으며, 노드의 '구간값'은 그 합을 나타내는 경우

# 세그먼트 트리 리스트
# tree = [0 for _ in range(1 << (int(ceil(log2(n))) + 2))] 와 같이 적정 크기로 선언하는 것도 가능
tree = [0 for _ in range(100)]
# 각 노드별 입력값
entry = []

# 세그먼트 트리 생성
# 각 node가 담당하는 구간 == [start, end]
def init(node, start, end):
    # node가 leaf 노드인 경우 그 원소값을 반환
    # leaf 노드인 경우 리프 노드는 그 원소값을 가져야 하므로 tree[node] = entry[start]
    if start == end:
        tree[node] = entry[start]
        return tree[node]
    
    else:
        # 재귀적으로 왼쪽 자식 트리와 오른쪽 자식 트리를 만들고 저장
        tree[node] = init(2*node, start, (start+end)//2) + init(2*node+1, (start+end)//2+1, end)
        return tree[node]

# 구간 합 쿼리
# 각 node가 담당하는 구간 == [start, end]
# 합을 구해야 하는 구간 == [left, right]
def query_sum(node, start, end, left, right):
    # 겹치는 구간이 없을 때는 탐색 종료
    if left > end or right < start:
        return 0
    
    # 노드 구간이 합 구간 속에 포함되기 때문에 저장된 합을 바로 리턴
    if left <= start and end <= right:
        return tree[node]
    
    # 합 구간과 노드 구간이 일부분만 겹친 경우, 재귀적으로 위 두 케이스가 나올 때까지 탐색
    return query_sum(2*node, start, (start+end)//2, left, right) + query_sum(2*node+1, (start+end)//2+1, end, left, right)

# 갱신 쿼리
def query_update(node, start, end, index, diff):
    # 겹치는 구간이 없을 때는 탐색 종료
    if index < start or index > end:
        return
    
    tree[node] += diff
    
    # 리프 노드가 아닌 경우, 자식 노드값도 갱신해줘야 하기 때문에 재귀 호출로 구현
    if start != end:
        query_update(2*node, start, (start+end)//2, index, diff)
        query_update(2*node+1, (start+end)//2+1, end, index, diff)