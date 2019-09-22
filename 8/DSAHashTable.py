import unittest
from enum import Enum
import numpy as np

class DSAHashEntry:
    class status(Enum):
        EMPTY = -1
        USED = 0
        FULL = 1

    def __init__(self, key = None, value: object = None,
                 state: "status" = status.EMPTY):
        self._key = key
        self._value = value
        self._state = state
    
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state


class DSAHashTable:
    def __init__(self, size: int = 100, *, loadFactor: float = 0.5, resizeFactor: float = 2):
        self._hashArray = np.empty(DSAHashTable._nextPrime(size), dtype=object)
        for i in range(len(self._hashArray)):
            self._hashArray[i] = DSAHashEntry()
        self._count = 0

        if loadFactor < 0 or loadFactor > 1:
            raise ValueError("Load factor must be in the range [0, 1]")
        self._loadFactor = loadFactor

        if resizeFactor <= 1:
            raise ValueError("Resize factor must be greater than 1")
        self._resizeFactor = resizeFactor

    def put(self, key, value: object) -> None:
        candidate = self._find(key)
        if candidate.state != DSAHashEntry.status.FULL:
            # Inserting into table
            self._count += 1
            if self._resizeIfNeeded():
                candidate = self._find(key)
            candidate.state = DSAHashEntry.status.FULL
            candidate.key = key
        candidate.value = value

    def get(self, key) -> DSAHashEntry:
        candidate = self._find(key)
        if candidate.state != DSAHashEntry.status.FULL:
            raise ValueError("Key not found.")
        return candidate.value

    def hasKey(self, key) -> bool:
        return self._find(key).state == DSAHashEntry.status.FULL

    def remove(self, key) -> object:
        candidate = self._find(key)
        if candidate.state != DSAHashEntry.status.FULL:
            raise ValueError("Key not found.")
        candidate.state = DSAHashEntry.status.USED
        candidate.key = None
        value = candidate.value
        candidate.value = None
        return value

    def loadFactor(self) -> float:
        return len(self) / len(self._hashArray)

    def export(self) -> str:
        ...

    @staticmethod
    def read(str: str) -> 'DSAHashTable':
        # Discard any duplicates
        ...

    def __len__(self):
        return self._count

    def _find(self, key) -> DSAHashEntry:
        i = DSAHashTable._hash(key, len(self._hashArray))
        stepHash = DSAHashTable._stepHash(key, len(self._hashArray))
        candidate = self._hashArray[i]
        jumps = 0
        while candidate.key != key and candidate.state != DSAHashEntry.status.EMPTY and jumps < len(self._hashArray):
            jumps += 1
            i = (i + stepHash) % len(self._hashArray)
            candidate = self._hashArray[i]
        return candidate

    def _resizeIfNeeded(self) -> bool:
        # Only ever increases the size
        resized = False
        if self.loadFactor() > self._loadFactor:
            self._resize(len(self._hashArray) * self._resizeFactor)
            resized = True
        return resized

    def _resize(self, size):
        newTable = DSAHashTable(size)
        for k, v in self:
            newTable.put(k, v)
        self._hashArray = newTable._hashArray

    def __iter__(self):
        def hashIter(hashArray):
            for x in hashArray:
                if x.state == DSAHashEntry.status.FULL:
                    yield (x.key, x.value)
        return hashIter(self._hashArray)

    @staticmethod
    def _hash(key, len: int) -> int:
        return DSAHashTable._baseHash(key) % len

    # Hash function requirements:
    # Fit within the size of the array
    # Fast to compute
    # Repeatable
    # Distribute evenly
    @staticmethod
    def _baseHash(key) -> int:
        import struct
        # Implementation of java string hash
        hash = 0
        if isinstance(key, int):
            key = struct.pack("i", key)
        elif isinstance(key, str):
            key = key.encode()
        else:
            raise ValueError("Unsupported key type. Use str or int instead.")
        
        for x in key:
            hash = 31 * hash + x
        return hash

    @staticmethod
    def _stepHash(key, len: int) -> int:
        return DSAHashTable._baseHash(key) % (len - 1) + 1

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

    def testPutGetResize(self):
        table = DSAHashTable(1)
        self.assertRaises(ValueError, table.get, "hello")
        table.put("hello", "world")
        self.assertEqual(table.get("hello"), "world")
        self.assertRaises(ValueError, table.get, 1)
        table.put(1, 2)
        self.assertEqual(table.get(1), 2)
        self.assertEqual(table.get("hello"), "world")
        self.assertRaises(ValueError, table.get, "world")
        table.put("world", "hello")
        self.assertEqual(table.get("world"), "hello")
        self.assertEqual(table.get("hello"), "world")
        self.assertEqual(table.get(1), 2)

    def testDelete(self):
        # Increase hash probability
        table = DSAHashTable(4, loadFactor=1.0)
        table.put(0, 0)
        table.put(1, 1)
        table.put(2, 2)
        table.put(3, 3)
        table.put(4, 4)
        self.assertEqual(table.get(0), 0)
        self.assertEqual(table.get(1), 1)
        self.assertEqual(table.get(2), 2)
        self.assertEqual(table.get(3), 3)
        self.assertEqual(table.get(4), 4)
        self.assertEqual(table.remove(0), 0)
        self.assertEqual(table.get(1), 1)
        self.assertEqual(table.get(2), 2)
        self.assertEqual(table.get(3), 3)
        self.assertEqual(table.get(4), 4)
        self.assertFalse(table.hasKey(0))
        self.assertEqual(table.remove(2), 2)
        self.assertEqual(table.get(1), 1)
        self.assertEqual(table.get(3), 3)
        self.assertEqual(table.get(4), 4)
        self.assertFalse(table.hasKey(0))
        self.assertFalse(table.hasKey(2))


    def testLoadFactor(self):
        table = DSAHashTable(4, loadFactor=1.0)
        self.assertEqual(0.0, table.loadFactor())
        table.put(0, 0)
        self.assertEqual(1/5, table.loadFactor())
        table.put(1, 1)
        self.assertEqual(2/5, table.loadFactor())
        table.put(2, 2)
        self.assertEqual(3/5, table.loadFactor())
        table.put(3, 3)
        self.assertEqual(4/5, table.loadFactor())
        table.put(4, 4)
        self.assertEqual(1.0, table.loadFactor())

    def testReadExport(self):
        # First, test that read works
        # Then, test that export works
        with open("RandomNames7000.csv", "r") as f:
            for x in f:
                names = {}
                key, value = x.rstrip('\n').split(',')
                if key not in names:
                    # Dont update duplicates
                    names[key] = value
            table = DSAHashTable.read("".join(f))
        # Test that read works
        for key in names:
            self.assertEqual(names[key], table.get(key))
        # Test that write works
        table2 = DSAHashTable.read(table.export())
        for k, v in table:
            self.assertEqual(table.remove(k), table2.remove(k))
        self.assertEqual(len(table2), 0)


if __name__ == "__main__":
    unittest.main()
