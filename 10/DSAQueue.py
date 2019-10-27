import unittest
from typing import Type
from collections import deque


class DSAQueue():
    def __init__(self):
        self._queue = deque()

    def enqueue(self, item : object):
        self._queue.append(item)

    def dequeue(self) -> object:
        return self._queue.popleft()

    def peek(self) -> object:
        return self._queue[0]

    def isEmpty(self) -> bool:
        return len(self._queue) == 0

    # Starts at the element referenced by peek
    def __iter__(self):
        return self._queue.__iter__()


class TestDSAQueue(unittest.TestCase):
    def testDSAQueue(self):
        queue = DSAQueue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.peek(), 2)
        self.assertEqual(queue.dequeue(), 2)
        queue.enqueue(100)
        queue.dequeue()
        queue.dequeue()
        queue.dequeue()
        self.assertEqual(queue.dequeue(), 100)
        self.assertTrue(queue.isEmpty())


if __name__ == '__main__':
    unittest.main()
