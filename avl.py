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

    def update_height(self):
        rh = self.right.height if self.right else -1
        lh = self.left.height if self.left else -1
        self.height = 1 + max(lh, rh)

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
        x = self
        y = self.right
        assert y
        # fix parent up for rotated subtree
        y.parent = x.parent
        if y.parent:
            if y.parent.left is x:     # subtree is to the left
                y.parent.left = y
            elif y.parent.right is x:  # subtree is to the right
                y.parent.right = y
        # perform rotation
        x.right = y.left
        if x.right:
            x.right.parent = x
        y.left = x; x.parent = y
        x.update_height()
        y.update_height()
        return y

    def right_rotate(self):
        y = self
        x = self.left
        assert x
        # fix parent up for rotated subtree
        x.parent = y.parent
        if x.parent:
            if x.parent.left is y:     # subtree is to the left
                x.parent.left = x
            elif x.parent.right is y:  # subtree is to the right
                x.parent.right = x
        # perform rotation
        y.left = x.right
        if y.left:
            y.left.parent = y
        x.right = y; y.parent = x
        y.update_height()
        x.update_height()
        return x

    def fix_right_heavy(self):
        assert self.balance == 2
        x = self
        if x.right.balance >= 0:
            return x.left_rotate()
        else:
            z = x.right
            y = z.right_rotate()
            x.right = y
            x.right.parent = x
            return x.left_rotate()

    def fix_left_heavy(self):
        assert self.balance == -2
        # left heavy node x, deal by symmetry
        x = self
        if x.left.balance <= 0:
            return x.right_rotate()
        else:
            z = x.left
            y = z.left_rotate()
            x.left = y
            x.left.parent = x
            return x.right_rotate()

    def rebalance(self, node):
        root = None
        while node:
            node.update_height()
            if node.balance == 2:
                _ = node.fix_right_heavy()
            if node.balance == -2:
                _ = node.fix_left_heavy()
            if node.parent is None:
                root = node
            node = node.parent
        return root

    def insert(self, key, check_ri=False):
        # returns root since tree may be rotated
        node = AVL(key=key, parent=None)
        BST._insert(self, node)
        root = self.rebalance(node)
        if check_ri:
            root.check_ri()
        return root

    def delete(self, key, check_ri=False):
        # returns root since tree may be rotated
        node = BST.search(self, key)
        parent = node.parent
        BST._delete(self, node)
        root = self.rebalance(parent)
        if check_ri:
            root.check_ri()
        return root
