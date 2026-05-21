
#This class defines the memory and some general methods


class Memory:
    # Initialize the memory array with max size 256
    def __init__(self):
        self.memory_array = [0] * 256

    # Method reads the address given and returns the value
    # First needs to check if it wthin the actual array though
    def read(self, address):
        if not 0 <= address <= 255:
            raise ValueError(f"Address {address} out of range (0-255)")

        return self.memory_array[address]
    
    # Method writes values to addresses
    # Same thing, needs to check if its within the actual array
    # It also needs to check if the value stored is 255 or lower
    # This is because i'm modelling a 8-bit CPU, we can technically store larger values
    def write(self, address, value):
        if not 0 <= address <= 255:
            raise ValueError(f"Address {address} out of range (0-255)")        

        if not 0 <= value <= 255:
            raise ValueError(f"Value {value} out of range (0-255)")

        self.memory_array[address] = value

    # Takes the list of bytes (the program) and loads it into memroy 
    # Starts at the starting_address 
    # This is the booting up part (check notes), we're basically stuffing the instructions into the RAM before the CPU starts
    def load_program(self, program, starting_address = 0x00):
        if starting_address + len(program) > 256:
            raise ValueError(f"Program of size {len(program)} is larger that the allocated memory starting at address {starting_address}")

        for i in range(len(program)):
            self.memory_array[starting_address + i] = program[i]


    def __str__(self):
        result = "Memory Contents:\n"
        for i in range(0, 256, 16):
            row = self.memory_array[i:i+16]
            hex_values = ' '.join(f'{val:02X}' for val in row)
            result += f"0x{i:02X}: {hex_values}\n"
        return result

