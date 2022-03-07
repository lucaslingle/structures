"""
Basic Binary Search Tree (BST) implementation.
"""


class BST:
    def __init__(self, key, parent):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None
        self.height = 0

    def check_ri(self):
        msg1 = "BST Representation Invariant Violated"
        msg2 = "BST Parent-Child Consistency Invariant Violated"
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

    def search(self, key):
        if key == self.key:
            return self
        if key < self.key and self.left:
            return self.left.search(key)
        if key > self.key and self.right:
            return self.right.search(key)
        return None

    def min(self):
        node = self
        while node.left:
            node = node.left
        return node

    def _next_larger(self, node):
        if not node:
            return None
        if node.right:
            return node.right.min()
        ancestor = node.parent
        while ancestor and ancestor.key < node.key:
            ancestor = ancestor.parent
        return ancestor

    def next_larger(self, key):
        node = self.search(key)
        return self._next_larger(node)

    def _update_heights(self, node):
        while node:
            node.height = 1 + max(
                node.left.height if node.left else -1,
                node.right.height if node.right else -1)
            node = node.parent

    def _insert(self, node):
        if node.key == self.key:
            raise ValueError('Duplicate keys not supported.')
        elif node.key < self.key:
            if not self.left:
                self.left = node
                node.parent = self
                self._update_heights(node.parent)
            else:
                assert isinstance(self.left, BST)
                self.left._insert(node)
        else:
            if not self.right:
                self.right = node
                node.parent = self
                self._update_heights(node.parent)
            else:
                assert isinstance(self.right, BST)
                self.right._insert(node)

    def insert(self, key, check_ri=False):
        node = BST(key=key, parent=None)
        self._insert(node)
        if check_ri:
            while node.parent:
                node = node.parent
            node.check_ri()

    def _delete(self, node):
        # case 1: neither left nor right child
        if not node.left and not node.right:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
                self._update_heights(node.parent)
        # case 2: both left and right child
        elif node.left and node.right:
            inorder_successor = self._next_larger(node)
            if inorder_successor:
                self._delete(inorder_successor)
                node.key = inorder_successor.key
        # case 3: only one child
        else:
            child = node.left if node.left else node.right
            child.parent = node.parent
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = child
                else:
                    node.parent.right = child
                self._update_heights(node.parent)

    def delete(self, key, check_ri=False):
        # todo: need to return new root in case it changes.
        node = self.search(key)
        self._delete(node)
        if check_ri:
            while node.parent:
                node = node.parent
            print(node.__repr__())
            node.check_ri()

    def __repr__(self):
        return f"BST(key={self.key}, height={self.height}, left={self.left.__repr__()}, right={self.right.__repr__()})"
