from linked_list import Node
from linked_list import LinkedList
import unittest

class TestAppendLL(unittest.TestCase):

    def setUp(self):
        self.ll = LinkedList()

    def test_append_1(self):
        self.assertEqual(self.ll.to_list(), [])        

    def test_append_2(self):
        self.ll.append(2)
        self.assertEqual(self.ll.to_list(), [2])

    def test_append_3(self):
        self.ll.append(1)
        self.ll.append(5)
        self.assertEqual(self.ll.to_list(), [1, 5])

if __name__ == '__main__':
    unittest.main()