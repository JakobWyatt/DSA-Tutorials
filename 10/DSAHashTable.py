import unittest
from enum import Enum
import numpy as np
from math import ceil

class DSAHashEntry:
    """
    This class represents an entry in a DSAHashTable,
    and contains setters and getters for entry keys,
    values, and state.
    """

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
    """
    This class is an impementation of an automatically resizing hash table,
    with O(1) amortized insert, delete, and find operations.
    """

    # autoResize allows creation of a "dumb" non-resizing table
    def __init__(self, size: int = 100, *, minLoadFactor: float = 0,
                 maxLoadFactor: float = 0.5, resizeFactor: float = 2, _autoResize = True):
        self._hashArray = np.empty(DSAHashTable._nextPrime(size), dtype=object)
        for i in range(len(self._hashArray)):
            self._hashArray[i] = DSAHashEntry()
        self._count = 0
        self._autoResize = _autoResize

        # Validating minLoadFactor and maxLoadFactor is difficult,
        # and amounts to verifying that the statement
        # ∀ n ∈ ℕ, ∃ b ≥ n ∈ prime s.t. lb < n/b < ub
        # is true. (n is the count and b is the table size)
        # Asserting that maxLoadFactor - minLoadFactor >= 1/3
        # or minLoadFactor = 0 is enough to satisfy this condition,
        # although it leaves out lots of valid solutions.
        if (maxLoadFactor - minLoadFactor < 1/3 and minLoadFactor != 0
            or maxLoadFactor > 1 or minLoadFactor < 0 or maxLoadFactor == 0):
            raise ValueError("Invalid max and min load factor.")
        self._minLoadFactor = minLoadFactor
        self._maxLoadFactor = maxLoadFactor

        # resizeFactor takes the range [maxLf, 1] and scales it to the range
        # [minLf, maxLf].
        # When shrinking the array, there is no resizeFactor to scale
        # all array sizes, as when count = 1 and array size → ∞, resizeFactor → ∞.
        # To circumvent this, calls to _resize use resizeFactor when possible,
        # and decide the value itself when resizeFactor is too small.
        if 1 > maxLoadFactor * resizeFactor or maxLoadFactor < minLoadFactor * resizeFactor:
            raise ValueError("Invalid resize factor.")
        self._resizeFactor = resizeFactor

    def put(self, key, value: object) -> None:
        candidate = self._find(key)
        if candidate is None or candidate.state != DSAHashEntry.status.FULL:
            # Inserting into table
            self._count += 1
            if self._autoResize:
                if self._resizeIfNeeded():
                    candidate = self._find(key)
            candidate.state = DSAHashEntry.status.FULL
            candidate.key = key
        candidate.value = value

    def get(self, key) -> DSAHashEntry:
        candidate = self._find(key)
        if candidate is None or candidate.state != DSAHashEntry.status.FULL:
            raise ValueError("Key not found.")
        return candidate.value

    def hasKey(self, key) -> bool:
        candidate = self._find(key)
        return candidate is not None and candidate.state == DSAHashEntry.status.FULL

    def remove(self, key) -> object:
        candidate = self._find(key)
        if candidate is None or candidate.state != DSAHashEntry.status.FULL:
            raise ValueError("Key not found.")
        self._count -= 1
        if self._autoResize:
            if self._resizeIfNeeded():
                candidate = self._find(key)
        candidate.state = DSAHashEntry.status.USED
        candidate.key = None
        value = candidate.value
        candidate.value = None
        return value

    def loadFactor(self) -> float:
        return len(self) / len(self._hashArray)

    def export(self) -> str:
        return "".join([f"{k},{v}\n" for (k, v) in self])

    @staticmethod
    def read(string: str) -> 'DSAHashTable':
        lines = string.split('\n')[:-1]
        table = DSAHashTable(len(lines))
        for x in lines:
            key, value = x.split(',')
            if not table.hasKey(key):
                table.put(key, value)
        return table

    def __len__(self):
        return self._count

    # Return None if there is no available space for the key
    def _find(self, key) -> DSAHashEntry:
        i = DSAHashTable._hash(key, len(self._hashArray))
        stepHash = DSAHashTable._stepHash(key, len(self._hashArray))
        candidate = self._hashArray[i]
        jumps = 0
        while candidate.key != key and candidate.state != DSAHashEntry.status.EMPTY and jumps < len(self._hashArray):
            jumps += 1
            i = (i + stepHash) % len(self._hashArray)
            candidate = self._hashArray[i]

        if jumps == len(self._hashArray):
            candidate = None
        return candidate

    def _resizeIfNeeded(self) -> bool:
        resized = False
        if self.loadFactor() > self._maxLoadFactor:
            self._resize(ceil(len(self._hashArray) * self._resizeFactor))
            resized = True
        elif self.loadFactor() < self._minLoadFactor:
            # Make consecutive remove as fast as possible
            self._resize(ceil(len(self) / self._maxLoadFactor))
            resized = True
        return resized

    def _resize(self, size):
        newTable = DSAHashTable(size, _autoResize=False)
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
        return DSAHashTable._javaStrHash(key) % len

    @staticmethod
    def _stepHash(key, len: int) -> int:
        return DSAHashTable._fnvHash(key) % (len - 1) + 1

    @staticmethod
    def _packKey(key):
        import struct
        if isinstance(key, int):
            key = struct.pack("i", key)
        elif isinstance(key, str):
            key = key.encode()
        else:
            raise ValueError("Unsupported key type. Use str or int instead.")
        return key

    # Hash function requirements:
    # Fit within the size of the array
    # Fast to compute
    # Repeatable
    # Distribute evenly
    @staticmethod
    def _javaStrHash(key) -> int:
        hash = 0
        for x in DSAHashTable._packKey(key):
            hash = 31 * hash + x
        return hash

    @staticmethod
    def _fnvHash(key) -> int:
        hash = 2166136261
        for x in DSAHashTable._packKey(key):
            # Force overflow
            hash = ((hash * 16777619) % 2**64) ^ x
        return hash

    @staticmethod
    def _nextPrime(x: int) -> int:
        if x < 3:
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


