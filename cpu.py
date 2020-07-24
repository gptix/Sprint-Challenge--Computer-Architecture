import sys

def number_of_operands (command):
    return (command & 0b11000000) >> 6

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0]*256
        
        # 8 general-purpose 8-bit numeric registers R0-R7.
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.registers = [0] * 8


        # Stack
        stack_pointer_when_empty = 0xF4 
        self.registers[7] = stack_pointer_when_empty


        # Internal registers
        self.PC = 0  # Program Counter, address of currently executing instruction
        self.IR = 0  # Instruction Register, copy of currently executing instruction
        self.MAR = 0 # Memory Address Register, address we're reading or writing
        self.MDR = 0 # Memory Data Register, value to write or value just read
        self.FL = 0  # Flags


    
        # Flags
        # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.


        ## Flags
        # The flags register `FL` holds the current flags status. 
        self.FL = 0
        # These flags change based on the operands given to the `CMP` opcode.

        # The register is made up of 8 bits. If a particular bit is set, that flag is "true".
        # `FL` bits: `00000LGE`
        # * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
        #   zero otherwise.
        # * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
        #   registerB, zero otherwise.
        # * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
        #   otherwise.


        # Operation Codes

        # Used to give readable names to instructions
        # - make sure these match with self.branchtable and have actual functions defined
        HLT =  0x01 # 0b01 0d01

        LDI =  0x82 # 0b10000010 0d130
                    # Set the value of a register to an integer.

                        # Three bytes
                            # byte 0 - instruction
                            # byte 1 - register
                            # byte 2 - "immediate" a number 0 - 255

        PRN =  0x47 # 0b1000111 0d71 
                    # Prints a value.
                        # Two bytes
                            # byte 0 - instruction
                            # byte 1 - value to print

        MUL = 0xa2  # #0b10100010 0d162
                    # Multiplies contents of register A by register B, 
                    # places result in registerA
                        # Three bytes
                            # byte 0 - instruction
                            # byte 1 - registerA number
                            # byte 2 - registerB number 

        POP =  0x46 # 0b01000110 0d70
                        # Pops a value off of the stack and stores in a register.
                        # Two bytes
                            # byte 0 - instruction
                            # byte 1 - number of register to hold value

        PUSH = 0x45 # 0b01000101 0d69
                        # Pushes a value in a register onto the stack.
                        # Two bytes
                            # byte 0 - instruction
                            # byte 1 - number of register holding value

        CALL = 0x50 # 0b01010000
                        # Pushes a return address onto the stack, then chasnges
                        # PC to address of subroutine
                        # Two bytes
                            # byte 0 - instruction
                            # byte 1 - address of subroutine to call

        RET = 0x11 # 0b00010001
                        # Pushes a return address onto the stack, then chasnges
                        # PC to address of subroutine
                        # One byte
                            # byte 0 - instruction

        ADD = 0xA0 # 0b01010000 0d160
                        # Adds contents of two specified registers
                        # zThree bytes
                        # byte 0 - instruction
                        # byte 1 - number of register for a
                        # byte 2 - number of register for b
                        # returns a + b 

        CMP =  0xA7 # 0b10100111
            # Compare the values in two registers.
                # Three bytes
                    # byte 0 - instruction
                    # byte 1 - register a
                    # byte 2 - register b

        JMP =  0x54 # 0b01010100
            # Jump to the address stored in the given register.
                # Two bytes
                    # byte 0 - instruction
                    # byte 1 - register containing jump address

        JEQ =  0x55 # 0b01010101
        # If `equal` flag is set (true), jump to the address stored in the given register.
            # Two bytes
                # byte 0 - instruction
                # byte 1 - register containing jump address

        JNE =  0x56 # 0b01010110
            # If `equal` flag is    NOT    set, jump to the address stored in the given register.
                # Two bytes
                    # byte 0 - instruction
                    # byte 1 - register containing jump address


        # Set up the branch table
        self.branchtable = {}
        self.branchtable[HLT] = self.HLT
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL
        self.branchtable[POP] = self.POP
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET
        self.branchtable[ADD] = self.ADD
        self.branchtable[CMP] = self.CMP
        self.branchtable[JMP] = self.JMP
        self.branchtable[JEQ] = self.JEQ
        self.branchtable[JNE] = self.JNE

    def HLT(self):
        sys.exit(f"Hit an HLT command at line {self.PC}")

    def LDI(self):
        # print(f'LDI value: {self.ram[self.PC+2]} into register {self.ram[self.PC+1]}')
        reg = self.ram[self.PC+1] # register in which to place val
        self.registers[reg] = self.ram[self.PC+2]  # place the val

    def PRN(self):
        # print(f'Print value in register {self.ram[self.PC+1]} to terminal')
        reg = self.ram[self.PC+1] # decide register to examine
        val = self.registers[reg] # get the value
        print(f'{val}')

    def MUL(self):
        registerA = self.ram[self.PC+1] # register to find multiplicand 1
        registerB = self.ram[self.PC+2] # register to find multiplicand 2
        a = self.registers[registerA] # get multiplicand 1
        b = self.registers[registerB] # get multiplicand 2
        result = (a * b) % 256 # multiply and mod 256 to fit 8 bits
        self.registers[registerA] = result # place the result

    def PUSH(self):
        # decrement the stack pointer
        self.registers[7] -= 1
        # get the stack pointer to use
        stack_pos = self.registers[7]
        # get the register number to pull a value from
        reg = self.ram[self.PC+1]
        # get the value to push
        val = self.registers[reg]
        
        # print(f'stack-pointer: {stack_pos} -- register # - {reg} value in that register: {self.registers[reg]}')
        self.ram[stack_pos] = val
        # print(f'updated value on top of stack to {self.ram[stack_pos]}')
        # push value at address pointed to by new SP.
        # Value is in RAM one location after instruction.
        val  = self.ram[self.PC + 1]


    def POP(self):
        # print(f'POP value from stack at {self.registers[7]} into register {self.ram[self.PC+1]}')
        # Determine register to use to store popped value.
        # Register number is in RAM one location after instruction.
        output_reg = self.ram[self.PC+1]
        # print(f'output register = {output_reg}')
        # Retrieve value from RAM and place in specified register.
        self.registers[output_reg] = self.ram[self.registers[7]]
        # Move Stack Pointer after pop.
        self.registers[7] += 1

    def CALL(self):
        """Calls a subroutine by storing a resume address on the stack, then
        # changing PC to the address stored in the register specified by the 
        next 'instruction'. """

        register_with_subroutine_address = self.ram[self.PC+1]
        # print(f'register_with_subroutine_address = {register_with_subroutine_address}')
        subroutine_address = self.registers[register_with_subroutine_address]
        # print(f'subroutine_address= {subroutine_address}')
        
        # Get address to which to return after subroutine call.
        resume_address = self.PC+2
        # print(f'resume_address {resume_address}')
        # input('here')
        # Store the resume address on the stack.
        self.registers[7] -= 1
        stack_pointer = self.registers[7]
        # print(f'stack pointer = {stack_pointer}')
        # push resume address onto stack
        self.ram[stack_pointer] = resume_address
        # input(f'stored on stack = {self.ram[stack_pointer]}')
        # print(f'self.ram[stack_pointer] = {self.ram[stack_pointer]}')
        # input()
        

        # Transfer control to the subroutine. trhe subroutine is responsible
        # for clearing the stack down to the resume address.
        self.PC = subroutine_address - 1  # correct for PC incrementing by run
        
        # print(f'instruction at {subroutine_address}: {self.ram[subroutine_address]} ')

        # offset PC because it will be incremented by dispactch loop,
        # and in this case that would be two (one for operand, one general) 
        # too low.
        self.PC -= 1
    
    
    def RET (self):
        """Returns from a subroutime call.  Pulls resume address off of the stack."""

        # pull resume address off of stack
        resume_address = self.ram[self.registers[7]]
        
        # increment stack pointer after popping
        self.registers[7] += 1

        self.PC = resume_address

        # offset PC because it will be incremented by dispactch loop,
        # and in this case that would be one too low.
        self.PC -= 1

    def ADD (self):
        """Adds numbers held in two registers. Places result in first register."""

        reg_a = self.ram[self.PC + 1]
        # print(f'reg_a = {reg_a}')
        reg_b = self.ram[self.PC + 2]

        a = self.registers[reg_a]
        b = self.registers[reg_b]

        result = a + b
        
        self.registers[reg_a] = result

    def CMP(self):
        """Compares contents ot two registers. Sets flag in FL appropriately."""
        # TODO:
        # refactor to set all three flags to zero, then simplify if-else structure 
        # to return after first success

        # print(f'Print value in register {self.ram[self.PC+1]} to terminal')
        reg_a = self.ram[self.PC+1] # decide register to examine
        # print(f'reg_a == {reg_a}')
        reg_b = self.ram[self.PC+2] # decide register to examine
        # print(f'reg_b == {reg_b}')
        val_a = self.registers[reg_a]
        # print(f'val in reg_a == {self.registers[reg_a]}')
        val_b = self.registers[reg_b]
        # print(f'val in reg_b == {self.registers[reg_b]}')
        # * If they are equal, set the Equal `E` flag to 1, 

        self.FL = 0b00000000


        if val_a ==  val_b:
            self.FL = self.FL = 0b00000001
            # print('set equal flag to 1')
            # print(f'FL register = {self.FL:08b}')
            # print('-----')
    
        elif val_a < val_b:
            self.FL = self.FL = 0b00000100
            # print('set the Less-than `L` flag to 1,')
            # print(f'FL register = {self.FL:08b}')
            # print('-----')
        
        else:
            self.FL = self.FL = 0b00000010
            # print('set the Greater-than `G` flag to 1')
            # print(f'FL register = {self.FL:08b}')
            # print('-----')
            # otherwise set it to 0.

        # print('-----')
        # print(f'FL register = {self.FL:08b}')
        return

    def JMP(self):
        """Reset program counter to the contents of the regiseter
        referenced by the following code line."""
        # print('Got to JMP')

        reg_a = self.ram[self.PC+1] # decide register to examine
        # print(f'reg_a = {reg_a}')
        jump_address = self.registers[reg_a]
        # print(f'jump_address = {jump_address}')
        self.PC = jump_address
        # print(f'self.PC = {self.PC}')
        self.PC -= 2 # compensate for run loop automatically incrementing PC by 1
        # print(f'self.PC after adjusting = {self.PC}')
        return

    def JEQ(self):
        """IFF EQ flag is set, jump to the address contained in the register
        referenced by following code line."""

        FL = self.FL
        # print(f'FL = {FL:3b}')

        EQ_flag = FL & 0b001 # get only the EQ flag (no need to shift)
        # print(f'EQ flag = {EQ_flag}')
        EQ_flag_set = EQ_flag == 1
        # print(f'EQ flag_set = {EQ_flag_set}')
        if EQ_flag_set:
            register_with_jump_address = self.ram[self.PC+1]
            # print(f'register_with_jump_address = {register_with_jump_address}')

            jump_address = self.registers[register_with_jump_address]
            # print(f'jump_address = {jump_address}')

            # print(f'self.PC before assigning jump address= {self.PC}')
            self.PC = jump_address
            # print(f'self.PC after assigning jump address= {self.PC}')
            self.PC -= 2 # compensate for run loop incrementing counter
            # print(f'self.PC adjustung for run loop= {self.PC}')
        # else:
        #     print('Did not Jump.')
        return

    def JNE(self):

        FL = self.FL
        print(f'FL = {FL:3b}')

        EQ_flag = FL & 0b001 # get only the EQ flag (no need to shift)
        print(f'EQ flag = {EQ_flag}')
        EQ_flag_set = EQ_flag == 1
        print(f'EQ flag_set = {EQ_flag_set}')
        if       not       EQ_flag_set:
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
            print('Flag was set (not clear). Did not Jump.')

        return




    
    def ram_read(self, MAR):
        """Accept the address to read and return the value stored there.
         MAR contains the address that is being read or written to.
        """
        return self.ram[MAR]

    def ram_write(self, MDR, val_to_write):
        """Should accept a value to write, and the address to write it to.
        MDR contains the data that was read or the data to write"""
        self.ram[MDR] = val_to_write
        return True

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def load(self, file_name):
        program = []
        try:
            address = 0
            with open(file_name) as f:
                for line in f:
                    # split on any first '#' char
                    line_data = line.split('#')[0]
                    # strip any remaining whitespace
                    line_data = line_data.strip()
                    # ignore empty lines
                    if line_data == '':
                        continue
                    # convert from string, interpret as binary
                    line_data = int(line_data,2)
                    program.append(line_data)                

                    self.ram_write(address, line_data)
                    address +=1


        except FileNotFoundError:
            print(f'The specified file, {file_name}, does not exist.')

    # def run_one_step(self):
    #     PC = self.PC
    #     # self.trace()
    #     command = self.ram[self.PC]
    #     input(f'PC: {PC} - command: b: {command:b} - x: {command:x} - d: {command:d}')
    #     input(f'self.branchtable[command] = {self.branchtable[command]}')
    #     func = self.branchtable[command]
    #     func()
    #     self.PC += number_of_operands(command) # per exact command            
    #     self.PC += 1 # per cycle

    def run(self):
        """Run the CPU."""
        running = True
    
        while running:
            # print(f'self.PC = {self.PC}')
            # self.run_one_step()
            # input(f'At text line {self.PC +1}')
            # print(f'PC = {self.PC}, Instruction = {self.ram[self.PC]:x}')
            # self.trace()
            command = self.ram[self.PC]
            # print(f'command = {command:x}')
            func = self.branchtable[command]
            func()
            self.PC += number_of_operands(command) # per exact command
            self.PC += 1 # per cycle


spanky = CPU()

if len(sys.argv)<2:
    print('Please enter the name of a file containing a program to load, like "$ ls8.py my_program.ls8"')
    sys.exit()

file_name = sys.argv[1]

spanky.load(file_name)

def dump_ram(length=10):
    ctr = 0
    for ctr in range(length):
        print(f'ram row {ctr}: 0x{spanky.ram[ctr]:x}')
        ctr += 1

# dump_ram()

spanky.run()


################## Depracated

    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


        # i = 1
        # for ln in program:
        #     print(f'Text file line number: {i} - {ln:#8b}')
        #     i += 1