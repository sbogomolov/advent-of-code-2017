"""
--- Day 18: Duet ---
You discover a tablet containing some strange assembly code labeled simply
"Duet". Rather than bother the sound card with it, you decide to run the code
yourself. Unfortunately, you don't see any documentation, so you're left to
figure out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are
each named with a single letter and that can each hold a single integer. You
suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what
they do. Here's what you determine:

snd X plays a sound with a frequency equal to the value of X.
set X Y sets register X to the value of Y.
add X Y increases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in
register X by the value of Y.
mod X Y sets register X to the remainder of dividing the value contained in
register X by the value of Y (that is, it sets X to the result of X modulo Y).
rcv X recovers the frequency of the last sound played, but only when the value
of X is not zero. (If it is zero, the command does nothing.)
jgz X Y jumps with an offset of the value of Y, but only if the value of X is
greater than zero. (An offset of 2 skips the next instruction, an offset of -1
jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a
number. The value of a register is the integer it contains; the value of a
number is that number.

After each jump instruction, the program continues with the instruction to which
the jump jumped. After any other instruction, the program continues with the
next instruction. Continuing (or jumping) off either end of the program
terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

The first four instructions set a to 1, add 2 to it, square it, and then set it
to itself modulo 5, resulting in a value of 4.
Then, a sound with frequency 4 (the value of a) is played.
After that, a is set to 0, causing the subsequent rcv and jgz instructions to
both be skipped (rcv because a is 0, and jgz because a is not greater than 0).
Finally, a is set to 1, causing the next jgz instruction to activate, jumping
back two instructions to another jump, which jumps again to the rcv, which
ultimately triggers the recover operation.
At the time the recover operation is executed, the frequency of the last sound
played is 4.

What is the value of the recovered frequency (the value of the most recently
played sound) the first time a rcv instruction is executed with a non-zero
value?

Your puzzle answer was 9423.

--- Part Two ---
As you congratulate yourself for a job well done, you notice that the
documentation has been on the back of the tablet this entire time. While you
actually got most of the instructions correct, there are a few key differences.
This assembly code isn't about sound at all - it's meant to be run twice at the
same time.

Each running copy of the program has its own set of registers and follows the
code independently - in fact, the programs don't even necessarily run at the
same speed. To coordinate, they use the send (snd) and receive (rcv)
instructions:

snd X sends the value of X to the other program. These values wait in a queue
until that program is ready to receive them. Each program has its own message
queue, so a program can never receive a message it sent. rcv X receives the next
value and stores it in register X. If no values are in the queue, the program
waits for a value to be sent to it. Programs do not continue to the next
instruction until they have received a value. Values are received in the order
they are sent. Each program also has its own program ID (one 0 and the other 1);
the register p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2,
0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and
stores it in a, receives another value (both 2) and stores it in b, and then
each receives the program ID of the other program (program 0 receives 1; program
1 receives 0) and stores it in c. Each program now sees a different value in its
own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for
either of them, and they reach a deadlock. When this happens, both programs
terminate.

It should be noted that it would be equally valid for the programs to run at
different speeds; for example, program 0 might have sent all three values and
then stopped at the first rcv before program 1 executed even its first
instruction.

Once both of your programs have terminated (regardless of what caused them to do
so), how many times did program 1 send a value?

Your puzzle answer was 7620.
"""


from abc import ABC, abstractmethod
from typing import Callable, Dict, List
from collections import namedtuple
from queue import Queue


CommandResult = namedtuple('CommandResult', ['shift', 'snd', 'rcv'])
CommandResult.__new__.__defaults__ = (1, None, None)


class Command(ABC):
    @abstractmethod
    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        pass

    def generate_get_value(self, value_expr: str) -> Callable[[], int]:
        try:
            value = int(value_expr)
            return lambda registers: value
        except ValueError:
            if len(value_expr) != 1:
                raise ValueError(f"Wrong registry name: {value_expr}")
            return lambda registers: get_register_value(registers, value_expr)


class Snd(Command):
    def __init__(self, value_expr: str):
        self.get_value = self.generate_get_value(value_expr)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        value = self.get_value(registers)
        queue_out.put(value)
        return CommandResult(snd = value)

