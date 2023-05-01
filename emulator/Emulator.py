class Register:
    def __init__(self, width, value=None):
        self.maximum = (2 ** width) - 1
        self.value = 0
        if value != None:
            self.write(value)

    def __repr__(self):
        return str(self.value)

    def read(self):
        return self.value

    def write(self, value):
        if 0 <= value <= self.maximum:
            self.value = value
        else:
            raise OverflowError()
        
class Counter(Register):
    def increment(self):
        try:
            self.write(self.read() + 1)
        except:
            self.write(0)

class Memory:
    def __init__(self, size, width, values=None):
        self.registers = [Register(width) for _ in range(size)]
        if values != None:
            for index, value in enumerate(values):
                self.write(index, value)

    def __repr__(self):
        return str(self.registers)

    def read(self, index):
        return self.registers[index].read()
    
    def read_all(self):
        return (register.read() for register in self.registers)
    
    def write(self, index, value):
        self.registers[index].write(value)

    def write_all(self, values):
        for register, value in zip(self.registers, values):
            register.write(value)

#0  | no_op             | no operation                      | 1 byte  |
#1  | halt              | halt                              | 1 byte  |
#1  | move              | move                              | 3 bytes | register -> register
#3  | create            | move immediate                    | 3 bytes | immediate -> register
#4  | load              | load                              | 3 bytes | memory -> register
#5  | store             | store                             | 3 bytes | register -> memory
#6  | store_i           | store immediate                   | 3 bytes | immediate -> memory
#7  | jump              | jump                              | 2 bytes | register -> program counter
#8  | jump_i            | jump immediate                    | 2 bytes | immediate -> program counter
#9  | jump_if_equal     | jump if equal                     | 4 bytes | register -> program counter IF register = register
#10 | jump_i_if_equal   | jump immediate if equal           | 4 bytes | immediate -> program counter IF register = register
#11 | jump_if_equal_i   | jump if immediate equal           | 4 bytes | register -> program counter IF immediate = register
#12 | jump_i_if_equal_i | jump immediate if immediate equal | 4 bytes | immediate -> program counter IF immediate = register
#13 | link              | link                              | 1 byte  | link register -> program counter
#14 | not               | not                               | 3 bytes | NOT register -> register
#15 | and               | and                               | 4 bytes | register AND register -> register
#16 | and_i             | and immediate                     | 4 bytes | immediate AND register -> register
#17 | or                | or                                | 4 bytes | register OR register -> register
#18 | or_i              | or immediate                      | 4 bytes | immediate OR register -> register
#19 | xor               | xor                               | 4 bytes | register XOR register -> register
#20 | xor_i             | xor immediate                     | 4 bytes | immediate XOR register -> register
#21 | add               | add                               | 5 byets | register + register -> register
#22 | add_i             | add immediate                     | 5 bytes | immediate + register -> register, register
#23 | sub               | subtract                          | 5 bytes | register - register -> register, register
#24 | sub_i             | subtract immediate                | 5 bytse | immediate - register -> register, register

class Emulator:
    def __init__(self, program):
        self.registers = Memory(8, 8)
        self.random_access_memory = Memory(256, 8)
        self.read_only_memory = Memory(256, 8, values=program)

        self.program_counter = Counter(8)
        self.link_register = Register(8)
        self.halt_flag = False

    def __repr__(self):
        return 'Registers: {}'.format(self.registers)
    
    def fetch(self):
        return self.read_only_memory.read(self.program_counter.read())
    
    def fetch_instruction_arguments(self, number):
        arguments = []
        for _ in range(number):
            self.program_counter.increment()
            arguments.append(self.fetch())
        if number == 1:
            return arguments[0]
        return tuple(arguments)
    
    def no_operation(self):
        self.program_counter.increment()

    def halt(self):
        self.halt_flag = True
        self.program_counter.increment()

    def move(self):
        read_index, write_index = self.fetch_instruction_arguments(2)
        self.registers.write(write_index, self.registers.read(read_index))
        self.program_counter.increment()

    def create(self):
        immediate, index = self.fetch_instruction_arguments(2)
        self.registers.write(index, immediate)
        self.program_counter.increment()

    def load(self):
        read_index, write_index = self.fetch_instruction_arguments(2)
        self.registers.write(write_index, self.random_access_memory.read(read_index))
        self.program_counter.increment()

    def store(self):
        read_index, write_index = self.fetch_instruction_arguments(2)
        self.random_access_memory.write(write_index, self.registers.read(read_index))
        self.program_counter.increment()

    def store_immediate(self):
        immediate, write_index = self.fetch_instruction_arguments(2)
        self.random_access_memory.write(write_index, immediate)
        self.program_counter.increment()

    def jump(self):
        index = self.fetch_instruction_arguments(1)
        self.link_register.write(self.program_counter.read() + 1)
        self.program_counter.write(index)
    
    def jump_immediate(self):
        immediate = self.fetch_instruction_arguments(1)
        self.link_register.write(self.program_counter.read())
        self.program_counter.write(immediate)

    def jump_if_equal(self):
        destination_index, index_a, index_b = self.fetch_instruction_arguments(3)
        self.link_register.write(self.program_counter.read() + 1)
        if self.registers.read(index_a) == self.registers.read(index_b):
            self.program_counter.write(destination_index)
        else:
            self.program_counter.increment()

    def jump_immediate_if_equal(self):
        immediate, index_a, index_b = self.fetch_instruction_arguments(3)
        self.link_register.write(self.program_counter.read() + 1)
        if self.registers.read(index_a) == self.registers.read(index_b):
            self.program_counter.write(immediate)
        else:
            self.program_counter.increment()

    def jump_if_equal_immediate(self):
        destination_index, immediate, index = self.fetch_instruction_arguments(3)
        self.link_register.write(self.program_counter.read() + 1)
        if immediate == self.registers.read(index):
            self.program_counter.write(destination_index)
        else:
            self.program_counter.increment()

    def jump_immediate_if_equal_immediate(self):
        destination_immediate, immediate, index = self.fetch_instruction_arguments(3)
        self.link_register.write(self.program_counter.read() + 1)
        if immediate == self.registers.read(index):
            self.program_counter.write(destination_immediate)
        else:
            self.program_counter.increment()

    def link(self):
        self.program_counter.write(self.link_register.read())

    def not_(self):
        read_index, write_index = self.fetch_instruction_arguments(2)
        self.registers.write(write_index, ~self.registers.read(read_index) & 255)
        self.program_counter.increment()

    def and_(self):
        read_index_1, read_index_2, write_index = self.fetch_instruction_arguments(3)
        self.registers.write(write_index, self.registers.read(read_index_1) & self.registers.read(read_index_2))
        self.program_counter.increment()

    def and_immediate(self):
        pass

    def or_(self):
        pass

    def or_immediate(self):
        pass

    def xor(self):
        pass

    def xor_immediate(self):
        pass

    def run(self):
        while not self.halt_flag:
            instruction = self.fetch()
            [
                self.no_operation,
                self.halt,
                self.move,
                self.create,
                self.load,
                self.store,
                self.store_immediate,
                self.jump,
                self.jump_immediate,
                self.jump_if_equal,
                self.jump_immediate_if_equal,
                self.jump_if_equal_immediate,
                self.jump_immediate_if_equal_immediate,
                self.link,
                self.not_
            ][instruction]()