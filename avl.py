"""
AVL Tree implementation.
"""

from bst import BST


class AVL(BST):
    def __init__(self, key, parent):
        super().__init__(key=key, parent=parent)

    @property
    def balance(self):
        rh = self.right.height if self.right else -1
        lh = self.left.height if self.left else -1
        return rh - lh

    def check_ri(self):
        msg0 = "AVL Representation Invariant Violated"
        msg1 = "BST Representation Invariant Violated"
        msg2 = "BST Parent-Child Consistency Invariant Violated"
        if not (-2 < self.balance < 2):
            raise RuntimeError(msg0)
        if self.left:
            if not self.left.key < self.key:
                raise RuntimeError(msg1)
            if self.left.parent is not self:
                raise RuntimeError(msg2)
            self.left.check_ri()
        if self.right:
            if not self.right.key > self.key:
                raise RuntimeError(msg1)
            if self.right.parent is not self:
                raise RuntimeError(msg2)
            self.right.check_ri()

    def left_rotate(self):
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
        while node:
            parent = node.parent
            if parent:
                go_right = parent.right == node
            if node.balance == 2:
                x = node
                y = x.fix_right_heavy()
                if parent:
                    if go_right:
                        parent.right = y
                    else:
                        parent.left = y
                    y.parent = parent
                    self._update_heights(parent)
                else:
                    y.parent = None
                    return y
            if node.balance == -2:
                y = node
                x = y.fix_left_heavy()
                if parent:
                    if go_right:
                        parent.right = x
                    else:
                        parent.left = x
                    y.parent = parent
                    self._update_heights(parent)
                else:
                    x.parent = None
                    return x
            if not parent:
                return node
            node = parent

    def insert(self, key, check_ri=False):
        # returns root since tree may be rotated
        node = AVL(key=key, parent=None)
        BST._insert(self, node)
        root = self.fix_avl(node.parent)
        if check_ri:
            root.check_ri()
        return root

    def delete(self, key, check_ri=False):
        # check this against the ref impl
        node = BST.search(self, key)
        parent = node.parent
        BST._delete(self, node)
        root = self.fix_avl(parent)
        if check_ri:
            root.check_ri()
        return root
