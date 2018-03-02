"""
--- Day 19: A Series of Tubes ---
Somehow, a network packet got lost and ended up here. It's trying to follow a
routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -,
and +) show the path it needs to take, starting by going down onto the only line
connected to the top of the diagram. It needs to follow this path until it
reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue
going the same direction, and only turn left or right when there's no other
option. In addition, someone has left letters on the line; these also don't
change its direction, but it can use them to keep track of where it's been. For
example:

     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

Given this diagram, the packet needs to take the following path:

Starting at the only line touching the top of the diagram, it must go down, pass
through A, and continue onward to the first +.
Travel right, up, and right, passing through B in the process.
Continue down (collecting C), right, and up (collecting D).
Finally, go all the way left through E and stopping at F.
Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What
letters will it see (in the order it would see them) if it follows the path?
(The routing diagram is very wide; make sure you view it without line wrapping.)

Your puzzle answer was DWNBGECOMY.

--- Part Two ---
The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |          
     |  +--+    
     A  |  C    
 F---|--|-E---+ 
     |  |  |  D 
     +B-+  +--+ 

...the packet would go:

6 steps down (including the first line at the top of the diagram).
3 steps right.
4 steps up.
3 steps right.
4 steps down.
3 steps right.
2 steps up.
13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

Your puzzle answer was 17228.
"""


from typing import List, Optional


class Map:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.pos = (0, lines[0].index('|'))
        self.direction = 0 # 0 - down, 1 - left, 2 - up, 3 - right
        self.steps = 1

    def get_character(self, pos: (int, int)) -> str:
        return self.lines[pos[0]][pos[1]]

    def change_direction(self) -> Optional[int]:
        if self.direction == 0 or self.direction == 2:
            # new direction will be left or right
            if self.pos[1] > 0 and self.get_character((self.pos[0], self.pos[1] - 1)) != ' ':
                # new direction is left
                return 1
            elif (self.pos[1] + 1) < len(self.lines[self.pos[0]]) and self.get_character((self.pos[0], self.pos[1] + 1)) != ' ':
                # new direction is right
                return 3
        else:
            # new direction will be down or up
            if self.pos[0] > 0 and self.get_character((self.pos[0] - 1, self.pos[1])) != ' ':
                # new direction is up
                return 2
            elif (self.pos[0] + 1) < len(self.lines) and self.get_character((self.pos[0] + 1, self.pos[1])) != ' ':
                # new direction is down
                return 0

        # end of game
        return None

    def move(self) -> Optional[str]:
        # try to move in the current direction
        if self.direction == 0:
            new_pos = (self.pos[0] + 1, self.pos[1])
        elif self.direction == 1:
            new_pos = (self.pos[0], self.pos[1] - 1)
        elif self.direction == 2:
            new_pos = (self.pos[0] - 1, self.pos[1])
        elif self.direction == 3:
            new_pos = (self.pos[0], self.pos[1] + 1)

        # check if move is possible
        if (
                new_pos[0] < 0 or
                new_pos[0] == len(self.lines) or
                new_pos[1] < 0 or
                new_pos[1] == len(self.lines[new_pos[0]]) or
                self.get_character(new_pos) == ' '
            ):
            # we need to change direction
            new_direction = self.change_direction()
            if new_direction is None:
                # we've reached the end
                return None
            self.direction = new_direction
            return self.move()

        self.pos = new_pos
        self.steps += 1
        return self.get_character(self.pos)

    def go(self) -> str:
        text = ''
        while True:
            character = self.move()
            if character is None:
                return text
            elif character == '|' or character == '-' or character == '+':
                continue
            else:
                text += character


def main():
    with open('day_19_input.txt') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]
    
        diagram = Map(lines)
        print(diagram.go())
        print(diagram.steps)


main()
