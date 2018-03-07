"""
--- Day 21: Fractal Art ---
You find a program trying to generate some art. It uses a strange process that
involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on
(#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have
a size of 3.

Then, the program repeats the following process:

If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and
convert each 2x2 square into a 3x3 square by following the corresponding
enhancement rule. Otherwise, the size is evenly divisible by 3; break the pixels
up into 3x3 squares, and convert each 3x3 square into a 4x4 square by following
the corresponding enhancement rule. Because each square of pixels is replaced by
a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however,
it seems to be missing rules. The artist explains that sometimes, one must
rotate or flip the input pattern to find a match. (Never rotate or flip the
output pattern, though.) Each pattern is written concisely: rows are listed as
single units, ordered top-down, and separated by slashes. For example, the
following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For
example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It
divides evenly into a single square; the square matches the second rule, which
produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is
used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of
which require some flipping and rotation to line up with the rule. The output
for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

Your puzzle answer was 147.

--- Part Two ---
How many pixels stay on after 18 iterations?

Your puzzle answer was 1936582.
"""


import math
from typing import List, Dict


class Pattern:
    def __init__(self, pattern: List[bool]):
        self.size = int(math.sqrt(len(pattern)))
        self.pattern = pattern

    def hash(self) -> int:
        out = 0
        for b in self.pattern:
            out = (out << 1) | b
        return out

    def get(self, row: int, column: int) -> bool:
        return self.pattern[row * self.size + column]

    def set(self, row: int, column: int, value: bool) -> None:
        self.pattern[row * self.size + column] = value

    def get_divisor(self) -> int:
        if self.size % 2 == 0:
            return 2
        elif self.size % 3 == 0:
            return 3
        else:
            raise RuntimeError(f"Pattern size is not divisible by 2 nor by 3 (size = {self.size})")

    def get_subpattern(self, row: int, column: int) -> List['Pattern']:
        divisor = self.get_divisor()
        sub_pattern = Pattern([0] * divisor * divisor)

        for i in range(divisor):
            start = row * self.size * divisor + column * divisor + i * self.size
            sub_pattern.pattern[i * divisor:(i + 1) * divisor] = self.pattern[start:start + divisor]
        
        return sub_pattern

    def set_subpattern(self, row:int, column: int, sub_pattern: 'Pattern') -> None:
        for i in range(sub_pattern.size):
            start = row * self.size * sub_pattern.size + column * sub_pattern.size + i * self.size
            self.pattern[start:start + sub_pattern.size] = sub_pattern.pattern[i * sub_pattern.size:(i + 1) * sub_pattern.size]

    def flip_horizontal(self) -> 'Pattern':
        new_pattern = Pattern([0] * len(self.pattern))
        for i in range(self.size):
            for j in range(self.size):
                new_pattern.set(i, self.size - j - 1, self.get(i, j))
        return new_pattern

    def flip_vertical(self) -> 'Pattern':
        new_pattern = Pattern([0] * len(self.pattern))
        for i in range(self.size):
            for j in range(self.size):
                new_pattern.set(self.size - i - 1, j, self.get(i, j))
        return new_pattern

    def rotate_ccw(self) -> 'Pattern':
        new_pattern = Pattern([0] * len(self.pattern))
        for i in range(self.size):
            for j in range(self.size):
                new_pattern.set(self.size - j - 1, i, self.get(i, j))
        return new_pattern

    def enchance(self, rules: Dict[int, 'Rule']) -> 'Pattern':
        divisor = self.get_divisor()
        sub_patterns_count = self.size // divisor
        new_size = self.size + sub_patterns_count
        new_pattern = Pattern([0] * new_size * new_size)

        # enchance all sub-patterns
        for i in range(sub_patterns_count):
            for j in range(sub_patterns_count):
                sub_pattern = self.get_subpattern(i, j)

                # find matching enchancement rule
                matching_rules = [r for r in rules[divisor] if r.match(sub_pattern)]
                if len(matching_rules) != 1:
                    raise RuntimeError(
                        f"Cannot find a unique rule that matches the pattern ({len(matching_rules)} rules matched)")

                # enchance sub-pattern
                new_pattern.set_subpattern(i, j, matching_rules[0].out_pattern)

        return new_pattern

    def __str__(self) -> str:
        text = ""
        for i in range(self.size):
            if i != 0:
                text += '/'
            for j in range(self.size):
                text += '#' if self.get(i, j) else '.'
        return text

    __repr__ = __str__


class Rule:
    def __init__(self, in_pattern: Pattern, out_pattern: Pattern):
        self.out_pattern = out_pattern
        self.size = in_pattern.size

        # generate all possible input pattern permutations
        in_pattern_rotated_90 = in_pattern.rotate_ccw()
        in_pattern_rotated_180 = in_pattern_rotated_90.rotate_ccw()
        in_pattern_rotated_270 = in_pattern_rotated_180.rotate_ccw()
        in_patterns = [
            in_pattern,
            in_pattern.flip_horizontal(),
            in_pattern.flip_vertical(),
            in_pattern_rotated_90,
            in_pattern_rotated_90.flip_horizontal(),
            in_pattern_rotated_90.flip_vertical(),
            in_pattern_rotated_180,
            in_pattern_rotated_270,
        ]

        # get hashes for all possible input pattern permutations
        self.in_pattern_hashes = set([p.hash() for p in in_patterns])

    def match(self, pattern: Pattern) -> bool:
        return pattern.hash() in self.in_pattern_hashes


def parse_pattern(text: str) -> Pattern:
    return Pattern([b == '#' for b in text if b != '/'])


def parse_rule(line: str) -> Rule:
    parts = line.split('=>')
    in_pattern = parse_pattern(parts[0].strip())
    out_pattern = parse_pattern(parts[1].strip())
    return Rule(in_pattern, out_pattern)


def do_iterations(rules: Dict[int, List[Rule]], count: int) -> Pattern:
    pattern = parse_pattern('.#./..#/###')
    for _ in range(count):
        pattern = pattern.enchance(rules)
    
    return pattern


def main():
    rules = {
        2: [],
        3: []
    }
    with open('day_21_input.txt') as file:
        for line in file.readlines():
            rule = parse_rule(line)
            rules[rule.size].append(rule)

    # part 1
    pattern = do_iterations(rules, 5)
    print(len([x for x in pattern.pattern if x]))

    # part 2
    pattern = do_iterations(rules, 18)
    print(len([x for x in pattern.pattern if x]))


main()
