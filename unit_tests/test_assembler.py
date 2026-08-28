import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from assembler import Assembler

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.asm = Assembler()

    def test_basic_instruction(self):
        result = self.asm.assemble("LOAD R0, 5")
        self.assertEqual(result, [0x01, 0x00, 0x05])

    def test_no_args(self):
        result = self.asm.assemble("HLT")
        self.assertEqual(result, [0xFF, 0x00, 0x00])

    def test_multiple_instructions(self):
        source = "LOAD R0, 5\nLOAD R1, 3\nHLT"
        result = self.asm.assemble(source)
        self.assertEqual(result, [0x01, 0x00, 0x05, 0x01, 0x01, 0x03, 0xFF, 0x00, 0x00])

    def test_label_resolution(self):
        source = "JMP end\nNOP\nend:\nHLT"
        result = self.asm.assemble(source)
        self.assertEqual(result, [0x07, 0x06, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00])

    def test_empty_lines_skipped(self):
        source = "LOAD R0, 5\n\nHLT"
        result = self.asm.assemble(source)
        self.assertEqual(result, [0x01, 0x00, 0x05, 0xFF, 0x00, 0x00])

    def test_hex_argument(self):
        source = "STORE R0, 0x80"
        result = self.asm.assemble(source)
        self.assertEqual(result, [0x03, 0x00, 0x80])

    def test_all_registers(self):
        source = "MOV R3, R2"
        result = self.asm.assemble(source)
        self.assertEqual(result, [0x02, 0x03, 0x02])

    def test_label_backward_reference(self):
        source = "loop:\nNOP\nJMP loop"
        result = self.asm.assemble(source)
        self.assertEqual(result, [0x00, 0x00, 0x00, 0x07, 0x00, 0x00])

if __name__ == '__main__':
    unittest.main()