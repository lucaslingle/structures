from avl import AVL


def make_avl():
    return AVL(parent=None, key=0)


def test_avl_insert():
    avl = make_avl()
    #        0
    assert avl.height == 0
    assert avl.key == 0
    assert avl.left is None
    assert avl.right is None
    node = AVL(parent=None, key=1)
    avl = avl.insert(node)
    #         0
    #             1
    assert avl.height == 1
    assert avl.key == 0
    assert avl.left is None
    assert avl.right.key == 1
    assert avl.right.parent == avl
    node2 = AVL(parent=None, key=-1)
    avl = avl.insert(node2)
    #         0
    #    -1      1
    assert avl.height == 1
    assert avl.key == 0
    assert avl.left is node2
    assert avl.left.key == -1
    assert avl.left.parent == avl
    assert avl.right.key == 1
    assert avl.right.parent == avl

    avl = make_avl()
    avl = avl.insert(AVL(parent=None, key=1))
    #         0
    #             1
    assert avl.height == 1
    avl = avl.insert(AVL(parent=None, key=2))
    #         1
    #     0       2
    assert avl.height == 1
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2
    avl = avl.insert(AVL(parent=None, key=3))
    #         1
    #     0       2
    #                3
    assert avl.height == 2
    assert avl.key == 1
    assert avl.left.key == 0
    assert avl.right.key == 2
    assert avl.right.right.key == 3
    avl = avl.insert(AVL(parent=None, key=4))
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
