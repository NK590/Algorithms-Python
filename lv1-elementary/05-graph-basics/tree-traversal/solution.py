### Tree Traversal (트리 순회)

# 트리 자료구조에서 각 노드를 한 번만 방문하는 방법
# 일반적으로 이진 노드를 기준으로 정의하지만, 일반적인 트리에서도 똑같이 적용 가능
# 수많은 탐색 방법이 있지만, 여기서는 전위, 중위, 후위 순회 세 가지를 작성함
# 자식 노드를 기점으로 하는 서브트리도 트리의 성질을 재귀적으로 가지고 있다는 점에 착안하면,
# 모든 순회 방법을 재귀를 통해 손쉽게 구현 가능

# 전위 순회(Preoder Traversal)
# 노드 -> 왼쪽 서브트리 -> 오른쪽 서브트리 순으로 방문

# 중위 순회(Inorder Traversal)
# 왼쪽 서브트리 -> 노드 -> 오른쪽 서브트리 순으로 방문

# 후위 순회(Postorder Traversal)
# 왼쪽 서브트리 -> 오른쪽 서브트리 -> 노드 순으로 방문

### 예시 코드

# key 값이 노드, value 리스트의 원소는 각각 왼쪽 자식, 오른쪽 자식을 나타냄
# value 값이 '.'인 경우는 값이 없음을 뜻함
tree = {
    'A' : ['B', 'C'],
    'B' : ['D', '.'],
    'C' : ['E', 'F'],
    'D' : ['.', '.'],
    'E' : ['.', '.'],
    'F' : ['.', 'G'],
    'G' : ['.', '.']
}

# 전위 순회
def preorder(root):
    if root != '.':
        visited.append(root)
        preorder(tree[root][0])
        preorder(tree[root][1])

# 중위 순회
def inorder(root):
    if root != '.':
        inorder(tree[root][0])
        visited.append(root)
        inorder(tree[root][1])

# 후위 순회
def postorder(root):
    if root != '.':
        postorder(tree[root][0])
        postorder(tree[root][1])
        visited.append(root)

# 각각 순회 시 방문하는 순서를 출력
visited = []
preorder('A')
print(*visited, sep = '')

visited = []
inorder('A')
print(*visited, sep = '')

visited = []
postorder('A')
print(*visited, sep = '')