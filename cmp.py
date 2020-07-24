
#####
# THis is old code.  cpu.py has refactored code
# 
# 
# # add to instruction set

        CMP =  0xA7 # 0b10100111
                    # Compare the values in two registers.
                        # Three bytes
                            # byte 0 - instruction
                            # byte 1 - register a
                            # byte 2 - register b

# add to instruction methods
    def CMP(self):
        # TODO:
        # refactor to set all three flags to zero, then simplify if-else structure 
        # to return after first success

        # print(f'Print value in register {self.ram[self.PC+1]} to terminal')
        reg_a = self.ram[self.PC+1] # decide register to examine
        reg_b = self.ram[self.PC+2] # decide register to examine
        val_a = self.ram[reg_a]
        val_b = self.ram[reg_b]
        # * If they are equal, set the Equal `E` flag to 1, 

        if val_a ==  val_b:
            print('set equal flag to 1')
        else:
            # otherwise set it to 0.
            print('set equal flag to 0')
        # * If registerA is less than registerB, set the Less-than `L` flag to 1,
        if val_a < val_b:
            print('set the Less-than `L` flag to 1,')
            # otherwise set it to 0.
            print('set the Less-than `L` flag to 0')
        # * If registerA is greater than registerB, set the Greater-than `G` flag
        if val_a > val_b:
            print('et the Greater-than `G` flag to 1')
            # otherwise set it to 0.
            print('set the Greater-than `G` flag to 0')
        return

# add to branchtable
self.branchtable[CMP] = self.CMP

