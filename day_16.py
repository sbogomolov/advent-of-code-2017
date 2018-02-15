"""
--- Day 16: Permutation Promenade ---
You come upon a very unusual sight; a group of programs here appear to be
dancing.

There are sixteen programs in total, named a through p. They start by standing
in a line: a stands in position 0, b stands in position 1, and so on until p,
which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but maintain
their order otherwise. (For example, s3 on abcde produces cdeab). Exchange,
written xA/B, makes the programs at positions A and B swap places. Partner,
written pA/B, makes the programs named A and B swap places. For example, with
only five programs standing in a line (abcde), they could do the following
dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle
input). In what order are the programs standing after their dance?

Your puzzle answer was namdgkbhifpceloj.

--- Part Two ---
Now that you're starting to get a feel for the dance moves, you turn your
attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs
perform it again and again: including the first dance, a total of one billion
(1000000000) times.

In the example above, their second dance would begin with the order baedc, and
use the same dance moves:

s1, a spin of size 1: cbaed.
x3/4, swapping the last two programs: cbade.
pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

Your puzzle answer was ibmchklnofjpdeag.
"""

from typing import List


class Programs:
    def __init__(self):
        self.programs = list(range(16))
        self.start = 0

    def get_transforms(self) -> List[int]:
        transforms = [0] * len(self.programs)
        for i in range(len(self.programs)):
            transforms[i] = self.programs[(self.start + i) % len(self.programs)]
        return transforms

    def spin(self, count: int) -> None:
        self.start = (self.start + len(self.programs) - count) % len(self.programs)

    def exchange(self, pos1: int, pos2: int) -> None:
        i1 = (self.start + pos1) % len(self.programs)
        i2 = (self.start + pos2) % len(self.programs)
        self.programs[i1], self.programs[i2] = self.programs[i2], self.programs[i1]

    def partner(self, program1: str, program2: str) -> None:
        pos1 = self.programs.index(ord(program1) - 97)
        pos2 = self.programs.index(ord(program2) - 97)
        self.programs[pos1], self.programs[pos2] = self.programs[pos2], self.programs[pos1]


def get_transforms(commands: List[str], include_partner: bool) -> List[int]:
    programs = Programs()

    for command in commands:
        command_type = command[0]
        if command_type == 's':
            programs.spin(int(command[1:]))
        else:
            params = command[1:].split('/')
            if command_type == 'x':
                programs.exchange(int(params[0]), int(params[1]))
            elif command_type == 'p':
                if include_partner:
                    programs.partner(params[0], params[1])
            else:
                raise RuntimeError(f"Unknown command type: {command_type}")

    return programs.get_transforms()


def apply_transforms(programs: List[int], transforms: List[int], repeats: int) -> List[int]:
    programs1 = programs[:]
    programs2 = [0] * len(programs1)
    source = programs1
    destination = programs2
    
    for _ in range(repeats):
        for i in range(len(transforms)):
            destination[i] = source[transforms[i]]

        tmp = source
        source = destination
        destination = tmp

    return source


def transforms_to_string(transforms: List[int]) -> str:
    return ''.join(map(lambda x: chr(x + 97), transforms))


def main():
    with open('day_16_input.txt') as file:
        commands = file.read().strip().split(',')

    programs = list(range(16))

    transforms_with_partner = get_transforms(commands, True)
    transformed_1 = apply_transforms(programs, transforms_with_partner, 1)
    print(transforms_to_string(transformed_1))
    
    # for even number of dances we can skip partner
    # transformations because when we do the second dance,
    # all partner transformations from the first dance
    # are reverted
    transforms = get_transforms(commands, False)
    transformed_1000 = apply_transforms(programs, transforms, 1000)
    transformed_1000000 = apply_transforms(programs, transformed_1000, 1000)
    transformed_1000000000 = apply_transforms(programs, transformed_1000000, 1000)
    print(transforms_to_string(transformed_1000000000))


main()
