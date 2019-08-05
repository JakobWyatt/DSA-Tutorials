from abc import ABC, abstractmethod
import typing
import numpy as np

class DSAQueue(ABC):
    @abstractmethod
    def enqueue(item : object):
        pass

    @abstractmethod
    def dequeue() -> object:
        pass

    @abstractmethod
    def peek() -> object:
        pass

    @abstractmethod
    def isEmpty() -> bool:
        pass

    @abstractmethod
    def isFull() -> bool:
        pass

    @abstractmethod
    def count() -> bool:
        pass
