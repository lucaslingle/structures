import pytest

from bst import BST


def test_check_ri():
    # child node violates bst property -> should throw runtime error.
    bst = BST(parent=None, key=0)
    bst.left = BST(parent=bst, key=1)
    with pytest.raises(RuntimeError):
        bst.check_ri()
    bst = BST(parent=None, key=0)
    bst.right = BST(parent=bst, key=-1)
    with pytest.raises(RuntimeError):
        bst.check_ri()

    # child node has no parent -> should throw runtime error.
    bst = BST(parent=None, key=0)
    bst.left = BST(parent=None, key=-1)
    with pytest.raises(RuntimeError):
        bst.check_ri()
    bst = BST(parent=None, key=0)
    bst.right = BST(parent=None, key=1)
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
    bst = BST(parent=None, key=0)
    assert bst.height == 0
    assert bst.key == 0
    assert bst.left is None
    assert bst.right is None
    bst.insert(1, check_ri=True)
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.parent == bst
    bst.insert(-1, check_ri=True)
    assert bst.height == 1
    assert bst.key == 0
    assert bst.left.key == -1
    assert bst.left.parent == bst
    assert bst.right.key == 1
    assert bst.right.parent == bst

    bst = BST(parent=None, key=0)
    bst.insert(1, check_ri=True)
    bst.insert(-1, check_ri=True)
    bst.insert(2, check_ri=True)
    bst.insert(-2, check_ri=True)
    bst.insert(3, check_ri=True)
    bst.insert(-0.5, check_ri=True)
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


def test_bst_delete():
    bst = BST(parent=None, key=0)
    bst.insert(1, check_ri=True)
    bst.insert(-1, check_ri=True)
    bst.delete(-1, check_ri=True)
    assert bst.left is None
    assert bst.right.key == 1
    assert bst.right.parent == bst

    bst = BST(parent=None, key=0)
    bst.insert(1, check_ri=True)
    bst.insert(-1, check_ri=True)
    bst.insert(2, check_ri=True)
    bst.insert(-2, check_ri=True)
    bst.insert(3, check_ri=True)
    bst.insert(-0.5, check_ri=True)
    #         0
    #    -1      1
    # -2  -0.5       2
    #                   3

    bst.delete(1, check_ri=True)
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

    bst.delete(-1, check_ri=True)
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

    bst.delete(3, check_ri=True)
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