class Set(Command):
    def __init__(self, register1: str, value_expr2: str):
        self.register1 = register1
        self.get_value2 = self.generate_get_value(value_expr2)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        set_register_value(registers, self.register1, self.get_value2(registers))
        return CommandResult()


class Add(Command):
    def __init__(self, register1: str, value_expr2: str):
        self.register1 = register1
        self.get_value2 = self.generate_get_value(value_expr2)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        new_value = get_register_value(registers, self.register1) + self.get_value2(registers)
        set_register_value(registers, self.register1, new_value)
        return CommandResult()


class Mul(Command):
    def __init__(self, register1: str, value_expr2: str):
        self.register1 = register1
        self.get_value2 = self.generate_get_value(value_expr2)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        new_value = get_register_value(registers, self.register1) * self.get_value2(registers)
        set_register_value(registers, self.register1, new_value)
        return CommandResult()


class Mod(Command):
    def __init__(self, register1: str, value_expr2: str):
        self.register1 = register1
        self.get_value2 = self.generate_get_value(value_expr2)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        new_value = get_register_value(registers, self.register1) % self.get_value2(registers)
        set_register_value(registers, self.register1, new_value)
        return CommandResult()


class Rcv1(Command):
    def __init__(self, value_expr: str):
        self.get_value = self.generate_get_value(value_expr)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        value = self.get_value(registers)
        return CommandResult(rcv = value if value != 0 else None)


class Rcv2(Command):
    def __init__(self, register: str):
        self.register = register

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        if queue_in.empty():
            return CommandResult(shift = 0)
        else:
            set_register_value(registers, self.register, queue_in.get())
            return CommandResult()


class Jgz(Command):
    def __init__(self, value_expr1: str, value_expr2: str):
        self.get_value1 = self.generate_get_value(value_expr1)
        self.get_value2 = self.generate_get_value(value_expr2)

    def execute(self, registers: List[int], queue_in: Queue, queue_out: Queue) -> CommandResult:
        shift = self.get_value2(registers) if self.get_value1(registers) > 0 else 1
        return CommandResult(shift = shift)


class Program:
    def __init__(self, commands: List[Command], number: int):
        self.commands = commands
        self.queue_out = Queue()
        self.pos = 0
        self.snd_count = 0
        self.registers = [0] * 26
        set_register_value(self.registers, 'p', number)

    def execute(self, queue_in: Queue) -> bool:
        if self.pos < 0 or self.pos >= len(self.commands):
            return False

        res = self.commands[self.pos].execute(self.registers, queue_in, self.queue_out)
        if res.shift == 0:
            return False
        
        self.pos += res.shift
        if res.snd is not None:
            self.snd_count += 1
        return True


def get_register_value(registers: List[int], register: str) -> int:
    return registers[ord(register) - 97]


def set_register_value(registers: List[int], register: str, value: int) -> None:
    registers[ord(register) - 97] = value


def create_command(command_types: Dict[str, type], line: str) -> Command:
    parts = line.rstrip().split()
    command = parts[0]
    args = parts[1:]
    
    if command not in command_types:
        raise RuntimeError(f"Unknown command: {command}")

    return command_types[command](*args)


def main():
    with open('day_18_input.txt') as file:
        lines = file.readlines()
        commands1 = [create_command(CommandTypes1, l) for l in lines]
        commands2 = [create_command(CommandTypes2, l) for l in lines]

    # part 1
    pos = 0
    last_sound = 0
    registers = [0] * 26
    while True:
        res = commands1[pos].execute(registers, Queue(), Queue())
        pos += res.shift
        if res.snd is not None:
            last_sound = res.snd
        if res.rcv:
            print(last_sound)
            break

    # part 2
    program0 = Program(commands2, 0)
    program1 = Program(commands2, 1)
    
    p0_executed = True
    p1_executed = True
    while p0_executed or p1_executed:
        p0_executed = program0.execute(program1.queue_out)
        p1_executed = program1.execute(program0.queue_out)

    print(program1.snd_count)


CommandTypes1 = {
    "snd": Snd,
    "set": Set,
    "add": Add,
    "mul": Mul,
    "mod": Mod,
    "rcv": Rcv1,
    "jgz": Jgz
}

CommandTypes2 = {
    "snd": Snd,
    "set": Set,
    "add": Add,
    "mul": Mul,
    "mod": Mod,
    "rcv": Rcv2,
    "jgz": Jgz
}


main()
