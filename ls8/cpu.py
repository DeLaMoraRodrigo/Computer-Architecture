"""CPU functionality."""

import sys

HLT  = 0b00000001
LDI  = 0b10000010
ST   = 0b10000100
PRN  = 0b01000111
PRA  = 0b01001000
ADD  = 0b10100000
SUB  = 0b10100001
MUL  = 0b10100010
CMP  = 0b10100111
JEQ  = 0b01010101
JNE  = 0b01010110
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
JMP  = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 7
        # self.sp = 0
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[ST] = self.handle_ST
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[PRA] = self.handle_PRA
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[SUB] = self.handle_SUB
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[JMP] = self.handle_JMP

    def ram_read(self, MAR):
        """Reads and returns value stored in address"""
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        """Writes value to address"""
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                # print(line.split("#")[0].strip())
                try:
                    str_line = line.split("#")[0]
                    byte = int(str_line, 2)
                    self.ram[address] = byte
                    address += 1
                except:
                    pass


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            else:
                self.E = 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1
            else:
                self.L = 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1
            else:
                self.G = 0
            print(f"SELF.E: {self.E}\nSELF.L: {self.L}\nSELF.G: {self.G}\n")
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_HLT(self):
        sys.exit()

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_ST(self, operand_a, operand_b):
        self.ram[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self, operand_a):
        print(f"{self.reg[operand_a]} \n")
        self.pc += 2

    def handle_PRA(self, operand_a):
        print(ord(self.reg[operand_a]))
        self.pc += 2

    def handle_ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def handle_SUB(self, operand_a, operand_b):
        self.alu("SUB", operand_a, operand_b)
        self.pc += 3

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def handle_CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    def handle_JEQ(self, operand_a):
        if self.E:
            print("JEQ-ING TO", self.reg[operand_a], "\n")
            self.pc = self.reg[operand_a]
        else:
            print("JEQ NOTHING HAPPENED\n")
            self.pc += 2

    def handle_JNE(self, operand_a):
        if not self.E:
            print("JNE-ING TO", self.reg[operand_a], "\n")
            self.pc = self.reg[operand_a]
        else:
            print("JNE NOTHING HAPPENED\n")
            self.pc += 2

    def handle_PUSH(self, operand_a):
        # print("PUSHING INITIATED")
        # print(f"REGISTER: {self.reg}")
        # print(f"RAM: {self.ram}")
        # print(f"OLD STACK POINTER IN REGISTER: {self.reg[self.sp]}")
        # # self.sp -= 1
        # self.reg[self.sp] -= 1
        # print(f"NEW STACK POINTER IN REGISTER: {self.reg[self.sp]}")
        # value = self.reg[operand_a]
        # pointer = self.reg[self.sp]
        # print(f"PUSHING REGISTER {operand_a} TO RAM AT INDEX {self.reg[self.sp]}")
        # self.ram[pointer] = value
        # print(f"NEW VALUE: {value} IN RAM AT INDEX {self.reg[self.sp]} \n")
        # self.pc += 2

        # self.sp = 7. Increment/Decrement self.reg[self.sp]
        self.reg[self.sp] -= 1
        pointer = self.reg[self.sp]
        value = self.reg[operand_a]
        self.ram[pointer] = value
        self.pc += 2

        # self.sp = 0. Increment/Decrement self.sp
        # self.sp -= 1
        # value = self.reg[operand_a]
        # self.ram[self.sp] = value
        # self.pc += 2

    def handle_POP(self, operand_a):
        # print("POPPING INITIATED")
        # print(f"REGISTER: {self.reg}")
        # print(f"RAM: {self.ram}")
        # pointer = self.reg[self.sp]
        # value = self.ram[pointer]
        # print(f"OLD STACK POINTER IN REGISTER: {self.reg[self.sp]}")
        # print(f"POPPING INDEX {self.reg[self.sp]} IN RAM, INTO REGISTER {operand_a}")
        # self.reg[operand_a] = value
        # print(f"NEW VALUE: {self.reg[operand_a]} AT REGISTER {operand_a}")
        # self.reg[self.sp] += 1
        # # self.sp += 1
        # print(f"NEW STACK POINTER IN REGISTER: {self.reg[self.sp]} \n")
        # self.pc += 2

        # self.sp = 7. Increment/Decrement self.reg[self.sp]
        pointer = self.reg[self.sp]
        value = self.ram[pointer]
        self.reg[operand_a] = value
        self.reg[self.sp] += 1
        self.pc += 2

        # self.sp = 0. Increment/Decrement self.sp
        # value = self.ram[self.sp]
        # self.reg[operand_a] = value
        # self.sp += 1
        # self.pc += 2

    def handle_CALL(self, operand_a):
        return_address = self.pc + 2

        self.reg[self.sp] -= 1
        pointer = self.reg[self.sp]
        self.ram[pointer] = return_address

        subroutine = self.reg[operand_a]
        self.pc = subroutine        

    def handle_RET(self):
        pointer = self.reg[self.sp]
        return_address = self.ram[pointer]
        self.reg[self.sp] += 1

        self.pc = return_address

    def handle_JMP(self, operand_a):
        try:
            self.pc = self.reg[operand_a]
        except:
            print("STACK OVERFLOW")
            sys.exit()

    def run(self):
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                print("HALTING")
                self.branchtable[HLT]()
            elif IR == LDI:
                print(f"LDI REGISTER: {operand_a} VALUE: {operand_b} \n")
                self.branchtable[LDI](operand_a, operand_b)
            elif IR == ST:
                print("ST-ING")
                self.branchtable[ST](operand_a, operand_b)
            elif IR == PRN:
                print("PRINTING")
                self.branchtable[PRN](operand_a)
            elif IR == PRA:
                print("PRANTING")
                self.branchtable[PRA](operand_a)
            elif IR == ADD:
                # print("ADDING")
                self.branchtable[ADD](operand_a, operand_b)
            elif IR == SUB:
                # print("SUBTRACTING")
                self.branchtable[SUB](operand_a, operand_b)
            elif IR == MUL:
                # print("MULTIPLYING")
                self.branchtable[MUL](operand_a, operand_b)
            elif IR == CMP:
                print(f"COMPARING {self.reg[operand_a]} WITH {self.reg[operand_b]}")
                self.branchtable[CMP](operand_a, operand_b)
            elif IR == JEQ:
                print("JEQ-ING")
                self.branchtable[JEQ](operand_a)
            elif IR == JNE:
                print("JNE-ING")
                self.branchtable[JNE](operand_a)
            elif IR == PUSH:
                # print("PUSHING")
                self.branchtable[PUSH](operand_a)
            elif IR == POP:
                # print("POPPING")
                self.branchtable[POP](operand_a)
            elif IR == CALL:
                # print("CALLING")
                self.branchtable[CALL](operand_a)
            elif IR == RET:
                # print("RETURNING")
                self.branchtable[RET]()
            elif IR == JMP:
                print("JUMPING")
                self.branchtable[JMP](operand_a)
            else:
                print(f"INVALID INSTRUCTION {bin(IR)}")
                running = False
            