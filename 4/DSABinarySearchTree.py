from typing import Generator
import unittest

class DSABinarySearchTree:
    class DSATreeNode:
        def __init__(self, key: object, value: object,
            left: 'DSATreeNode', right: 'DSATreeNode'):
            self._key = key
            self._value = value
            self._left = left
            self._right = right

    def __init__(self):
        self._root = None

    def find(self, key: object) -> object:
        return DSABinarySearchTree._findRec(key, self._root)

    @staticmethod
    def _findRec(key: object, cur: 'DSATreeNode') -> object:
        val = None
        if cur == None:
            raise ValueError("Key: " + str(key) + " not found.")
        elif key == cur._key:
            val = cur._value
        elif key < cur._key:
            value = DSABinarySearchTree._findRec(key, cur._left)
        else:
            value = DSABinarySearchTree._findRec(key, cur._right)
        return val

    def insert(self, key: object, value: object):
        ...

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
        ...

    def postorder(self):
        ...

class TestDSABinarySearchTree(unittest.TestCase):
    def testInsertFind(self):
        tree = DSABinarySearchTree()
        tree.insert(1, "one")
        tree.insert(3, "three")
        tree.insert(2, "two")
        tree.insert(4, "four")
        tree.insert(-1, "-one")
        tree.insert(0, "zero")
        tree.insert(-2, "-two")
        self.assertEqual(tree.find(1), "one")
        self.assertEqual(tree.find(3), "three")
        self.assertEqual(tree.find(2), "two")
        self.assertEqual(tree.find(3), "three")
        self.assertEqual(tree.find(-1), "-one")
        self.assertEqual(tree.find(0), "zero")
        self.assertEqual(tree.find(-2), "-two")
        with self.assertRaises(ValueError):
            tree.find(4)
            tree.insert(1, "one")
            tree.insert(3, "three")
            tree.insert(2, "two")
            tree.insert(4, "four")
            tree.insert(-1, "-one")
            tree.insert(0, "zero")
            tree.insert(-2, "-two")

if __name__ == "__main__":
    unittest.main()
