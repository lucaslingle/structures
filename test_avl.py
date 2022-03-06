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
    avl.right = AVL(parent=None, key=1)
    avl.right.right = AVL(parent=None, key=2)
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
    avl = AVL(parent=None, key=0)
    #        0
    assert avl.height == 0
    assert avl.key == 0
    assert avl.left is None
    assert avl.right is None
    avl = avl.insert(1, check_ri=True)
    #         0
    #             1
    assert avl.height == 1
    assert avl.key == 0
    assert avl.left is None
    assert avl.right.key == 1
    assert avl.right.parent == avl
    avl = avl.insert(-1, check_ri=True)
    #         0
    #    -1      1
    assert avl.height == 1
    assert avl.key == 0
    assert avl.left.key == -1
    assert avl.left.parent == avl
    assert avl.right.key == 1
    assert avl.right.parent == avl

    avl = AVL(parent=None, key=0)
    avl = avl.insert(1, check_ri=True)
    #         0
    #             1
    assert avl.height == 1
    avl = avl.insert(2, check_ri=True)
    #         1
    #     0       2
    assert avl.height == 1
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2
    avl = avl.insert(3, check_ri=True)
    #         1
    #     0       2
    #                3
    assert avl.height == 2
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2
    assert avl.right.right.key == 3
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
    # todo: add tests for zig zag and zag zig, and for left mirror of everything


if __name__ == '__main__':
    test_avl_insert()
