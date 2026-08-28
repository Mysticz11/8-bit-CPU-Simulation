# Class just defines the registers and some basic methods

class Registers:

    # Dict for the registers and flags
    # flags have three types so I made it seperate
    def __init__(self):
        # No ACC as the R0 will double as the ACC
        # Check notes for further info
        self.registers = {
        'R0': 0,
        'R1': 0,
        'R2': 0,
        'R3': 0,
        'PC': 0,
        'IR': 0,
        'MDR': 0,
        'MAR': 0,
        'SP': 0xFF,
        }

        self.flags = {
        'Z': 0,
        'C': 0,
        'N': 0
        }

    # Reads the register value at the given register name and returns it
    # Has case handling where if the register name passed isnt in the dict it throws a error
    def read(self, register_name):
        if register_name not in self.registers:
            raise ValueError(f"Unknown register: {register_name}")
        return self.registers[register_name]
    
    # Writes values to the registers
    # Handles cases where the register name passed isn't in the dict
    # Handles cases where the value passed is greater than 255 or smaller than 0
    def write(self, register_name, value):
        if register_name not in self.registers:
            raise ValueError(f"Unknown register: {register_name}")
        
        if not 0 <= value <= 255:
            raise ValueError(f"The value {value} is out of range (0-255) ")
        
        self.registers[register_name] = value

    # Same logic for the flags as the registers, only thing different is the names and error messages
    def get_flag(self, flag_name):
        if flag_name not in self.flags:
            raise ValueError(f"Unknown flag: {flag_name}")
        return self.flags[flag_name]
    
    def set_flag(self, flag_name, value):

        if flag_name not in self.flags:
            raise ValueError(f"Unknown flag: {flag_name}")

        if value not in (0,1):
            raise ValueError(f"Flag {flag_name} is not 0 or 1")

        self.flags[flag_name] = value
    
    # Included for testing, so that I can reset it all to 0 if needed
    # Not really needed
    def reset(self):
        for reg in self.registers:
            self.registers[reg] = 0

        for flg in self.flags:
            self.flags[flg] = 0
    