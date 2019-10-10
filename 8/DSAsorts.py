#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#
import numpy as np


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
    mergeSortRecurse(A, 0, len(A) - 1)


def mergeSortRecurse(A, left, right):
    if left < right:
        mid = int((left + right) / 2)
        mergeSortRecurse(A, left, mid)
        mergeSortRecurse(A, mid + 1, right)
        merge(A, left, mid, right)


def merge(A, left, mid, right):
    temp = np.zeros(right - left + 1, dtype=object)
    i = left
    j = mid + 1
    k = 0
    while i <= mid and j <= right:
        if A[i] < A[j]:
            temp[k] = A[i]
            i += 1
        else:
            temp[k] = A[j]
            j += 1
        k += 1
    for x in A[i:mid + 1]:
        temp[k] = x
        k += 1
    for x in A[j:right + 1]:
        temp[k] = x
        k += 1
    for i, x in enumerate(temp):
        A[i + left] = x


def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    quickSortRecurse(A, 0, len(A) - 1)


def quickSortRecurse(A, left, right):
    if right > left:
        pivot = findPivot(A, left, right)
        pivot = doPartitioning(A, left, right, pivot)
        quickSortRecurse(A, left, pivot - 1)
        quickSortRecurse(A, pivot + 1, right)


def doPartitioning(A, left, right, pivot):
    A[pivot], A[right] = A[right], A[pivot]

    cur = left
    for i, x in enumerate(A[left:right]):
        if x < A[right]:
            A[i + left], A[cur] = A[cur], A[i + left]
            cur += 1
    A[cur], A[right] = A[right], A[cur]
    return cur


def findPivot(A, left, right):
    return (left + right) // 2

if __name__ == "__main__":
    A = [4, 3, 2, 1, 5]
    quickSort(A)
    print(A)
