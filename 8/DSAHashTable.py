import unittest
import numpy as np

class DSAHashEntry:
    def __init__(self, key = None, value: object = None, state: int = 0):
        self._key = key
        self._value = value
        self._state = state
    
    @property
    def key(self):
        return self._key
    
    @property
    def value(self):
        return self._value

    @property
    def state(self):
        return self._state


class DSAHashTable:
    def __init__(self, size: int = 100):
        self._hashArray = np.empty(DSAHashTable._nextPrime(size), dtype=object)
        for x in self._hashArray:
            x = DSAHashEntry()
        self._count = 0

    def put(self, key, value: object) -> None:
        ...

    def get(self, key) -> object:
        ...

    def remove(self, key) -> object:
        ...

    def getLoadFactor(self) -> float:
        ...

    def export(self) -> str:
        ...

    def _resize(self, size: int) -> str:
        ...
    
    @staticmethod
    def _hash(key) -> int:
        ...

    @staticmethod
    def _stepHash(key) -> int:
        ...

    @staticmethod
    def _nextPrime(x: int) -> int:
        if x == 2 or x == 1:
            x = 2
        else:
            # Can be made more efficient
            x = x - 1 if x % 2 == 0 else x - 2
            isPrime = False
            while not isPrime:
                i = 3
                x += 2
                isPrime = True
                while i ** 2 <= x and isPrime:
                    if x % i == 0:
                        isPrime = False
                    i += 2
        return x


class TestDSAHashTable(unittest.TestCase):
    def testNextPrime(self):
        self.assertEqual(2, DSAHashTable._nextPrime(1))
        self.assertEqual(2, DSAHashTable._nextPrime(2))
        self.assertEqual(3, DSAHashTable._nextPrime(3))
        self.assertEqual(5, DSAHashTable._nextPrime(4))
        self.assertEqual(5, DSAHashTable._nextPrime(5))
        self.assertEqual(163, DSAHashTable._nextPrime(158))


if __name__ == "__main__":
    unittest.main()
