# # add to instruction set

        JEQ =  0x55 # 0b01010101
                    # If `equal` flag is set (true), jump to the address stored in the given register.
                        # Two bytes
                            # byte 0 - instruction
                            # byte 1 - register containing jump address


# add to instruction methods
    def JEQ(self):

        FL = self.FL
        print(f'FL = {FL:3b}')

        EQ_flag = FL & 0b001 # get only the EQ flag (no need to shift)
        print(f'EQ flag = {EQ_flag')
        EQ_flag_set = EQ_flag == 1
        print(f'EQ flag_set = {EQ_flag_set}')
        if EQ_flag_set:
            register_with_jump_address = self.ram[self.PC+1]
            print(f'register_with_jump_address = {register_with_jump_address}')

            jump_address = self.registers[register_with_jump_address]
            print(f'jump_address = {jump_address}')

            print(f'self.PC before assigning jump address= {self.PC}')
            self.PC = jump_address
            print(f'self.PC after assigning jump address= {self.PC}')
            self.PC -= 2 # compensate for run loop incrementing counter
            print(f'self.PC adjustung for run loop= {self.PC}')

        else:
            print('Did not Jump.')

        return

# add to branchtable
self.branchtable[JEQ] = self.JEQ

