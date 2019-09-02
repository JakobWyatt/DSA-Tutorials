import unittest
import pickle
from linkedLists import *

class TestDSALinkedList(unittest.TestCase):
    def testConstructorIsEmpty(self):
        ll = DSALinkedList()
        self.assertTrue(ll.isEmpty)

    def testSimpleInsertAndPeek(self):
        ll = DSALinkedList()
        ll.insertFirst("abc")
        self.assertEqual(ll.peekFirst(), "abc")
        self.assertEqual(ll.peekLast(), "abc")
        ll.insertFirst("asd")
        self.assertEqual(ll.peekFirst(), "asd")
        self.assertEqual(ll.peekLast(), "abc")

    def testIter(self):
        ll = DSALinkedList()
        data = ["a", "b", "c", "d"]
        for x in data:
            ll.insertFirst(x)
        
        i = 0
        for x in reversed(ll):
            self.assertEqual(data[i], x)
            i += 1
        for i, elem in enumerate(ll):
            self.assertEqual(data[len(data) - i - 1], elem)

    def testFind(self):
        ll = DSALinkedList()
        ll.insertFirst("abc")
        ll.insertFirst("jkl")
        ll.insertFirst("xyz")
        self.assertTrue(ll.find("jkl"))
        self.assertTrue(ll.find("abc"))
        self.assertTrue(ll.find("xyz"))
        self.assertFalse(ll.find("jkq"))

    def testAdvInsertDelete(self):
        ll = DSALinkedList()
        ll.insertFirst("a")
        ll.insertBefore("b", "a")
        ll.insertLast("c")
        ll.insertBefore("d", "c")
        listState = ["b", "a", "d", "c"]
        for i, elem in enumerate(ll):
            self.assertEqual(listState[i], elem)
        ll.removeFirst()
        ll.remove("d")
        ll.removeLast()
        for i, elem in enumerate(ll):
            self.assertEqual("a", elem)

    def testSerialization(self):
        cucumber = DSALinkedList()
        cucumber.insertFirst("abc")
        cucumber.insertFirst("jkl")
        cucumber.insertFirst("xyz")
        with open("tmp", "wb") as f:
            pickle.dump(cucumber, f)
        with open("tmp", "rb") as f:
            gherkin = pickle.load(f)
        for x1, x2 in zip(gherkin, cucumber):
            self.assertEqual(x1, x2)

if __name__ == "__main__":
    unittest.main()
