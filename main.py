from CPU import CPU


cpu = CPU()

# Program: LOAD R0, 5 → LOAD R1, 3 → ADD R0, R1 → HLT
program = [
    0x01, 0x00, 0x09,  # LOAD R0
    0x01, 0x01, 0x07,  # LOAD R1
    0x03, 0x00, 0x80,  # Does stuff with R0 & R1
    0xFF, 0x00, 0x00,  # HLT
]

cpu.load_program(program)
cpu.run()

print(f"R0: {cpu.reg.read('R0')}")  
print(f"R1: {cpu.reg.read('R1')}")  
print(cpu.memory)


