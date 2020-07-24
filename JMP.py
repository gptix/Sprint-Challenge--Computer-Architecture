# # add to instruction set

### JMP

# `JMP register`

# 

# Set the `PC` to the address stored in the given register.

# Machine code:
# ```
#  00000rrr
# 54 0r
# ```

        JMP =  0xA7 # 0b01010100
                    # Jump to the address stored in the given register.
                        # Two bytes
                            # byte 0 - instruction
                            # byte 1 - register containing jump address


# add to instruction methods
    def JMP(self):

        reg_a = self.ram[self.PC+1] # decide register to examine
        print(f'reg_a = {reg_a}')

        jump_address = self.registers[reg_a]
        print(f'jump_address = {jump_address}')

        self.PC = jump_address
        print(f'self.PC = {self.PC}')

        self.PC -= 3 # compensate for run loop automatically incrementing PC by 1
        print(f'self.PC after adjusting = {self.PC}')

        return

# add to branchtable
self.branchtable[JMP] = self.JMP

