from typing import Generator
import unittest

class DSATreeNode:
    def __init__(self, key: object, value: object,
        left: 'DSATreeNode', right: 'DSATreeNode'):
        self._key = key
        self._value = value
        self._left = left
        self._right = right

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

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
        elif key == cur.key:
            val = cur.value
        elif key < cur.key:
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
        elif cur.key == key:
            raise ValueError(f"Key {key} already exists.")
        elif key < cur.key:
            cur._left = DSABinarySearchTree._insertRec(key, value, cur._left)
        else:
            cur._right = DSABinarySearchTree._insertRec(key, value, cur._right)
        return updateNode

    def delete(self, key: object) -> object:
        ...

    @staticmethod
    def render(gv: str, *, type='svg'):
        """
        Renders a graphviz DOT file.
        Prints the render result to a temporary output file.
        Opens this file using the default program assigned
        to the given extension.
        """
        from subprocess import run
        from shutil import which
        from tempfile import NamedTemporaryFile

        if which("dot") == None:
            raise RuntimeError("Rendering DOT files requires "
                "graphviz to be installed.")
        else:
            with NamedTemporaryFile(delete=False, suffix=f'.{type}') as f:
                run(["dot", f"-T{type}", "-o", f.name], input=gv.encode())
                if which("xdg-open") != None:
                    run(["xdg-open", f.name])
                elif which("open") != None:
                    run(["open", f.name])
                else:
                    print(f"Could not open the rendered image. "
                        "File written to {f.name}")

    @staticmethod
    def _uniqueNode(parent: str, isLeft: bool) -> str:
        """
        Creates a unique hidden graphviz node.
        """
        import uuid
        import string
        # Create valid, unique node identifier.
        id = str(uuid.uuid4()).replace("-", "").lstrip(string.digits)
        return (f"{id} [label=\"A\", shape=point]\n"
            f"{parent}:{'sw' if isLeft else 'se'} -> {id}:n\n")

    def display(self) -> str:
        """
        Generates a string that represents this tree.
        This string can be compiled into a visual graph using
        dot, as part of the package graphviz.
        """
        gv = "digraph {\nsplines=false\n"
        # Iterate through the tree with postorder.
        # This means that any nodes referenced will already be printed.
        for x in self.postorder():
            gv += f"{x.key} [label=\"{x.key}: {x.value}\"]\n"
            if x._left != None:
                gv += f"{x.key}:sw -> {x._left.key}:n\n"
            else:
                gv += DSABinarySearchTree._uniqueNode(x.key, True)
            if x._right != None:
                gv += f"{x.key}:se -> {x._right.key}:n\n"
            else:
                gv += DSABinarySearchTree._uniqueNode(x.key, False)
        return gv + "}\n"

    def height(self) -> int:
        return DSABinarySearchTree._heightRec(self._root)

    def _minHeight(self) -> int:
        return DSABinarySearchTree._heightRec(self._root, findMax=False)

    @staticmethod
    def _heightRec(curNode: 'DSATreeNode', *, findMax=True) -> int:
        """
        Finds either the maximum or minimum height of a tree.
        """
        depth = -1
        picker = max if findMax else min
        if curNode != None:
            depth = picker(
                DSABinarySearchTree._heightRec(curNode._left),
                DSABinarySearchTree._heightRec(curNode._right)) + 1
        return depth

    def min(self) -> (object, object):
        cur = self._root
        while cur._left != None:
            cur = cur._left
        return (cur.key, cur.value)

    def max(self) -> (object, object):
        cur = self._root
        while cur._right != None:
            cur = cur._right
        return (cur.key, cur.value)

    def balance(self) -> float:
        """
        Balance is a number between 0 and 1,
        where 0 is the least balanced
        and 1 is perfectly balanced.
        This is calculated with the equation:
        (min_height - max_height)/max_height + 1
        """
        max_height = self.height()
        balance = 1.0
        if max_height > 0:
            balance = (self._minHeight() - max_height)/max_height + 1.0
        return balance

    def inorder(self) -> Generator['DSATreeNode', None, None]:
        def inorderGenerator(cur: 'DSATreeNode'):
            if cur != None:
                yield from inorderGenerator(cur._left)
                yield cur
                yield from inorderGenerator(cur._right)
        return inorderGenerator(self._root)

    def preorder(self):
        def preorderGenerator(cur: 'DSATreeNode'):
            if cur != None:
                yield cur
                yield from preorderGenerator(cur._left)
                yield from preorderGenerator(cur._right)
        return preorderGenerator(self._root)

    def postorder(self):
        def postorderGenerator(cur: 'DSATreeNode'):
            if cur != None:
                yield from postorderGenerator(cur._left)
                yield from postorderGenerator(cur._right)
                yield cur
        return postorderGenerator(self._root)

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

    def testTraversal(self):
        tree = DSABinarySearchTree()
        nodes = [(1, "one"), (3, "three"), (2, "two"), (4, "four"),
            (-1, "-one"), (0, "zero"), (-2, "-two")]
        preorder = [(1, "one"), (-1, "-one"), (-2, "-two"),
            (0, "zero"), (3, "three"), (2, "two"), (4, "four")]
        inorder = [(-2, "-two"), (-1, "-one"), (0, "zero"), (1, "one"),
            (2, "two"), (3, "three"), (4, "four")]
        postorder = [(-2, "-two"), (0, "zero"), (-1, "-one"),
            (2, "two"), (4, "four"), (3, "three"), (1, "one")]
        for x in nodes:
            tree.insert(*x)
        for x1, x2 in zip(preorder,
            [(x.key, x.value) for x in tree.preorder()]):
            self.assertEqual(x1, x2)
        for x1, x2 in zip(inorder,
            [(x.key, x.value) for x in tree.inorder()]):
            self.assertEqual(x1, x2)
        for x1, x2 in zip(postorder,
            [(x.key, x.value) for x in tree.postorder()]):
            self.assertEqual(x1, x2)

    def testMinMax(self):
        tree = DSABinarySearchTree()
        nodes = [(1, "one"), (3, "three"), (2, "two"), (4, "four"),
            (-1, "-one"), (0, "zero"), (-2, "-two")]
        for x in nodes:
            tree.insert(*x)
        self.assertEqual(tree.min(), (-2, "-two"))
        self.assertEqual(tree.max(), (4, "four"))

    def testHeight(self):
        tree = DSABinarySearchTree()
        self.assertEqual(tree.height(), -1)
        tree.insert(1, "one")
        self.assertEqual(tree.height(), 0)
        tree.insert(3, "three")
        self.assertEqual(tree.height(), 1)
        tree.insert(-1, "-one")
        self.assertEqual(tree.height(), 1)
        tree.insert(4, "four")
        self.assertEqual(tree.height(), 2)
        tree.insert(-2, "-two")
        self.assertEqual(tree.height(), 2)
        tree.insert(-3, "three")
        self.assertEqual(tree.height(), 3) 

    def testDisplay(self):
        tree = DSABinarySearchTree()
        nodes = [(1, "one"), (3, "three"), (5, "five"), (4, "four"),
            (-1, "-one"), (-2, "-two"), (0, "zero")]
        for x in nodes:
            tree.insert(*x)
        try:
            DSABinarySearchTree.render(tree.display())
        except RuntimeError as err:
            print(str(err))

    def testBalance(self):
        tree = DSABinarySearchTree()
        self.assertAlmostEqual(tree.balance(), 1.0, places=3)
        tree.insert(1, "one")
        self.assertAlmostEqual(tree.balance(), 1.0, places=3)
        tree.insert(3, "three")
        self.assertAlmostEqual(tree.balance(), 0.0, places=3)
        tree.insert(-1, "-one")
        self.assertAlmostEqual(tree.balance(), 1.0, places=3)
        tree.insert(5, "five")
        self.assertAlmostEqual(tree.balance(), 0.5, places=3)
        tree.insert(4, "four")
        self.assertAlmostEqual(tree.balance(), 1/3, places=3)

if __name__ == "__main__":
    unittest.main()
