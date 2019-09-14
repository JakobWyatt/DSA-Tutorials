import unittest
import typing
import numpy as np

from linkedLists import DSALinkedList


class DSAGraphVertex:
    def __init__(self, label: object, value: object):
        self._label = label
        self._value = value
        self._adjacent = DSALinkedList()
        self._visited = False

    @property
    def label(self) -> object:
        return self._label

    @property
    def value(self) -> object:
        return self._value

    @property
    def adjacent(self) -> 'DSALinkedList':
        return self._adjacent

    def addEdge(self, vertex: 'DSAGraphVertex') -> None:
        self._adjacent.insertFirst(vertex)

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, visited: bool) -> None:
        self._visited = bool(visited)

    def __str__(self) -> str:
        return ("{label},{value}:{adj}"
                .format(label=self.label, value=self.value,
                        adj=" ".join([x.label for x in self.adjacent])))

    def gv(self) -> str:
        return "".join([f"{self.label} -- {x.label}\n" for x in self.adjacent])

    def __eq__(self, other: 'DSAGraphVertex') -> bool:
        return self.label == other.label


class DSAGraph:
    def __init__(self):
        self._verticies = DSALinkedList()

    def addVertex(self, label: object, value: object) -> None:
        """
        Does not check for duplicates.
        """
        self._verticies.insertFirst(DSAGraphVertex(label, value))

    def addEdge(self, label1: object, label2: object) -> None:
        """
        Assumes that the nodes already exist.
        """
        vertex1 = self.getVertex(label1)
        vertex2 = self.getVertex(label2)
        vertex1.addEdge(vertex2)
        vertex2.addEdge(vertex1)

    def hasVertex(self, label: object) -> bool:
        return self._verticies.find(DSAGraphVertex(label, None))

    def getVertexCount(self) -> int:
        return self._verticies.count()

    def getEdgeCount(self) -> int:
        """
        Assumes an undirected graph.
        """
        return sum(x.adjacent.count() for x in self._verticies) // 2

    def getVertex(self, label: object) -> 'DSAGraphVertex':
        # Use list internals for efficiency
        return self._verticies._find(DSAGraphVertex(label, None))._data

    def getAdjacent(self, label: object) -> 'DSALinkedList':
        return self.getVertex(label).adjacent

    def isAdjacent(self, label1: object, label2: object) -> bool:
        return self.getVertex(label1).adjacent.find(DSAGraphVertex(label2, None))

    def displayAsList(self) -> str:
        return "".join(f"{x}\n" for x in self._verticies)

    def displayAsMatrix(self) -> str:
        label = [str(x.label) for x in self._verticies]
        colWidth = len(max(label, key=lambda x: len(x))) + 1
        # Pad initial row of labels
        matStr = ' ' * colWidth
        matStr += "".join([x + " " * (colWidth - len(x)) for x in label])
        matStr += "\n"
        adjMat = self.adjacencyMatrix()
        for i, l in enumerate(label):
            matStr += l + " " * (colWidth - len(l))
            matStr += (" " * (colWidth - 1)).join([str(x) for x in adjMat[i].flat])
            matStr += "\n"
        return matStr

    def adjacencyMatrix(self):
        count = self.getVertexCount()
        mat = np.zeros([count, count], dtype=int)
        for i, v in enumerate(self._verticies):
            for j, l in enumerate(self._verticies):
                mat[i][j] = 1 if v.adjacent.find(l) else 0
        return mat

    def display(self) -> str:
        return "strict graph {\n" + "".join([x.gv() for x in self._verticies]) + "}\n"

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
                run(["fdp", f"-T{type}", "-o", f.name], input=gv.encode())
                # Attempt to display the graph.
                if which("xdg-open") is not None:
                    run(["xdg-open", f.name])
                elif which("open") is not None:
                    run(["open", f.name])
                else:
                    print("Could not open the rendered image. "
                          f"File written to {f.name}")

    def depthFirstSearch() -> 'DSAGraph':
        ...

    def breadthFirstSearch() -> 'DSAGraph':
        ...


class TestDSAGraph(unittest.TestCase):
    def testAddVertex(self):
        graph = DSAGraph()
        self.assertFalse(graph.hasVertex("hello"))
        graph.addVertex("hello", "world")
        self.assertTrue(graph.hasVertex("hello"))
        self.assertFalse(graph.hasVertex("world"))
        graph.addVertex("world", "hello")
        self.assertTrue(graph.hasVertex("world"))

    def testVertexCount(self):
        graph = DSAGraph()
        self.assertEqual(0, graph.getVertexCount())
        graph.addVertex("hello", "world")
        self.assertEqual(1, graph.getVertexCount())
        graph.addVertex("world", "hello")
        self.assertEqual(2, graph.getVertexCount())

    def testAdjacentEdge(self):
        graph = DSAGraph()
        graph.addVertex("hello", "world")
        graph.addVertex("world", "hello")
        graph.addVertex("yeah", "boi")
        graph.addEdge("hello", "world")
        self.assertTrue(graph.isAdjacent("hello", "world"))
        self.assertFalse(graph.isAdjacent("yeah", "world"))
        graph.addEdge("hello", "yeah")
        for x1, x2 in zip(graph.getAdjacent("hello"), ["yeah", "world"]):
            self.assertEqual(x1.label, x2)

    def testEdgeCount(self):
        graph = DSAGraph()
        self.assertEqual(graph.getEdgeCount(), 0)
        graph.addVertex("hello", "world")
        graph.addVertex("world", "hello")
        graph.addVertex("yeah", "boi")
        self.assertEqual(graph.getEdgeCount(), 0)
        graph.addEdge("hello", "world")
        self.assertEqual(graph.getEdgeCount(), 1)
        graph.addEdge("yeah", "hello")
        self.assertEqual(graph.getEdgeCount(), 2)
        graph.addEdge("yeah", "world")
        self.assertEqual(graph.getEdgeCount(), 3)

    def testListDisplay(self):
        graph = DSAGraph()
        graph.addVertex("hello", "world")
        graph.addVertex("world", "hello")
        graph.addVertex("yeah", "boi")

        graph.addEdge("hello", "world")
        graph.addEdge("yeah", "hello")
        graph.addEdge("yeah", "world")

        self.assertEqual(graph.displayAsList(),
                        ("yeah,boi:world hello\n"
                         "world,hello:yeah hello\n"
                         "hello,world:yeah world\n"))

    def testMatrixDisplay(self):
        graph = DSAGraph()
        graph.addVertex("hello", "world")
        graph.addVertex("world", "hello")
        graph.addVertex("yeah", "boi")

        #graph.addEdge("hello", "world")
        graph.addEdge("yeah", "hello")
        graph.addEdge("yeah", "world")

        self.assertEqual(graph.displayAsMatrix(),
                        ("      yeah  world hello \n"
                         "yeah  0     1     1\n"
                         "world 1     0     0\n"
                         "hello 1     0     0\n"))

    def testDisplay(self):
        graph = DSAGraph()
        graph.addVertex("hello", "world")
        graph.addVertex("world", "hello")
        graph.addVertex("yeah", "boi")

        graph.addEdge("hello", "world")
        graph.addEdge("yeah", "hello")
        graph.addEdge("yeah", "world")

        self.assertEqual(graph.display(),
                        ("strict graph {\n"
                         "yeah -- world\n"
                         "yeah -- hello\n"
                         "world -- yeah\n"
                         "world -- hello\n"
                         "hello -- yeah\n"
                         "hello -- world\n"
                         "}\n"))


if __name__ == "__main__":
    unittest.main()
