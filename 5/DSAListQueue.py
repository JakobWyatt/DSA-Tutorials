import typing
from linkedLists import *

class DSAListQueue():
    def __init__(self):
        self._queue = DSALinkedList()

    def enqueue(self, item : object):
        self._queue.insertLast(item)

    def dequeue(self) -> object:
        return self._queue.removeFirst()

    def peek(self) -> object:
        return self._queue.peekFirst()

    def isEmpty(self) -> bool:
        return self._queue.isEmpty()

    # Starts at the element referenced by peek
    def __iter__(self):
        return self._queue.__iter__()

    def __reversed__(self):
        return self._queue.__reversed__()
