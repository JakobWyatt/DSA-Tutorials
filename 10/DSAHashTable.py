import unittest
from enum import Enum
import numpy as np
from math import ceil
import copy

class DSAHashTable:
    """
    This class is an impementation of an automatically resizing hash table,
    with O(1) amortized insert, delete, and find operations.
    """

    # autoResize allows creation of a "dumb" non-resizing table
    def __init__(self):
        self._dict = {}

    def put(self, key, value: object) -> None:
        self._dict[key] = value

    def get(self, key) -> object:
        return self._dict[key]

    def hasKey(self, key) -> bool:
        return key in self._dict

    def remove(self, key) -> object:
        return self._dict.pop(key, None)

    def export(self) -> str:
        return "".join([f"{k},{v}\n" for k, v in self])

    @staticmethod
    def read(string: str) -> 'DSAHashTable':
        lines = string.split('\n')[:-1]
        table = DSAHashTable()
        for x in lines:
            key, value = x.split(',')
            if not table.hasKey(key):
                table.put(key, value)
        return table

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return self._dict.items().__iter__()


class UnitTestDSAHashTable(unittest.TestCase):
    """
    This class contains unittests for the DSAHashTable class.
    """
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
        tableCopy = copy.deepcopy(table)
        for k, v in tableCopy:
            self.assertEqual(table.remove(k), table2.remove(k))
        self.assertEqual(len(table2), 0)


if __name__ == "__main__":
    unittest.main()
