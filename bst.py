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

    def fix_heights(self, node):
        print('BST.fix_heights')
        while node:
            print(f'BST.fix_heights.key = {node.key}')
            node.height = 1 + max(
                node.left.height if node.left else -1,
                node.right.height if node.right else -1)
            node = node.parent

    def _insert(self, node):
        print('BST._insert')
        if node.key == self.key:
            raise ValueError('Duplicate keys not supported.')
        elif node.key < self.key:
            if not self.left:
                self.left = node
                node.parent = self
                self.fix_heights(node.parent)
            else:
                assert isinstance(self.left, BST)
                self.left._insert(node)
        else:
            if not self.right:
                self.right = node
                node.parent = self
                self.fix_heights(node.parent)
            else:
                assert isinstance(self.right, BST)
                self.right._insert(node)

    def insert(self, node):
        print('BST.insert')
        self._insert(node)

    def search(self, key):
        print('BST.search')
        if key == self.key:
            return self
        if key < self.key and self.left:
            return self.left.search(key)
        if key > self.key and self.right:
            return self.right.search(key)
        raise ValueError('Key not found in tree.')

    def _delete(self, node):
        print('BST._delete')
        # case 1: neither left nor right child
        if not node.left and not node.right:
            if node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None
                self.fix_heights(node.parent)
        # case 2: both left and right child
        elif node.left and node.right:
            inorder_successor = node.right
            if inorder_successor:
                while inorder_successor.left:
                    inorder_successor = inorder_successor.left
                self._delete(inorder_successor)
                node.key = inorder_successor.key
        # case 3: only one child
        else:
            child = node.left if node.left else node.right
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
            self.fix_heights(node.parent)

    def delete(self, key):
        print('BST.delete')
        node = self.search(key)
        self._delete(node)
