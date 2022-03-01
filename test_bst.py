from bst import BST


def make_bst():
    return BST(parent=None, key=0)


def test_bst_insert():
    bst = make_bst()
    assert bst.height == 0
    assert bst.key == 0
    assert bst.left is None
    assert bst.right is None
    node = BST(parent=None, key=1)
    bst.insert(node)
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.parent == bst
    node2 = BST(parent=None, key=-1)
    bst.insert(node2)
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left is node2
    assert bst.left.key == -1
    assert bst.left.parent == bst
    assert bst.right.key == 1
    assert bst.right.parent == bst

    bst = make_bst()
    bst.insert(BST(parent=None, key=1))
    bst.insert(BST(parent=None, key=-1))
    bst.insert(BST(parent=None, key=2))
    bst.insert(BST(parent=None, key=-2))
    bst.insert(BST(parent=None, key=3))
    bst.insert(BST(parent=None, key=-0.5))
    #         0
    #    -1      1
    # -2  -0.5       2
    #                   3
    assert bst.height == 3
    assert bst.key == 0
    assert bst.left.key == -1
    assert bst.right.key == 1
    assert bst.left.left.key == -2
    assert bst.left.right.key == -0.5
    assert bst.right.right.key == 2
    assert bst.right.right.right.key == 3


def test_bst_search():
    bst = make_bst()
    node = BST(parent=None, key=1)
    bst.insert(node)
    node2 = BST(parent=None, key=-1)
    bst.insert(node2)
    result = bst.search(0)
    assert result == bst
    result = bst.search(1)
    assert result == bst.right
    result = bst.search(-1)
    assert result == bst.left


def test_bst_delete():
    bst = make_bst()
    node = BST(parent=None, key=1)
    node2 = BST(parent=None, key=-1)
    bst.insert(node)
    bst.insert(node2)
    bst.delete(-1)
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.parent == bst

    bst = make_bst()
    bst.insert(BST(parent=None, key=1))
    bst.insert(BST(parent=None, key=-1))
    bst.insert(BST(parent=None, key=2))
    bst.insert(BST(parent=None, key=-2))
    bst.insert(BST(parent=None, key=3))
    bst.insert(BST(parent=None, key=-0.5))
    #         0
    #    -1      1
    # -2  -0.5       2
    #                   3

    bst.delete(1)
    #          0
    #    -1        2
    # -2  -0.5         3
    assert bst.height == 2
    assert bst.key == 0
    assert bst.left.height == 1
    assert bst.left.key == -1
    assert bst.right.height == 1
    assert bst.right.key == 2
    assert bst.left.left.height == 0
    assert bst.left.left.key == -2
    assert bst.left.right.height == 0
    assert bst.left.right.key == -0.5
    assert bst.right.left is None
    assert bst.right.right.height == 0
    assert bst.right.right.key == 3
    assert bst.left.left.left is None
    assert bst.left.left.right is None
    assert bst.left.right.left is None
    assert bst.left.right.right is None
    assert bst.right.right.left is None
    assert bst.right.right.right is None

    bst.delete(-1)
    #         0
    #   -0.5     2
    # -2            3
    assert bst.height == 2
    assert bst.key == 0
    assert bst.left.height == 1
    assert bst.left.key == -0.5
    assert bst.right.height == 1
    assert bst.right.key == 2
    assert bst.left.left.height == 0
    assert bst.left.left.key == -2
    assert bst.left.right is None
    assert bst.right.left is None
    assert bst.right.right.height == 0
    assert bst.right.right.key == 3
    assert bst.left.left.left is None
    assert bst.left.left.right is None
    assert bst.right.right.left is None
    assert bst.right.right.right is None

    bst.delete(-0.5)
    #         0
    #   -2       2
    #                3
    assert bst.height == 2
    assert bst.key == 0
    assert bst.left.height == 0
    assert bst.left.key == -2
    assert bst.right.height == 1
    assert bst.right.key == 2
    assert bst.left.left is None
    assert bst.left.right is None
    assert bst.right.left is None
    assert bst.right.right.height == 0
    assert bst.right.right.key == 3
    assert bst.right.right.left is None
    assert bst.right.right.right is None

    bst.delete(3)
    #         0
    #   -2       2
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left.height == 0
    assert bst.left.key == -2
    assert bst.right.height == 0
    assert bst.right.key == 2
    assert bst.left.left is None
    assert bst.left.right is None
    assert bst.right.left is None
    assert bst.right.right is None


if __name__ == '__main__':
    test_bst_insert()
    test_bst_search()
    test_bst_delete()
