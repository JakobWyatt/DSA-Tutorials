import unittest
import typing

import linkedLists


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


class DSAGraph:
    def __init__(self):
        ...

    def addVertex(self, label: object, value: object) -> None:
        ...

    def addEdge(self, label1: object, label2: object) -> None:
        ...

    def hasVertex(self, label: object) -> bool:
        ...

    def getVertexCount(self) -> int:
        ...

    def getEdgeCount(self) -> int:
        ...

    def getVertex(self, label: object) -> 'DSAGraphVertex':
        ...

    def getAdjacent(self, label: object) -> 'DSALinkedList':
        ...

    def isAdjacent(self, label1: object, label2: object) -> bool:
        ...

    def displayAsList(self) -> str:
        ...

    def displayAsMatrix(self) -> str:
        ...

    def display(self) -> str:
        ...

    @staticmethod
    def render(gv: str, *, type='svg'):
        ...

    def depthFirstSearch() -> 'DSAGraph':
        ...

    def breadthFirstSearch() -> 'DSAGraph':
        ...


class TestDSAGraph(unittest.TestCase):
    ...


if __name__ == "__main__":
    unittest.main()
