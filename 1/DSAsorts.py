#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#


def bubbleSort(A):
    isSorted = False
    while not isSorted:
        # This algorithm is in place,
        # restricting our usage of list comprehensions.
        isSorted = True
        for i in range(0, len(A) - 1):
            if A[i] > A[i + 1]:
                isSorted = False
                A[i], A[i + 1] = A[i + 1], A[i]
    return A


def insertionSort(A):
    ...


def selectionSort(A):
    ...


def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm
    """
    ...


def mergeSortRecurse(A, leftIdx, rightIdx):
    ...


def merge(A, leftIdx, midIdx, rightIdx):
    ...


def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...


def quickSortRecurse(A, leftIdx, rightIdx):
    ...


def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...
