from CPU import CPU
from assembler import Assembler

assemble = Assembler()
cpu = CPU()

# Countdown from 5 to 0
source = """
LOAD R0, 5
LOAD R1, 1
loop:
SUB R0, R1
JZ end
JMP loop
end:
HLT
"""
program = assemble.assemble(source)

cpu.load_program(program)

debug_bool = input("Would you like to use the debugger?\nType Y for yes and N for no: ")

if debug_bool == 'Y':
    debug_bool = True
else:
    debug_bool = False

cpu.run(debug=debug_bool)

print(f"R0: {cpu.reg.read('R0')}")  # Should be 0
print(f"R1: {cpu.reg.read('R1')}")  # Should be 1
print(f"Z flag: {cpu.reg.get_flag('Z')}")  # Should be 1 (last SUB resulted in 0)
print(f"C flag: {cpu.reg.get_flag('C')}")  # Should be 0
print(f"N flag: {cpu.reg.get_flag('N')}")  # Should be 0

# print(cpu.memory)