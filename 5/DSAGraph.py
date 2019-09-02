import unittest
import typing

import linkedLists


class DSAGraphVertex:
    def __init__(self, label: object, value: object):
        ...

    @property
    def label(self) -> object:
        ...

    @property
    def value(self) -> object:
        ...

    def getAdjacent(self) -> 'DSALinkedList':
        ...

    def addEdge(self, vertex: 'DSAGraphVertex') -> None:
        ...

    @property
    def visited(self) -> bool:
        ...

    @visited.setter
    def visited(self, visited: bool) -> None:
        ...

    def __str__(self) -> str:
        ...


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
