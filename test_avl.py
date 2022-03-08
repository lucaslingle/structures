import pytest

from avl import AVL


def test_check_ri():
    # child node violates bst property -> should throw runtime error.
    avl = AVL(parent=None, key=0)
    avl.left = AVL(parent=avl, key=1)
    avl.height = 1
    avl.left.height = 0
    with pytest.raises(RuntimeError):
        avl.check_ri()

    avl = AVL(parent=None, key=0)
    avl.right = AVL(parent=avl, key=-1)
    avl.height = 1
    avl.right.height = 0
    with pytest.raises(RuntimeError):
        avl.check_ri()

    # child node has no parent -> should throw runtime error.
    avl = AVL(parent=None, key=0)
    avl.left = AVL(parent=None, key=-1)
    avl.height = 1
    avl.left.height = 0
    with pytest.raises(RuntimeError):
        avl.check_ri()

    avl = AVL(parent=None, key=0)
    avl.right = AVL(parent=None, key=1)
    avl.height = 1
    avl.right.height = 0
    with pytest.raises(RuntimeError):
        avl.check_ri()

    # left and right subtree heights differ by two or more ->
    #     should throw runtime error.
    avl = AVL(parent=None, key=0)
    avl.left = AVL(parent=avl, key=-1)
    avl.left.left = AVL(parent=avl.left, key=-2)
    avl.height = 2
    avl.left.height = 1
    avl.left.left.height = 0
    with pytest.raises(RuntimeError):
        avl.check_ri()

    avl = AVL(parent=None, key=0)
    avl.right = AVL(parent=avl, key=1)
    avl.right.right = AVL(parent=avl.right, key=2)
    avl.height = 2
    avl.right.height = 1
    avl.right.right.height = 0
    with pytest.raises(RuntimeError):
        avl.check_ri()


def test_avl_balance():
    avl = AVL(parent=None, key=0)
    avl.left = AVL(parent=avl, key=-1)
    avl.right = AVL(parent=avl, key=1)
    avl.right.right = AVL(parent=avl.right, key=2)
    avl.right.right.height = 0
    avl.right.height = 1
    avl.left.height = 0
    avl.height = 2
    assert avl.balance == 1
    assert avl.left.balance == 0
    assert avl.right.balance == 1
    assert avl.right.right.balance == 0


