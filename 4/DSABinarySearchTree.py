from typing import Generator
import testing

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
        ...

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

    def inorder(self) -> Generator[(object, object), None, None]:
        ...

    def preorder(self) -> Generator[(object, object), None, None]:
        ...

    def postorder(self) -> Generator[(object, object), None, None]:
        ...

class TestDSABinarySearchTree(unittest.TestCase):
    def testInsert(self):
        ...

if __name__ == "__main__":
    unittest.main()
