r"""
--- Day 11: Hex Ed ---
Crossing the bridge, you've barely reached the other side of the stream when a
program comes up to you, clearly in distress. "It's my child process," she says,
"he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be
found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to
determine the fewest number of steps required to reach him. (A "step" means to
move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).

Your puzzle answer was 784.

--- Part Two ---
How many steps away is the furthest he ever got from his starting position?

Your puzzle answer was 1558.

This resource contains a lot of information about hexagonal grids:
https://www.redblobgames.com/grids/hexagons/
"""

def make_move(x_coord: int, y_coord: int, direction: str):
    """ Makes a move and returns a new position """
    if direction == 'n':
        return x_coord + 1, y_coord
    elif direction == 'ne':
        return x_coord + 1, y_coord - 1
    elif direction == 'se':
        return x_coord, y_coord - 1
    elif direction == 's':
        return x_coord - 1, y_coord
    elif direction == 'sw':
        return x_coord - 1, y_coord + 1
    elif direction == 'nw':
        return x_coord, y_coord + 1
    else:
        raise ValueError("Unknown direction: $s" % direction)

def main():
    """ Main function """
    with open('day_11_input.txt') as file:
        moves = file.readline().split(',')

    x_coord = 0
    y_coord = 0
    max_distance = 0
    for move in moves:
        # compute axial coordinates after move
        x_coord, y_coord = make_move(x_coord, y_coord, move)

        # compute z to have all cube coordinates taking into account that x + y + z = 0
        z_coord = -(x_coord + y_coord)
        distance = int((abs(x_coord) + abs(y_coord) + abs(z_coord)) / 2)
        max_distance = max(max_distance, distance)

    print(distance)
    print(max_distance)

main()
