import unittest
import typing
import numpy as np


class DSAHeapEntry:
    def __init__(self, priority: int, value: object):
        self._priority = priority
        self._value = value

    @property
    def priority(self) -> int:
        return self._priority
        
    @priority.setter
    def priority(self, p: int):
        self._priority = p

    @property
    def value(self) -> int:
        return self._value
        
    @value.setter
    def value(self, p: int):
        self._value = p


class DSAHeap:
    def __init__(self, size: int = 100):
        self._heap = np.zeros(size, dtype=object)
        self._count = 0

    def add(self, priority: int, value: object):
        ...

    def remove(self) -> object:
        ...

    @staticmethod
    def heapSort(values: Array[Object]) -> 'DSAHeapEntry':
        ...

    def _trickleUp(self, index: int):
        ...

    def _trickleDown(self, index: int):
        ...


class TestDSAHeap:
    ...


if __name__ == "__main__":
    unittest.main()
