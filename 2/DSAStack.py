import typing
import numpy as np

class DSAStack():
    DEFAULT_CAPACITY = 100

    def __init__(self):
        self._stack = np.empty(DEFAULT_CAPACITY, dtype=object)
        self._count = 0
    
    def __init__(self, capacity : int):
        self._stack = np.empty(capacity, dtype=object)
        self._count = 0
    
    def push(self, item : object):
        self._stack[self._count] = item
        self._count += 1

    def pop(self) -> object:
        self._count -= 1
        return self._stack[self._count]
    
    def top(self) -> object:
        return self._stack[self._count - 1]

    def isEmpty(self) -> bool:
        return self._count == 0

    def isFull(self) -> bool:
        return self._count == len(self._stack)

    def count(self) -> int:
        return self._count
