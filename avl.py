"""
AVL Tree implementation.
"""

from bst import BST


class AVL(BST):
    def __init__(self, key, parent):
        super().__init__(key=key, parent=parent)

    def left_rotate(self):
        print('AVL.left_rotate')
        assert self.right is not None
        x = self
        y = self.right
        A = x.left
        B = y.left
        C = y.right
        x.left = A
        if A:
            A.parent = x
        x.right = B
        if B:
            B.parent = x
        x.height = 1 + max(
            x.left.height if x.left else -1,
            x.right.height if x.right else -1)
        y.left = x; x.parent = y
        y.right = C
        if C:
            C.parent = y
        y.height = 1 + max(
            y.left.height if y.left else -1,
            y.right.height if y.right else -1)
        return y

    def right_rotate(self):
        print('AVL.right_rotate')
        assert self.left is not None
        y = self
        x = self.left
        A = x.left
        B = x.right
        C = y.right
        y.left = B
        if B:
            B.parent = y
        y.right = C
        if C:
            C.parent = y
        y.height = 1 + max(
            y.left.height if y.left else -1,
            y.right.height if y.right else -1)
        x.left = A
        if A:
            A.parent = x
        x.right = y; y.parent = x
        x.height = 1 + max(
            x.left.height if x.left else -1,
            x.right.height if x.right else -1)
        return x

    def fix_right_heavy(self):
        print('AVL.fix_right_heavy')
        x = self
        xr_balance = (x.right.right.height if x.right.right else -1) \
            - (x.right.left.height if x.right.left else -1)
        if xr_balance >= 0:
            return x.left_rotate()
        else:
            z = x.right
            y = z.right_rotate()
            x.right = y
            return x.left_rotate()

    def fix_left_heavy(self):
        print('AVL.fix_left_heavy')
        # left heavy node x, deal by symmetry
        x = self
        xl_balance = (x.left.right.height if x.left.right else -1) \
            - (x.left.left.height if x.left.left else -1)
        if xl_balance <= 0:
            return x.right_rotate()
        else:
            z = x.left
            y = z.left_rotate()
            x.left = y
            return x.right_rotate()

    def fix_avl(self, node):
        print('AVL.fix_avl')
        while node:
            print(f'{node.key}')
            balance = (node.right.height if node.right else -1) \
                - (node.left.height if node.left else -1)
            print(f'\tbalance: {balance}')
            parent = node.parent
            if parent:
                go_right = parent.right == node
            if balance == 2:
                x = node
                y = x.fix_right_heavy()
                if parent:
                    if go_right:
                        parent.right = y
                    else:
                        parent.left = y
                    y.parent = parent
                    self.fix_heights(parent)
                else:
                    y.parent = None
                    return y
            if balance == -2:
                y = node
                x = y.fix_left_heavy()
                if parent:
                    if go_right:
                        parent.right = x
                    else:
                        parent.left = x
                    y.parent = parent
                    self.fix_heights(parent)
                else:
                    x.parent = None
                    return x
            if not parent:
                return node
            node = parent

    def insert(self, node):
        # returns root.
        BST.insert(self, node)
        return self.fix_avl(node)

    def __repr__(self):
        return f"BST(key={self.key}, height={self.height}, left={self.left.__repr__()}, right={self.right.__repr__()})"
