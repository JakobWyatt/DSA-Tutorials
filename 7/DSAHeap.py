import unittest
from typing import List, Tuple
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
        for i in range(len(self._heap)):
            self._heap[i] = DSAHeapEntry(None, None)
        self._count = 0

    def add(self, priority: int, value: object):
        if len(self) == len(self._heap):
            raise ValueError("Heap is full.")
        self._heap[len(self)].priority = priority
        self._heap[len(self)].value = value
        self._trickleUp(len(self))
        self._count += 1

    def remove(self) -> object:
        if len(self) == 0:
            raise ValueError("Heap is empty.")
        value = self._heap[0].value
        self._count -= 1
        # Swap to conserve consistency of objects
        self._heap[0], self._heap[len(self)] = self._heap[len(self)], self._heap[0]
        self._trickleDown(0)
        return value

    def _heapify(self):
        for i in reversed(range(int(len(self) / 2) - 1)):
            self._trickleDown(i)

    def _heapSort(self):
        self._heapify()
        for i in reversed(range(1, len(self))):
            self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
            self._count -= 1
            self._trickleDown(0)

    @staticmethod
    def heapSort(values: List[Tuple[int, object]]) -> List[Tuple[int, object]]:
        heap = DSAHeap(len(values))
        for i in range(len(values)):
            heap._heap[i].priority = values[i][0]
            heap._heap[i].value = values[i][1]
        heap._count = len(values)
        heap._heapSort()
        return [(x.priority, x.value) for x in heap._heap]

    def _trickleUp(self, index: int):
        parent = int((index - 1) / 2)
        if index > 0 and self._heap[parent].priority < self._heap[index].priority:
            self._heap[parent], self._heap[index] = self._heap[index], self._heap[parent]
            self._trickleUp(parent)

    def _trickleDown(self, index: int):
        left = index * 2 + 1
        right = left + 1
        # Choose the element to swap with
        swap = 0
        if left < len(self):
            swap = left
        if right < len(self) and self._heap[right].priority > self._heap[left].priority:
            swap = right
        # Perform the swap
        if swap != 0 and self._heap[swap].priority > self._heap[index].priority:
            self._heap[swap], self._heap[index] = self._heap[index], self._heap[swap]
            self._trickleDown(swap)

    def __len__(self):
        return self._count

    def __iter__(self):
        def iterate(heap):
            for i in range(len(heap)):
                yield heap._heap[i]
        return iterate(self)


class TestDSAHeap(unittest.TestCase):
    def testAddRemove(self):
        heap = DSAHeap()
        self.assertRaises(ValueError, heap.remove)
        heap.add(5, "five")
        heap.add(6, "six")
        heap.add(-1, "negone")
        heap.add(0, "zero")
        heap.add(1, "one")
        heap.add(-50, "neg50")
        heap.add(-51, "neg51")
        heap.add(50, "fifty")
        self.assertEqual(heap.remove(), "fifty")
        self.assertEqual(heap.remove(), "six")
        self.assertEqual(heap.remove(), "five")
        heap.add(100, "bignoi")
        heap.add(50, "fifty")
        heap.add(0, "zero")
        heap.add(-49, "neg49")
        heap.add(-51, "neg51")
        self.assertEqual(heap.remove(), "bignoi")
        self.assertEqual(heap.remove(), "fifty")
        self.assertEqual(heap.remove(), "one")
        self.assertEqual(heap.remove(), "zero")
        self.assertEqual(heap.remove(), "zero")
        self.assertEqual(heap.remove(), "negone")
        self.assertEqual(heap.remove(), "neg49")
        self.assertEqual(heap.remove(), "neg50")
        self.assertEqual(heap.remove(), "neg51")
        self.assertEqual(heap.remove(), "neg51")

    def testHeapSort(self):
        with open("RandomNames7000.csv", "r") as f:
            student = [x.rstrip("\n").split(",") for x in f]
            for x1, x2 in zip(sorted(student), DSAHeap.heapSort(student)):
                self.assertEqual(x1[0], x2[0])


if __name__ == "__main__":
    unittest.main()
