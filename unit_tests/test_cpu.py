import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CPU import CPU

class TestCPU(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()

    def test_load(self):
        program = [0x01, 0x00, 0x05, 0xFF, 0x00, 0x00]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 5)

    def test_mov(self):
        program = [
            0x01, 0x00, 0x0A,  # LOAD R0, 10
            0x02, 0x01, 0x00,  # MOV R1, R0
            0xFF, 0x00, 0x00,
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R1'), 10)

    def test_store_and_load_mem(self):
        program = [
            0x01, 0x00, 0x2A,  # LOAD R0, 42
            0x03, 0x00, 0x80,  # STORE R0, 0x80
            0x01, 0x00, 0x00,  # LOAD R0, 0 (clear R0)
            0x20, 0x00, 0x80,  # LOAD_MEM R0, 0x80
            0xFF, 0x00, 0x00,
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 42)

    def test_add(self):
        program = [
            0x01, 0x00, 0x03,  # LOAD R0, 3
            0x01, 0x01, 0x05,  # LOAD R1, 5
            0x04, 0x00, 0x01,  # ADD R0, R1
            0xFF, 0x00, 0x00,
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 8)

    def test_sub(self):
        program = [
            0x01, 0x00, 0x0A,  # LOAD R0, 10
            0x01, 0x01, 0x03,  # LOAD R1, 3
            0x05, 0x00, 0x01,  # SUB R0, R1
            0xFF, 0x00, 0x00,
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 7)

    def test_jz_taken(self):
        program = [
            0x01, 0x00, 0x05,  # LOAD R0, 5
            0x01, 0x01, 0x05,  # LOAD R1, 5
            0x06, 0x00, 0x01,  # CMP R0, R1
            0x08, 0x0F, 0x00,  # JZ 0x0F
            0x01, 0x02, 0xFF,  # LOAD R2, 255 (should be skipped)
            0xFF, 0x00, 0x00,  # HLT
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R2'), 0)

    def test_jnz_taken(self):
        program = [
            0x01, 0x00, 0x05,  # LOAD R0, 5
            0x01, 0x01, 0x03,  # LOAD R1, 3
            0x06, 0x00, 0x01,  # CMP R0, R1
            0x09, 0x0F, 0x00,  # JNZ 0x0F
            0x01, 0x02, 0xFF,  # LOAD R2, 255 (should be skipped)
            0xFF, 0x00, 0x00,  # HLT
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R2'), 0)

    def test_countdown_loop(self):
        program = [
            0x01, 0x00, 0x05,  # LOAD R0, 5
            0x01, 0x01, 0x01,  # LOAD R1, 1
            0x05, 0x00, 0x01,  # SUB R0, R1
            0x08, 0x0F, 0x00,  # JZ 0x0F
            0x07, 0x06, 0x00,  # JMP 0x06
            0xFF, 0x00, 0x00,  # HLT
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 0)
        self.assertEqual(self.cpu.reg.get_flag('Z'), 1)

    def test_push_pop(self):
        program = [
            0x01, 0x00, 0x2A,  # LOAD R0, 42
            0x21, 0x00, 0x00,  # PUSH R0
            0x01, 0x00, 0x00,  # LOAD R0, 0
            0x22, 0x00, 0x00,  # POP R0
            0xFF, 0x00, 0x00,
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 42)

    def test_call_ret(self):
        program = [
            0x01, 0x00, 0x05,  # LOAD R0, 5
            0x01, 0x01, 0x0A,  # LOAD R1, 10
            0x23, 0x0F, 0x00,  # CALL 0x0F
            0x03, 0x00, 0x80,  # STORE R0, 0x80
            0xFF, 0x00, 0x00,  # HLT
            0x04, 0x00, 0x01,  # ADD R0, R1 (subroutine at 0x0F)
            0x24, 0x00, 0x00,  # RET
        ]
        self.cpu.load_program(program)
        self.cpu.run()
        self.assertEqual(self.cpu.reg.read('R0'), 15)
        self.assertEqual(self.cpu.memory.read(0x80), 15)

if __name__ == '__main__':
    unittest.main()