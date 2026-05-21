
# This class defines basic ALU operations. 
# Keep in mind that the ALU will ONLY do basic arithmetic.
# So here we aren't reading from registers or anything, reading from registers is through the parameters passed


class ALU():

    # We'll pass the registers as a parameter once this is actually used
    def __init__(self, registers):
        self.registers = registers


    # For all arithmetic we needed two types of sums
    # The raw_result is simply just adding the two numbers
    # The result is when we mask it to 8-bit, meaning that if we overflow it takes the first 8-bits and ignores the rest
    # Basically overflow

    # Adds two values, returns it and updates flags 
    def add(self, V1, V2):
        raw_result = V1 + V2
        result = raw_result & 0xFF
        
        self._update_flags(result,raw_result)

        return result

    # Subtracts two values, returns it and updates flags
    def sub(self, V1, V2):
        raw_result = V1 - V2
        result = raw_result & 0xFF

        self._update_flags(result, raw_result)

        return result
    
    # Subtracts two values, but ONLY updates flags
    def cmp(self, V1, V2):
        raw_result = V1 - V2
        result = raw_result & 0xFF

        self._update_flags(result, raw_result)

    # Helper method since I don't want to retype this everywhere
    # underscore at the beggining of the name is apparantly naming conventions
    def _update_flags(self, result, raw_result):
        # If zero set zero flag, otherwise clear it
        if result == 0:
            self.registers.set_flag('Z',1)
        else:
            self.registers.set_flag('Z',0)

        # If overflow or underflow set carry flag, else clear
        if raw_result > 255 or raw_result < 0:
            self.registers.set_flag('C',1)
        else:
            self.registers.set_flag('C',0)

        # Check the 7th bit to see if its negative, if so set Negative flag, else clear it.
        if result & 0x80:
            self.registers.set_flag('N',1)
        else:
            self.registers.set_flag('N',0)



    