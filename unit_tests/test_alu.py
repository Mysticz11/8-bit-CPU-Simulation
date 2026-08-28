import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ALU import ALU
from Registers import Registers


class TestALU(unittest.TestCase):
    def setUp(self):
        self.reg = Registers()
        self.alu = ALU(self.reg)

    def test_add_basic(self):
        result = self.alu.add(3, 5)
        self.assertEqual(result, 8)

    def test_add_overflow(self):
        result = self.alu.add(200,100)
        self.assertEqual(result, 44)
        self.assertEqual(self.reg.get_flag('C'), 1)

    def test_sub_basic(self):
        result = self.alu.sub(10, 5)
        self.assertEqual(result, 5)

    def test_sub_underflow(self):
        result = self.alu.sub(50, 100)
        self.assertEqual(result, 206)
        self.assertEqual(self.reg.get_flag('N'), 1)


    def test_cmp(self):
        self.alu.cmp(50, 50)
        self.assertEqual(self.reg.get_flag('Z'), 1)

        self.alu.cmp(5,10)
        self.assertEqual(self.reg.get_flag('N'), 1)

    
    if __name__ == '__main__':
        unittest.main()