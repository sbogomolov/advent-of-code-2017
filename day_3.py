"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite
two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location
marked 1 and then counting up while spiraling outward. For example, the first
few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must
be carried back to square 1 (the location of the only access port for this
memory system) by programs that can only move up, down, left, or right. They
always take the shortest path: the Manhattan Distance between the location of
the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your
puzzle input all the way to the access port?

Your puzzle answer was 326.

--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store
the value 1 in square 1. Then, in the same allocation order as shown above, they
store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

Once a square is written, its value does not change. Therefore, the first few
squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

Your puzzle answer was 363010.
"""

import math

def find_index(x_coord: int, y_coord: int):
    """ Finds index by coordinates. Index starts from 1. """
    radius = max(abs(x_coord), abs(y_coord))
    inner_edge = (2 * radius - 1)
    inner_points = inner_edge * inner_edge
    if y_coord == -radius:
        shift = 3 * (radius * 2) + (radius + x_coord)
    elif y_coord == radius:
        shift = (radius * 2) + (radius - x_coord)
    elif x_coord == -radius:
        shift = 2 * (radius * 2) + (radius - y_coord)
    else:
        shift = radius + y_coord

    return inner_points + shift

def find_coordinates(index: int):
    """ Finds coordinates by index. Index starts from 1. """
    radius = math.floor(math.ceil(math.sqrt(index)) / 2)
    inner_edge = (2 * radius - 1)
    inner_points = inner_edge * inner_edge
    min_value = inner_points + 1
    value = index - min_value
    if value < (2 * radius):
        return (radius, value - radius + 1)
    elif value < (4 * radius):
        shift = value - 2 * radius
        return (radius - shift - 1, radius)
    elif value < (6 * radius):
        shift = value - 4 * radius
        return (-radius, radius - shift - 1)
    else:
        shift = value - 6 * radius
        return (shift - radius + 1, -radius)

def count_steps(index: int):
    """ Finds Manhattan Distance. """
    x_coord, y_coord = find_coordinates(index)
    return abs(x_coord) + abs(y_coord)

def find_first_larger(value: int):
    """ Finds first number in sequence that is larger than the provided value. """
    numbers = [1]
    while True:
        # current coordinates
        x_coord, y_coord = find_coordinates(len(numbers) + 1)

        # compute new value
        new_value = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # do not add the element itself (even though it does not
                # exist yet, we can save some cycles here)...
                # or not if this will break branch predicting...
                if i == 0 and j == 0:
                    continue

                # add existing surrounding elements
                index = find_index(x_coord + i, y_coord + j) - 1
                if index < len(numbers):
                    new_value += numbers[index]

        if new_value > value:
            return new_value

        # save value for future computations
        numbers.append(new_value)

def main():
    """ Main function """
    input_value = 361527

    # part 1
    print(count_steps(input_value))

    # part 2
    print(find_first_larger(input_value))

main()