class UnitTestDSAHashTable(unittest.TestCase):
    """
    This class contains unittests for the DSAHashTable class.
    """

    def testNextPrime(self):
        self.assertEqual(2, DSAHashTable._nextPrime(-3))
        self.assertEqual(2, DSAHashTable._nextPrime(-2))
        self.assertEqual(2, DSAHashTable._nextPrime(-1))
        self.assertEqual(2, DSAHashTable._nextPrime(0))
        self.assertEqual(2, DSAHashTable._nextPrime(1))
        self.assertEqual(2, DSAHashTable._nextPrime(2))
        self.assertEqual(3, DSAHashTable._nextPrime(3))
        self.assertEqual(5, DSAHashTable._nextPrime(4))
        self.assertEqual(5, DSAHashTable._nextPrime(5))
        self.assertEqual(163, DSAHashTable._nextPrime(158))

    def TputGetResize(self, *, rf, lb, ub):
        table = DSAHashTable(1, minLoadFactor=lb, maxLoadFactor=ub, resizeFactor=rf)
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

    def Tdelete(self, *, rf, lb, ub):
        table = DSAHashTable(6, minLoadFactor=lb, maxLoadFactor=ub, resizeFactor=rf)
        vals = [0, 1, 2, 3, 4]
        for x in vals:
            table.put(x, x)
        for x in vals:
            self.assertEqual(table.remove(x), x)
            for x in vals[:x + 1]:
                self.assertFalse(table.hasKey(x))
            for x in vals[x + 1:]:
                self.assertEqual(table.get(x), x)

    def testLoadFactor(self):
        table = DSAHashTable(4, maxLoadFactor=1)
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

    def testHashTableParams(self):
        ub = 0.5
        lb = 0
        rf = 2
        self.Tdelete(lb=lb, ub=ub, rf=rf)
        self.TputGetResize(lb=lb, ub=ub, rf=rf)
        ub = 1
        lb = 0
        rf = 1.2
        self.Tdelete(lb=lb, ub=ub, rf=rf)
        self.TputGetResize(lb=lb, ub=ub, rf=rf)
        ub = 1.0
        lb = 0.33
        rf = 1.5
        self.Tdelete(lb=lb, ub=ub, rf=rf)
        self.TputGetResize(lb=lb, ub=ub, rf=rf)

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
            f.seek(0)
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
