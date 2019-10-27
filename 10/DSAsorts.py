#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#
import numpy as np
import math

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
    insertion(A, 0, len(A))


def insertion(A, left, right):
    for i in range(left, right):
        while i > left and A[i] < A[i - 1]:
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


def quickSort(A, *, pivotFunc, threeWay = False):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    if threeWay:
        quickSort3wayRecurse(A, 0, len(A) - 1, pivotFunc)
    else:
        quickSortRecurse(A, 0, len(A) - 1, pivotFunc)


def quickSortRecurse(A, left, right, pivotFunc):
    if right > left:
        pivot = pivotFunc(A, left, right)
        pivot = doPartitioning(A, left, right, pivot)
        quickSortRecurse(A, left, pivot - 1, pivotFunc)
        quickSortRecurse(A, pivot + 1, right, pivotFunc)


def quickSort3wayRecurse(A, left, right, pivotFunc):
    if right > left:
        pivot = pivotFunc(A, left, right)
        i, j = doPartitioning3way(A, left, right, pivot)
        quickSort3wayRecurse(A, left, i - 1, pivotFunc)
        quickSort3wayRecurse(A, j + 1, right, pivotFunc)


def doPartitioning3way(A, left, right, pivot):
    i = left
    j = right
    k = left
    pivotVal = A[pivot]
    while k <= j:
        if A[k] < pivotVal:
            A[k], A[i] = A[i], A[k]
            i += 1
            k += 1
        elif A[k] > pivotVal:
            A[k], A[j] = A[j], A[k]
            j -= 1
        else:
            k += 1
    return i, j


def doPartitioning(A, left, right, pivot):
    A[pivot], A[right] = A[right], A[pivot]

    cur = left
    for i, x in enumerate(A[left:right]):
        if x < A[right]:
            A[i + left], A[cur] = A[cur], A[i + left]
            cur += 1
    A[cur], A[right] = A[right], A[cur]
    return cur


def leftPivot(A, left, right):
    return left


def medianOfThreePivot(A, left, right):
    # Find the median of the left, mid, and right values
    mid = (left + right) // 2
    if A[left] <= A[mid] and A[mid] <= A[right] or A[right] <= A[mid] and A[mid] <= A[left]:
        pivot = mid
    elif A[mid] <= A[left] and A[left] <= A[right] or A[right] <= A[left] and A[left] <= A[mid]:
        pivot = left
    else:
        pivot = right
    return pivot


def shellSort(A):
    shellSortGap(A, 5)
    shellSortGap(A, 3)
    shellSortGap(A, 1)


def shellSortGap(A, gap):
    if gap == 1:
        insertionSort(A)
    else:
        for i in range(0, len(A) // gap):
            insertion(A, i, i + gap)
        insertion(A, len(A) // gap * gap, len(A))


def countingSort(A):
    # A must be an integer array
    counting(A, min(A), max(A) + 1)


def counting(A, min, max, transform=lambda x: x):
    count = np.zeros(max - min, dtype=int)
    # Count the elements in the range
    for x in A:
        print(transform(x))
        count[transform(x) - min] += 1
    # Slot into result
    i = 0
    for j, x in enumerate(count):
        for _ in range(x):
            A[i] = j + min
            i += 1


def radixLsdSort(A):
    # A must be an integer array
    base = 10
    places = math.floor(math.log(max(A)) / math.log(base)) + 1
    for x in range(places):
        counting(A, 0, base, lambda a: a // (base ** x) % base)
