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
        if cur is None:
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
    def _insertRec(key: object, value: object,
                   cur: 'DSATreeNode') -> 'DSATreeNode':
        if cur is None:
            cur = DSATreeNode(key, value, None, None)
        elif cur.key == key:
            raise ValueError(f"Key {key} already exists.")
        elif key < cur.key:
            cur._left = DSABinarySearchTree._insertRec(key, value, cur._left)
        else:
            cur._right = DSABinarySearchTree._insertRec(key, value, cur._right)
        return cur

    def delete(self, key: object):
        self._root = DSABinarySearchTree._deleteRec(key, self._root)

    @staticmethod
    def _deleteRec(key: object, cur: 'DSATreeNode') -> 'DSATreeNode':
        if cur is None:
            raise ValueError(f"Key {key} not in tree.")
        elif cur.key == key:
            cur = DSABinarySearchTree._deleteNode(key, cur)
        elif key < cur.key:
            cur._left = DSABinarySearchTree._deleteRec(key, cur._left)
        else:
            cur._right = DSABinarySearchTree._deleteRec(key, cur._right)
        return cur

    @staticmethod
    def _deleteNode(key: object, cur: 'DSATreeNode') -> 'DSATreeNode':
        if cur._left is None and cur._right is None:
            updateNode = None
        elif cur._left is None:
            updateNode = cur._right
        elif cur._right is None:
            updateNode = cur._left
        else:
            updateNode = DSABinarySearchTree._promoteSuccessor(cur._right)
            if updateNode is not cur._right:
                updateNode._right = cur._right
            updateNode._left = cur._left
        return updateNode

    @staticmethod
    def _promoteSuccessor(cur: 'DSATreeNode') -> 'DSATreeNode':
        succ = cur
        if cur._left is not None:
            succ = DSABinarySearchTree._promoteSuccessor(cur._left)
            if succ is cur._left:
                # Perform adoption.
                # If succ._right = None, then cur._left is a leaf node,
                # and is updated to reflect this.
                cur._left = succ._right
        return succ

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

        if which("dot") is None:
            raise RuntimeError("Rendering DOT files requires "
                               "graphviz to be installed.")
        else:
            with NamedTemporaryFile(delete=False, suffix=f'.{type}') as f:
                # Render the graph.
                run(["dot", f"-T{type}", "-o", f.name], input=gv.encode())
                # Attempt to display the graph.
                if which("xdg-open") is not None:
                    run(["xdg-open", f.name])
                elif which("open") is not None:
                    run(["open", f.name])
                else:
                    print("Could not open the rendered image. "
                          f"File written to {f.name}")

    @staticmethod
    def _uniqueNode(parent: str, isLeft: bool) -> str:
        """
        Creates a unique hidden graphviz node.
        """
        import uuid
        import string
        # Create valid, unique node identifier by modifying a uuid.
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
            if x._left is not None:
                gv += f"{x.key}:sw -> {x._left.key}:n\n"
            else:
                gv += DSABinarySearchTree._uniqueNode(x.key, True)
            if x._right is not None:
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
        if curNode is not None:
            depth = picker(
                DSABinarySearchTree._heightRec(curNode._left),
                DSABinarySearchTree._heightRec(curNode._right)) + 1
        return depth

    def min(self) -> (object, object):
        cur = self._root
        while cur._left is not None:
            cur = cur._left
        return (cur.key, cur.value)

    def max(self) -> (object, object):
        cur = self._root
        while cur._right is not None:
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
            if cur is not None:
                yield from inorderGenerator(cur._left)
                yield cur
                yield from inorderGenerator(cur._right)
        return inorderGenerator(self._root)

    def preorder(self):
        def preorderGenerator(cur: 'DSATreeNode'):
            if cur is not None:
                yield cur
                yield from preorderGenerator(cur._left)
                yield from preorderGenerator(cur._right)
        return preorderGenerator(self._root)

    def postorder(self):
        def postorderGenerator(cur: 'DSATreeNode'):
            if cur is not None:
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

    def testDelete(self):
        tree = DSABinarySearchTree()
        nodes = [(1, "one"), (3, "three"), (2, "two"), (4, "four"),
                 (-1, "-one"), (0, "zero"), (-2, "-two")]
        for x in nodes:
            tree.insert(*x)
        tree.delete(1)
        for x1, x2 in zip(tree.postorder(), [-2, 0, -1, 4, 3, 2]):
            self.assertEqual(x1.key, x2)
        tree.delete(-1)
        for x1, x2 in zip(tree.postorder(), [-2, 0, 4, 3, 2]):
            self.assertEqual(x1.key, x2)
        tree.delete(4)
        for x1, x2 in zip(tree.postorder(), [-2, 0, 3, 2]):
            self.assertEqual(x1.key, x2)


if __name__ == "__main__":
    unittest.main()
