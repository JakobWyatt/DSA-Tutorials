from typing import Generator
import unittest

class DSATreeNode:
        def __init__(self, key: object, value: object,
            left: 'DSATreeNode', right: 'DSATreeNode'):
            self._key = key
            self._value = value
            self._left = left
            self._right = right

class DSABinarySearchTree:
    def __init__(self):
        self._root = None

    def find(self, key: object) -> object:
        return DSABinarySearchTree._findRec(key, self._root)

    @staticmethod
    def _findRec(key: object, cur: 'DSATreeNode') -> object:
        val = None
        if cur == None:
            raise ValueError(f"Key {key} not found.")
        elif key == cur._key:
            val = cur._value
        elif key < cur._key:
            val = DSABinarySearchTree._findRec(key, cur._left)
        else:
            val = DSABinarySearchTree._findRec(key, cur._right)
        return val

    def insert(self, key: object, value: object):
        self._root = DSABinarySearchTree._insertRec(key, value, self._root)

    @staticmethod
    def _insertRec(key: object, value: object, cur: 'DSATreeNode') -> 'DSATreeNode':
        updateNode = cur
        if cur == None:
            updateNode = DSATreeNode(key, value, None, None)
        elif cur._key == key:
            raise ValueError(f"Key {key} already exists.")
        elif key < cur._key:
            cur._left = DSABinarySearchTree._insertRec(key, value, cur._left)
        else:
            cur._right = DSABinarySearchTree._insertRec(key, value, cur._right)
        return updateNode

    def delete(self, key: object) -> object:
        ...

    def display(self):
        ...

    def height(self) -> int:
        ...

    def min(self) -> (object, object):
        ...

    def max(self) -> (object, object):
        ...

    def balance(self) -> float:
        ...

    def inorder(self):
        ...

    def preorder(self):
        def preorderGenerator(cur: 'DSATreeNode'):
            if cur != None:
                yield (cur._key, cur._value)
                yield from preorderGenerator(cur._left)
                yield from preorderGenerator(cur._right)
        return preorderGenerator(self._root)

    def postorder(self):
        ...

class TestDSABinarySearchTree(unittest.TestCase):
    def testInsertFind(self):
        tree = DSABinarySearchTree()
        nodes = [(1, "one"), (3, "three"), (2, "two"), (4, "four"),
            (-1, "-one"), (0, "zero"), (-2, "-two")]
        for x in nodes:
            tree.insert(*x)
        for x in nodes:
            self.assertEqual(tree.find(x[0]), x[1])
        for x in nodes:
            with self.assertRaises(ValueError):
                tree.insert(x[0], x[1])

if __name__ == "__main__":
    unittest.main()
