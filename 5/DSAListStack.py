import typing
from linkedLists import *

class DSAListStack():
    def __init__(self):
        self._stack = DSALinkedList()
    
    def push(self, item : object):
        self._stack.insertFirst(item)

    def pop(self) -> object:
        return self._stack.removeFirst()
    
    def top(self) -> object:
        return self._stack.peekFirst()

    def isEmpty(self) -> bool:
        return self._stack.isEmpty()

    # Starts at the most recently pushed value
    def __iter__(self):
        return self._stack.__iter__()

    def __reversed__(self):
        return self._stack.__reversed__()
