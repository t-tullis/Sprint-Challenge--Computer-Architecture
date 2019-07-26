import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # hold 256 bytes of memory
        self.ram = [0] * 256
        #8 general-purpose registers.
        self.register = [0] * 8
        #Program Counter
        self.pc = 0
        #Comp flag
        self.FL = None
        self.register[7] = 0xF4

    

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []
        
        with open(sys.argv[1]) as file:
            for line in file:
                instruction = line.split('#', 1)[0]
                if instruction.strip() == '':
                    continue
                
                program.append(int(instruction, 2))
            print(program)
        



        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    # should accept the address to read and return the value stored there.
    def ram_read(self,MAR):
        return self.ram[MAR]
    
    #  should accept a value to write, and the address to write it to.
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        #Compare the values in two registers.
        CMP = 0b10100111
       
        # `FL` bits: `00000LGE`              |LGE   
        # Equal = E 1 otherwise 0 (0000|001)
        # A < B = L 1 otherwise 0 (00000|100)
        # A > B = G 1 otherwise 0 (00000|010)
        if op == CMP:
            if self.register[reg_a] == self.register[reg_b]:
                self.FL = 0b00000001
            elif self.register[reg_a] > self.register[reg_b]:
                self.FL = 0b00000010
            elif self.register[reg_a] < self.register[reg_b]:
                self.FL = 0b00000100
     
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True 

        #Instructions
        #Halt the CPU (and exit the emulator).
        HLT = 0b00000001
        #Set the value of a register to an integer.
        LDI = 0b10000010
        #Print to the console the decimal integer value that is stored in the given register.
        PRN = 0b01000111
        #Compare the values in two registers.
        JEQ = 0b01010101
        #If E flag is clear (false, 0), jump to the address stored in the given register.
        JNE = 0b01010110
        #Jump to the address stored in the given register.
        JMP = 0b01010100

        while running:

            IR = self.ram[self.pc]

            # get next two MDR's from the next two MAR's stored in ram incase instructions need it
            #Argument 1
            operand_a = self.ram_read(self.pc + 1)
            #Argument2
            operand_b = self.ram_read(self.pc + 2)
            
            #checks for Instruction and if AA->B<-CDDDD is a 1 and then shifts over 5bits and performs algorithmic or logical operation
            alu_number = (IR & 0b00100000) >> 5

            if alu_number == 1:
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
            
            elif IR == HLT:
                running = False
                self.pc += 1

            #Else if Instruction Register == LDI Set the value of a register[operand_a] to a operand_b/integer. 
            elif IR == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
    
            #Else if Instruction Register == PRN print to the console the decimal integer value of  register[operand_a]
            elif IR == PRN:
                print(self.register[operand_a])
                self.pc += 2
                
            elif IR == JMP:
                #jump to the address stored in the given register.
                self.pc = self.register[operand_a]

            elif IR == JEQ:
                #checks to see if FLAG is  == 1
                if self.FL == 0b00000001:
                    #then jumps to the address stored in the given register.
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2

            #checks to see if FLAG is  != 1
            elif IR == JNE:
                #then jumps to the address stored in the given register.
                if self.FL != 0b00000001 :
                    self.pc = self.register[operand_a]
                else:
                    self.pc += 2

            
            else:
                print(f"Command {IR} Not Found")
                sys.exit()