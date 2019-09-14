import unittest
from typing import Type
from DSAListStack import DSAListStack
from DSAListQueue import DSAListQueue

class TestDSAADT(unittest.TestCase):
    def testDSAListStack(self):
        stack = DSAListStack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.push(5)
        self.assertEqual(stack.top(), 5)
        self.assertEqual(stack.pop(), 5)
        self.assertEqual(stack.pop(), 4)
        stack.push(100)
        self.assertEqual(stack.pop(), 100)
        while not stack.isEmpty():
            stack.pop()
        self.assertTrue(stack.isEmpty())

    def testDSAListQueue(self):
        queue = DSAListQueue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.peek(), 2)
        self.assertEqual(queue.dequeue(), 2)
        queue.enqueue(100)
        queue.dequeue()
        queue.dequeue()
        queue.dequeue()
        self.assertEqual(queue.dequeue(), 100)
        self.assertTrue(queue.isEmpty())

if __name__ == '__main__':
    unittest.main()