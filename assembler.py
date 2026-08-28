class Assembler():
    def __init__(self):

        # Opcodes to be used later
        # Converts the string instruction to binary
        self.OPCODES = {
            'NOP':   0x00,
            'LOAD':  0x01,
            'MOV':   0x02,
            'STORE': 0x03,
            'ADD':   0x04,
            'SUB':   0x05,
            'CMP':   0x06,
            'JMP':   0x07,
            'JZ':    0x08,
            'JNZ':   0x09,
            'AND':   0x0A,
            'OR':    0x0B,
            'XOR':   0x0C,
            'NOT':   0x0D,
            'SHL':   0x0E,
            'SHR':   0x0F,
            'LOAD_MEM': 0x20, 
            'PUSH':   0x21,
            'POP':    0x22,
            'CALL':   0x23,
            'RET':    0x24,
            'HLT':   0xFF, 
        }


        # Same thing but for registers
        self.register_map = {
            'R0': 0x00,
            'R1': 0x01,
            'R2': 0x02,
            'R3': 0x03
        }


    # Converts the source code (string instructions) to bytes
    def assemble(self, source_code):
        # list that will be extended then returned
        program = []

        self.labels = {}

        # New list that contains the source code but splits it by spaces
        # So we get each 3-byte instruction alone
        # This still includes commas and is in the string format
        lines = source_code.strip().split("\n")

        # This is where we find the labels and add them into a dict that contains their address
        address = 0
        for line in lines:
            bare = line.strip()
            if bare.endswith(':'):
                label_name = bare[:-1]
                self.labels[label_name] = (address)
            else:
                address += 3

        
        # Iterates through the list (lines) and extends the program list with the converted version
        for line in lines:
            bare = line.strip()

            # Makes sure we dont count the labels and just skip past them
            if bare.endswith(':'):
                continue

            program.extend(self._parse_line(line))

        # Returns the bytes representation to be used
        return program           




    # Parses the line instruction and converts it to bytes 
    def _parse_line(self, line):
        # Strips all extra whitespace and creates a new list by splitting spaces
        parts = line.strip().split()

        # Gets the opcode instruction, this'll always be the first thing
        opcode = self.OPCODES[parts[0]]

        # Creates variables for the first two arguments
        # We assign these incase we are dealing with operations that dont require the full three bytes
        # Hence they will be 0
        # This is basically padding
        arg1 = 0x00
        arg2 = 0x00


        # If it contains two instructions we update it
        if len(parts) > 1:
            arg1 = self._parse_argument(parts[1])
        # If it contains 3 instructions we update it
        if len(parts) > 2:
            arg2 = self._parse_argument(parts[2])

        # Returns the three byte representation
        return [opcode, arg1, arg2]
    

    # Finds out if its a register, hexadecimal representation of a number, or a plain number
    def _parse_argument(self, arg):
        # Strips any commas, thats just the convention we have going on
        arg = arg.strip(",")

        # Checks if its a register and returns the byte representation
        if arg in self.register_map:
            return self.register_map[arg]
        # Checks if its in the labels dictionary, upon which it returns the address associated with the branching/jumping
        if arg in self.labels:
            return self.labels[arg]
        # This is only here because conventions with looping usually uses hexadecimal
        # Will convert it to int
        if arg.startswith('0x'):
            return int(arg, 16)
        
        # Normal number, returns just the number
        return int(arg)
    
        
            



            
            
        
    

    
