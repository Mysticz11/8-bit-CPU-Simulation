from Registers import Registers
from Memory import Memory
from ALU import ALU

class CPU:
    def __init__(self):
        # This is the instruction set
        # Each hexa corresponds to a action
    self.OPCODES = {
        0x00: 'NOP',
        0x01: 'LOAD',
        0x02: 'MOV',
        0x03: 'STORE',
        0x04: 'ADD',
        0x05: 'SUB',
        0x06: 'CMP',
        0x07: 'JMP',
        0x08: 'JZ',
        0x09: 'JNZ',
        0x0A: 'AND',
        0x0B: 'OR',
        0x0C: 'XOR',
        0x0D: 'NOT',
        0x0E: 'SHL',
        0x0F: 'SHR',
        0x20: 'LOAD_MEM',
        0x21: 'PUSH',
        0x22: 'POP',
        0x23: 'CALL',
        0x24: 'RET',
        0xFF: 'HLT',
    }
        

        # Used for the HLT
        self.running = True

        # Initializing CLasses
        self.reg = Registers()
        self.memory = Memory()
        
        self.alu = ALU(self.reg)

    # Loads programs, self explantiory
    def load_program(self, program):
        self.memory.load_program(program)
        
    # Three step loop: fetch - decode - execute
    
    # First step
    def fetch(self):
        # Read the PC and store it for later use (incrementing)
        pc = self.reg.read("PC")

        # We use a fixed three-bit program
        # So read at the PC then + 1 and + 2
        b1 = self.memory.read(pc)
        b2 = self.memory.read(pc+1)
        b3 = self.memory.read(pc+2)

        # the IR cant store more than one
        # Either way though the first bit read IS the instruction
        # So thats what we store 
        self.reg.write("IR", b1)

        # create variables for arguments
        # Used in other methods
        self.arg1 = b2
        self.arg2 = b3

        # Increment the PC by 3 (fixed three-bit we don't care if it actually needs less than 3)
        self.reg.write("PC", pc + 3)


    # Second step: Decode
    def decode(self):
        # Read the instruction (opcode)
        # Located at the IR (refer to notes for definitions)
        opcode = self.reg.read("IR")

        # Exception handling, makes sure its actually located in the instruction set
        if opcode not in self.OPCODES:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        # Returns the instruction by using the opcode array at the beggining
        return self.OPCODES[opcode]

    def execute(self):
        
        # Get the instruction
        instruction = self.decode()

        # Used for the debugger
        self.last_instruction = instruction

        # Fat if-else with all the instructions
        # There has to be something else thats more efficient than this, but our instruction set is small enough.

        # NOP does nothing so just pass
        if instruction == 'NOP':
            pass 

        # LOAD gets data from memory and stores it in some register
        # So the first argument is what register it wants, the second is the info it wants to write
        elif instruction == 'LOAD':
            self.reg.write(f"R{self.arg1}", self.arg2)      

        # MOV copies data between registers 
        # So we read the value at the second argument (A register) and write it to whatever register the first argument wants 
        elif instruction == 'MOV':
            value = self.reg.read(f"R{self.arg2}")
            self.reg.write(f"R{self.arg1}", value)

        # Read the value of the first argument (register) and then store it in the second argument (location in memory)
        elif instruction == 'STORE':
            value = self.reg.read(f"R{self.arg1}")
            self.memory.write(self.arg2, value)
        
        # ADD is a arithmetic operation
        # Read the values at both registers, then uses the ALU class to do the adding
        # We store all results in R0, so write it there 
        elif instruction == 'ADD':
            value1 = self.reg.read(f"R{self.arg1}")
            value2 = self.reg.read(f"R{self.arg2}")
            result = self.alu.add(value1, value2)
            self.reg.write('R0', result)
        
        # Same thing but we use the subtract method in ALU
        elif instruction == 'SUB':
            value1 = self.reg.read(f"R{self.arg1}")
            value2 = self.reg.read(f"R{self.arg2}")
            result = self.alu.sub(value1, value2)
            self.reg.write('R0', result)

        # Same thing as SUB but this time we use the CMP method (doesn't return) and don't store anything
        elif instruction == 'CMP':
            value1 = self.reg.read(f"R{self.arg1}")
            value2 = self.reg.read(f"R{self.arg2}")
            self.alu.cmp(value1, value2)

        # Moves the PC to a new location
        elif instruction == 'JMP':
            self.reg.write('PC', self.arg1)

        # Moves the PC to a new location if the Zero flag is set
        elif instruction == 'JZ':
            if self.reg.get_flag('Z') == 1:
                self.reg.write('PC', self.arg1)

        # Moves the PC to a new location if the PC is NOT set
        elif instruction == 'JNZ':
            if self.reg.get_flag('Z') != 1:
                self.reg.write('PC', self.arg1)

        elif instruction == 'AND':
            value1 = self.reg.read(f"R{self.arg1}")
            value2 = self.reg.read(f"R{self.arg2}")
            result = self.alu.and_op(value1, value2)
            self.reg.write('R0', result)

        elif instruction == 'OR':
            value1 = self.reg.read(f"R{self.arg1}")
            value2 = self.reg.read(f"R{self.arg2}")
            result = self.alu.or_op(value1, value2)
            self.reg.write('R0', result)

        elif instruction == 'XOR':
            value1 = self.reg.read(f"R{self.arg1}")
            value2 = self.reg.read(f"R{self.arg2}")
            result = self.alu.xor_op(value1, value2)
            self.reg.write('R0', result)

        elif instruction == 'NOT':
            value = self.reg.read(f"R{self.arg1}")
            result = self.alu.not_op(value)
            self.reg.write('R0', result)

        elif instruction == 'SHL':
            value = self.reg.read(f"R{self.arg1}")
            result = self.alu.shiftl(value)
            self.reg.write('R0', result)

        elif instruction == 'SHR':
            value = self.reg.read(f"R{self.arg1}")
            result = self.alu.shiftr(value)
            self.reg.write('R0', result)

        elif instruction == 'LOAD_MEM':
            value = self.memory.read(self.arg2)
            self.reg.write(f"R{self.arg1}", value)
        
        elif instruction == 'PUSH':
            value = self.reg.read(f"R{self.arg1}")
            sp = self.reg.read('SP')        
            self.memory.write(sp, value)
            self.reg.write('SP', sp - 1)
        
        elif instruction == 'POP':
            sp = self.reg.read('SP')  

            if sp < 0xFF:
                sp += 1
                value = self.memory.read(sp)
                self.reg.write(f"R{self.arg1}", value)
                self.reg.write('SP', sp)
        
        elif instruction == 'CALL':
            pc = self.reg.read('PC')
            sp = self.reg.read('SP')    
            self.memory.write(sp, pc)
            self.reg.write('PC', self.arg1)
            self.reg.write('SP', sp - 1)
            
        elif instruction == 'RET':
            sp = self.reg.read('SP') + 1
            new_pc = self.memory.read(sp)
            self.reg.write('PC', new_pc)
            self.reg.write('SP', sp)

        # Stops the program
        elif instruction == "HLT":
            self.running = False

    # The running loop
    # We dont see decode because execute will call it by defualt
    def run(self, debug = False):
        while self.running:
            self.fetch()
            self.execute()
            if debug:
                print(self.__str__())
                command = input("Enter = next, r = run to the end, q = quit: ")
                if command == 'q':
                    break
                elif command == 'r':
                    debug = False
        
    def __str__(self):
        build = "──────────────────────────────────\n"

        build += f"Instruction: {self.last_instruction} {self.arg1} {self.arg2}\n"
        build += f"R0 = {self.reg.read('R0')} R1 = {self.reg.read('R1')} R2 = {self.reg.read('R2')} R3 = {self.reg.read('R3')}\n"
        build += f"Flags: Z = {self.reg.get_flag('Z')}  C = {self.reg.get_flag('C')}  N = {self.reg.get_flag('N')}\n"
        
        pc = self.reg.read('PC')
        next_opcode = self.memory.read(pc)

        if next_opcode in self.OPCODES:
            next_arg1 = self.memory.read(pc + 1)
            next_arg2 = self.memory.read(pc + 2)

            build += f"Next: {self.OPCODES[next_opcode]} {next_arg1} {next_arg2}"
        else:
            build += f"Next opcode: {next_opcode} is not a recognized instruction"

        build += "\n──────────────────────────────────"


        return build

                
                
                
            