def test_avl_insert():
    # test constructor
    avl = AVL(parent=None, key=0)
    #        0
    assert avl.height == 0
    assert avl.key == 0
    assert avl.left is None
    assert avl.right is None

    # test leaf insert left
    avl = avl.insert(-1, check_ri=True)
    #         0
    #   -1
    assert avl.height == 1
    assert avl.key == 0
    assert avl.left.key == -1
    assert avl.left.parent == avl
    assert avl.right is None

    # test leaf insert right
    avl = avl.insert(1, check_ri=True)
    #         0
    #    -1       1
    assert avl.height == 1
    assert avl.key == 0
    assert avl.left.key == -1
    assert avl.left.parent == avl
    assert avl.right.key == 1
    assert avl.right.parent == avl

    # test rebalance for straight left heavy at root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.insert(-2, check_ri=True)
    #          -1
    #     -2       0
    assert avl.height == 1
    assert avl.key == -1
    assert avl.left.key == -2
    assert avl.right.key == 0

    # test rebalance for straight right heavy at root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    avl = avl.insert(2, check_ri=True)
    #         1
    #     0       2
    assert avl.height == 1
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2

    # test rebalance for zig-zag left heavy at root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.insert(-0.5, check_ri=True)
    #          -0.5
    #     -1          0
    assert avl.height == 1
    assert avl.key == -0.5
    assert avl.left.key == -1
    assert avl.right.key == 0

    # test rebalance for zig-zag right heavy at root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    avl = avl.insert(0.5, check_ri=True)
    #         0.5
    #     0        1
    assert avl.height == 1
    assert avl.key == 0.5
    assert avl.left.key == 0
    assert avl.right.key == 1

    # test rebalance for straight left heavy at non-root node
    avl = AVL(parent=None, key=-1)
    avl = avl.insert(0, check_ri=True)
    avl = avl.insert(-2, check_ri=True)
    avl = avl.insert(-3, check_ri=True)
    avl = avl.insert(-4, check_ri=True)
    #          -1
    #     -3       0
    # -4    -2
    assert avl.height == 2
    assert avl.key == -1
    assert avl.right.key == 0
    assert avl.left.key == -3
    assert avl.left.right.key == -2
    assert avl.left.left.key == -4

    # test rebalance for straight right heavy at non-root node
    avl = AVL(parent=None, key=1)
    avl = avl.insert(0, check_ri=True)
    avl = avl.insert(2, check_ri=True)
    avl = avl.insert(3, check_ri=True)
    avl = avl.insert(4, check_ri=True)
    #         1
    #     0       3
    #           2    4
    assert avl.height == 2
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 3
    assert avl.right.left.key == 2
    assert avl.right.right.key == 4

    # test rebalance for zig-zag left heavy at non-root node
    avl = AVL(parent=None, key=-1)
    avl = avl.insert(0, check_ri=True)
    avl = avl.insert(-2, check_ri=True)
    avl = avl.insert(-3, check_ri=True)
    avl = avl.insert(-2.5, check_ri=True)
    #           -1
    #     -2.5      0
    #   -3   -2
    assert avl.height == 2
    assert avl.key == -1
    assert avl.right.key == 0
    assert avl.left.key == -2.5
    assert avl.left.right.key == -2
    assert avl.left.left.key == -3

    # test rebalance for zig-zag right heavy at non-root node
    avl = AVL(parent=None, key=1)
    avl = avl.insert(0, check_ri=True)
    avl = avl.insert(2, check_ri=True)
    avl = avl.insert(3, check_ri=True)
    avl = avl.insert(2.5, check_ri=True)
    #         1
    #     0       2.5
    #           2     3
    assert avl.height == 2
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2.5
    assert avl.right.left.key == 2
    assert avl.right.right.key == 3


def test_avl_delete():
    # test root delete singleton
    avl = AVL(parent=None, key=0)
    avl = avl.delete(0)
    assert avl is None

    # test root delete with subtrees
    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    avl = avl.delete(0)
    assert avl.height == 0
    assert avl.key == 1
    assert avl.parent is None
    assert avl.left is None
    assert avl.right is None

    # test leaf delete left
    avl = AVL(parent=None, key=0)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.delete(-1)
    assert avl.height == 0
    assert avl.key == 0
    assert avl.left is None
    assert avl.right is None

    # test leaf delete right
    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    avl = avl.delete(1)
    assert avl.height == 0
    assert avl.key == 0
    assert avl.left is None
    assert avl.right is None

    # test rebalance for straight left heavy root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.insert(-2, check_ri=True)
    avl = avl.delete(1)
    #         -1
    #     0        -2
    assert avl.height == 1
    assert avl.key == -1
    assert avl.right.key == 0
    assert avl.left.key == -2

    # test rebalance for straight right heavy root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.insert(1, check_ri=True)
    avl = avl.insert(2, check_ri=True)
    avl = avl.delete(-1)
    #         1
    #     0       2
    assert avl.height == 1
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2

    # test rebalance for zig-zag left heavy root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.insert(-0.5, check_ri=True)
    avl = avl.delete(1)
    #         -0.5
    #     -1         0
    assert avl.height == 1
    assert avl.key == -0.5
    assert avl.right.key == 0
    assert avl.left.key == -1

    # test rebalance for zig-zag right heavy root
    avl = AVL(parent=None, key=0)
    avl = avl.insert(-1, check_ri=True)
    avl = avl.insert(1, check_ri=True)
    avl = avl.insert(0.5, check_ri=True)
    avl = avl.delete(-1)
    #         0.5
    #     0        1
    assert avl.height == 1
    assert avl.key == 0.5
    assert avl.left.key == 0
    assert avl.right.key == 1


if __name__ == '__main__':
    #test_avl_insert()
    test_avl_delete()
