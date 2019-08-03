import sys
from typing import Sequence, Callable, Any
from functools import total_ordering
import numpy as np

from DSAsorts import bubbleSort, selectionSort, insertionSort


@total_ordering
class Student():
    def __init__(self, id, name):
        self._id = int(id)
        self._name = str(name)

    def __str__(self):
        return f"{self.id},{self.name}"

    def __lt__(self, other) -> bool:
        return self.id < other.id

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.name == other.name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name


def fileLen(filename: str) -> int:
    i = 0
    with open(filename) as f:
        for x in f:
            i += 1
    return i


def readCsvFile(filename: str, parseLine: Callable[..., Any]) -> Sequence[Any]:
    """Reads a CSV file, calling the given function on each row.

    Args:
        filename : The file to read from.
        parseLine : A callable that inputs all columns of the given csv row.
    Returns:
        List containing all values returned from ``parseLine``.
    """
    arr = np.empty(fileLen(filename), dtype=object)
    with open(filename) as f:
        for i, line in enumerate(f):
            arr[i] = parseLine(*line.rstrip('\n').split(','))
    return arr


def testSortingAlgorithms(unordered: Sequence[Any],
                          key: Callable[[Any], Any]) -> (Sequence[Any], bool):
    """Uses a list of unordered data to test the sorting alorithms
        implemented in ```DSAsorts.py```.

    Args:
        unordered : A list of data to sort. The data must be totally orderable.
        key : A function which, given an element of the list, returns
            an instance of the variable that is used to compare the element.
            This is required because selectionSort, one of the algorithms that
            is tested, is an unstable sort.
            The equality operator is used to ensure the other sorts are stable,
            and the key is used to ensure the unstable sorts
            sort correctly.
            For example, ``Student`` orders by _id,
            so a good key to use would be ``lambda x: x.id``.
    Returns:
        A tuple containing the sorted data, and a boolean value which
        indicates true if all sorting algorithms worked.
    """
    sorted_data = sorted(unordered)
    return sorted_data, \
        (np.array_equal(sorted_data, insertionSort(unordered.copy()))
         # and np.array_equal(sorted_data, bubbleSort(unordered))
         and np.array_equal([key(x) for x in sorted_data],
                            [key(x) for x in selectionSort(unordered.copy())]))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 SortFile.py <read file> <write file>")
    else:
        try:
            students = readCsvFile(sys.argv[1], Student)
            sorted_students, isSorted = \
                testSortingAlgorithms(students, lambda x: x.id)
            if not isSorted:
                print("Sorting algorithms failed.")
            else:
                with open(sys.argv[2], "w") as f:
                    [f.write(f"{x}\n") for x in sorted_students]
        except IOError as ioErr:
            print(f"Error opening file: {ioErr}")
