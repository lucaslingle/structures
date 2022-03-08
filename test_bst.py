import pytest

from bst import BST


def test_check_ri():
    # child node violates bst property -> should throw runtime error.
    bst = BST(parent=None, key=0)
    bst.left = BST(parent=bst, key=1)
    bst.height = 1
    bst.left.height = 0
    with pytest.raises(RuntimeError):
        bst.check_ri()

    bst = BST(parent=None, key=0)
    bst.right = BST(parent=bst, key=-1)
    bst.height = 1
    bst.right.height = 0
    with pytest.raises(RuntimeError):
        bst.check_ri()

    # child node has no parent -> should throw runtime error.
    bst = BST(parent=None, key=0)
    bst.left = BST(parent=None, key=-1)
    bst.height = 1
    bst.left.height = 0
    with pytest.raises(RuntimeError):
        bst.check_ri()

    bst = BST(parent=None, key=0)
    bst.right = BST(parent=None, key=1)
    bst.height = 1
    bst.right.height = 0
    with pytest.raises(RuntimeError):
        bst.check_ri()


def test_bst_search():
    bst = BST(parent=None, key=0)
    bst.left = BST(parent=bst, key=-1)
    bst.right = BST(parent=bst, key=1)
    result = bst.search(0)
    assert result == bst
    result = bst.search(-1)
    assert result == bst.left
    result = bst.search(1)
    assert result == bst.right


def test_bst_min():
    bst = BST(parent=None, key=0)
    bst.left = BST(parent=bst, key=-1)
    bst.right = BST(parent=bst, key=1)
    bst.right.left = BST(parent=bst, key=0.5)
    assert bst.min() == bst.left
    assert bst.left.min() == bst.left
    assert bst.right.min() == bst.right.left
    assert bst.right.left.min() == bst.right.left


def test_next_larger():
    # cover right simplest case
    bst = BST(parent=None, key=0)
    bst.right = BST(parent=bst, key=1)
    assert bst.next_larger(0).key == 1

    # cover right intermediate case
    bst = BST(parent=None, key=0)
    bst.right = BST(parent=bst, key=1)
    bst.right.left = BST(parent=bst.right, key=0.5)
    assert bst.next_larger(0).key == 0.5

    # cover backtrack case 1
    bst = BST(parent=None, key=3)
    bst.left = BST(parent=bst, key=2)
    bst.left.left = BST(parent=bst.left, key=1)
    assert bst.next_larger(1).key == 2

    # cover backtrack case 2
    bst = BST(parent=None, key=1)
    bst.left = BST(parent=bst, key=2)
    bst.left.left = BST(parent=bst.left, key=3)
    assert bst.next_larger(3) is None


def test_bst_insert():
    # test contructor
    bst = BST(parent=None, key=0)
    assert bst.height == 0
    assert bst.key == 0
    assert bst.left is None
    assert bst.right is None

    # test leaf insert left
    bst = BST(parent=None, key=0)
    bst = bst.insert(-1, check_ri=True)
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left.key == -1
    assert bst.left.parent == bst
    assert bst.right is None

    # test leaf insert right
    bst = BST(parent=None, key=0)
    bst = bst.insert(1, check_ri=True)
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.parent == bst

    # test make straight left unbalanced tree
    bst = BST(parent=None, key=0)
    bst = bst.insert(-1, check_ri=True)
    bst = bst.insert(-2, check_ri=True)
    assert bst.key == 0
    assert bst.height == 2
    assert bst.right is None
    assert bst.left.key == -1
    assert bst.left.height == 1
    assert bst.left.right is None
    assert bst.left.left.key == -2

    # test make straight right unbalanced tree
    bst = BST(parent=None, key=0)
    bst = bst.insert(1, check_ri=True)
    bst = bst.insert(2, check_ri=True)
    assert bst.key == 0
    assert bst.height == 2
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.height == 1
    assert bst.right.left is None
    assert bst.right.right.key == 2

    # test make zig-zag left unbalanced tree
    bst = BST(parent=None, key=0)
    bst = bst.insert(-1, check_ri=True)
    bst = bst.insert(-0.5, check_ri=True)
    assert bst.key == 0
    assert bst.height == 2
    assert bst.right is None
    assert bst.left.key == -1
    assert bst.left.height == 1
    assert bst.left.right.key == -0.5
    assert bst.left.left is None

    # test make zig-zag right unbalanced tree
    bst = BST(parent=None, key=0)
    bst = bst.insert(1, check_ri=True)
    bst = bst.insert(0.5, check_ri=True)
    assert bst.key == 0
    assert bst.height == 2
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.height == 1
    assert bst.right.left.key == 0.5
    assert bst.right.right is None


def test_bst_delete():
    # test delete root with zero children
    bst = BST(parent=None, key=0)
    bst = bst.delete(0, check_ri=True)
    assert bst is None

    # test delete root with nonzero children
    bst = BST(parent=None, key=0)
    bst = bst.insert(1, check_ri=True)
    bst = bst.insert(-1, check_ri=True)
    bst = bst.delete(0, check_ri=True)
    assert bst.key == 1
    assert bst.right is None
    assert bst.left.key == -1

    # test delete general node with zero children (left leaf)
    bst = BST(parent=None, key=0)
    bst = bst.insert(-1, check_ri=True)
    bst = bst.insert(1, check_ri=True)
    bst = bst.delete(-1, check_ri=True)
    assert bst.key == 0
    assert bst.left is None
    assert bst.right.key == 1

    # test delete general node with zero children (right leaf)
    bst = BST(parent=None, key=0)
    bst = bst.insert(-1, check_ri=True)
    bst = bst.insert(1, check_ri=True)
    bst = bst.delete(1, check_ri=True)
    assert bst.key == 0
    assert bst.right is None
    assert bst.left.key == -1

    # test delete general node with one child
    bst = BST(parent=None, key=0)
    bst = bst.insert(-1, check_ri=True)
    bst = bst.insert(1, check_ri=True)
    bst = bst.insert(-2, check_ri=True)
    bst = bst.insert(2, check_ri=True)
    bst = bst.insert(3, check_ri=True)
    bst = bst.insert(-0.5, check_ri=True)
    #         0
    #    -1      1
    # -2  -0.5       2
    #                   3
    bst = bst.delete(1, check_ri=True)
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

    # test delete general node with two children
    #          0
    #    -1        2
    # -2  -0.5         3
    bst = bst.delete(-1, check_ri=True)
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


if __name__ == '__main__':
    test_bst_insert()
    test_bst_search()
    test_bst_delete()
