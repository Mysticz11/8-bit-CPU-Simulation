import argparse
from CPU import CPU
from assembler import Assembler

# Lets us chagne the program run from the terminal insteaf of changing the file path each time
# RUN WITH python main.py programs/program_name.asm --debug
# Remove the --debug if you dont want it.

# This is the parser object
parser = argparse.ArgumentParser(description="8-bit CPU Simulator")
# Tells the parse that the user needs to give a filename
parser.add_argument("file", help="Path to .asm file")
# - - means the debug optional, if not provided we assume true
parser.add_argument("--debug", action="store_true", help="Run in debug mode")
# this reads the stuff written in the terminal
args = parser.parse_args()

assemble = Assembler()
cpu = CPU()

with open(args.file, "r") as file:
        source = file.read()

program = assemble.assemble(source)

cpu.load_program(program)

# debug_bool = input("Would you like to use the debugger?\nType Y for yes and N for no: ")

# if debug_bool == 'Y':
#     debug_bool = True
# else:
#     debug_bool = False

cpu.run(debug = args.debug)

print(f"R0: {cpu.reg.read('R0')}")  
print(f"R1: {cpu.reg.read('R1')}")  
print(f"Z flag: {cpu.reg.get_flag('Z')}")  
print(f"C flag: {cpu.reg.get_flag('C')}")  
print(f"N flag: {cpu.reg.get_flag('N')}")  

# print(cpu.memory)