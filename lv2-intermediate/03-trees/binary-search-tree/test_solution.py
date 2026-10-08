"""solution.py 검증: 정렬된 리스트(bisect)를 기준 모델로 랜덤 연산 비교 + 구조 불변식 점검"""
import bisect
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def check_structure(tree):
    """BST 성질(모든 노드에서 왼쪽 < 키 < 오른쪽)과 size 가 모두 맞는가"""
    def walk(node, low, high):
        if node is None:
            return 0
        assert (low is None or node.key > low) and (high is None or node.key < high), node.key
        left = walk(node.left, low, node.key)
        right = walk(node.right, node.key, high)
        assert node.size == left + right + 1, ("size", node.key)
        return node.size

    walk(tree.root, None, None)


def test_matches_sorted_list_model():
    rng = random.Random(0)
    for _ in range(150):
        tree, model = solution.BST(), []
        for _ in range(rng.randint(0, 60)):
            key = rng.randint(0, 25)
            if rng.random() < 0.6:
                inserted = tree.insert(key)
                assert inserted == (key not in model)
                if inserted:
                    bisect.insort(model, key)
            else:
                deleted = tree.delete(key)
                assert deleted == (key in model)
                if deleted:
                    model.remove(key)
            check_structure(tree)
            assert tree.inorder() == model
            assert len(tree) == len(model)
        for x in range(-2, 28):
            assert (x in tree) == (x in model)
            i = bisect.bisect_left(model, x)
            assert tree.rank(x) == i
            assert tree.ceil(x) == (model[i] if i < len(model) else None)
            j = bisect.bisect_right(model, x)
            assert tree.floor(x) == (model[j - 1] if j > 0 else None)
            assert tree.successor(x) == (model[j] if j < len(model) else None)
        assert tree.minimum() == (model[0] if model else None)
        assert tree.maximum() == (model[-1] if model else None)
        for k in range(0, len(model) + 2):
            assert tree.kth_smallest(k) == (model[k - 1] if 1 <= k <= len(model) else None)


def test_delete_all_three_cases():
    tree = solution.BST()
    for key in [50, 30, 70, 20, 40, 60, 80, 35, 45]:
        tree.insert(key)
    assert tree.delete(20)  # ① 잎 (자식이 없다)
    assert tree.inorder() == [30, 35, 40, 45, 50, 60, 70, 80]
    assert tree.delete(30) and tree.root.left.key == 40  # ② 자식이 하나(오른쪽 40): 그 자식으로 대체
    check_structure(tree)
    assert tree.delete(50)  # ③ 루트이면서 자식이 둘: 오른쪽 서브트리의 최솟값(60)의 키를 가져온다
    assert tree.root.key == 60
    check_structure(tree)
    assert tree.inorder() == [35, 40, 45, 60, 70, 80]
    assert not tree.delete(999)
    while len(tree):
        assert tree.delete(tree.minimum())
    assert tree.root is None and tree.inorder() == [] and tree.height() == 0


def test_empty_tree_and_duplicates():
    tree = solution.BST()
    assert len(tree) == 0 and tree.minimum() is None and tree.floor(3) is None and 3 not in tree
    assert tree.insert(5) is True and tree.insert(5) is False and len(tree) == 1


def test_sorted_inserts_make_a_chain_but_do_not_recurse():
    tree = solution.BST()
    n = 2000
    for key in range(n):
        tree.insert(key)
    assert tree.height() == n  # 사슬
    assert tree.kth_smallest(n) == n - 1 and tree.rank(n - 1) == n - 1
    assert tree.inorder() == list(range(n))
    while len(tree):
        tree.delete(tree.maximum())
    assert len(tree) == 0


def test_build_balanced_has_logarithmic_height():
    for n in [0, 1, 2, 3, 7, 8, 100, 1000]:
        tree = solution.build_balanced(list(range(n)))
        check_structure(tree)
        assert tree.inorder() == list(range(n))
        assert tree.height() == (math.ceil(math.log2(n + 1)) if n else 0)


def postorder_by_recursion(preorder):
    if not preorder:
        return []
    root, rest = preorder[0], preorder[1:]
    left = [x for x in rest if x < root]
    right = [x for x in rest if x > root]
    return postorder_by_recursion(left) + postorder_by_recursion(right) + [root]


def test_postorder_from_preorder_matches_recursive_definition():
    rng = random.Random(1)
    for _ in range(500):
        keys = rng.sample(range(100), rng.randint(0, 15))
        tree = solution.BST()
        for k in keys:
            tree.insert(k)
        # keys 를 넣은 순서가 곧 전위 순회가 되도록 BST 를 다시 전위 순회로 뽑는다
        preorder, stack = [], [tree.root] if tree.root else []
        while stack:
            node = stack.pop()
            preorder.append(node.key)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        assert solution.postorder_from_preorder(preorder) == postorder_by_recursion(preorder)
    assert solution.postorder_from_preorder([]) == []
    assert solution.postorder_from_preorder([5, 3, 4, 8]) == [4, 3, 8, 5]


def test_postorder_from_preorder_long_chain():
    n = 20000
    assert solution.postorder_from_preorder(list(range(n))) == list(range(n - 1, -1, -1))
    assert solution.postorder_from_preorder(list(range(n, 0, -1))) == list(range(1, n + 1))


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("50\n30\n24\n5\n28\n45\n98\n52\n60\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["5", "28", "24", "45", "30", "60", "52", "98", "50"]
