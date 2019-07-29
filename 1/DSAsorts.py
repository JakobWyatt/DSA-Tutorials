#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#


def bubbleSort(A):
    isSorted = False
    while not isSorted:
        isSorted = True
        for i in range(len(A) - 1):
            if A[i] > A[i + 1]:
                isSorted = False
                A[i], A[i + 1] = A[i + 1], A[i]
    return A


def insertionSort(A):
    for i in range(len(A)):
        while i > 0 and A[i] < A[i - 1]:
            A[i], A[i - 1] = A[i - 1], A[i]
            i -= 1
    return A


def selectionSort(A):
    for i in range(len(A)):
        min_idx = min(enumerate(A[i:]), key=lambda x: x[1])[0] + i
        A[i], A[min_idx] = A[min_idx], A[i]
    return A


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
