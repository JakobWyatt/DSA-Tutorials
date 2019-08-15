import unittest
from typing import Type
from DSAStack import DSAStack
from DSAQueue import DSAShufflingQueue, DSACircularQueue, DSAQueue

class TestDSAADT(unittest.TestCase):
    def testDSAStack(self):
        stack = DSAStack(5)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.push(5)
        self.assertTrue(stack.isFull())
        self.assertEqual(stack.top(), 5)
        self.assertEqual(stack.pop(), 5)
        self.assertEqual(stack.count(), 4)
        self.assertEqual(stack.pop(), 4)
        stack.push(100)
        self.assertEqual(stack.pop(), 100)
        while not stack.isEmpty():
            stack.pop()
        self.assertTrue(stack.isEmpty())
    
    def testDSACircularQueue(self):
        testDSAQueue(self, DSACircularQueue)

    def testDSAShufflingQueue(self):
        testDSAQueue(self, DSAShufflingQueue)

def testDSAQueue(testCase : unittest.TestCase, cls : Type[DSAQueue]):
    queue = cls(5)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.enqueue(4)
    queue.enqueue(5)
    testCase.assertTrue(queue.isFull())
    testCase.assertEqual(queue.dequeue(), 1)
    testCase.assertEqual(queue.peek(), 2)
    testCase.assertEqual(queue.count(), 4)
    testCase.assertEqual(queue.dequeue(), 2)
    queue.enqueue(100)
    while queue.count() > 1:
        queue.dequeue()
    testCase.assertEqual(queue.dequeue(), 100)
    testCase.assertTrue(queue.isEmpty())

if __name__ == '__main__':
    unittest.main()