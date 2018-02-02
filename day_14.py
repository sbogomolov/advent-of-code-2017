"""
--- Day 14: Disk Defragmentation ---
Suddenly, a scheduled job activates the system's disk defragmenter. Were the
situation different, you might sit and watch it for a while, but today, you just
don't have that kind of time. It's soaking up valuable system resources that are
needed elsewhere, and so the only option is to help it finish its task as soon
as possible.

The disk in question consists of a 128x128 grid; each square of the grid is
either free or used. On this disk, the state of the grid is tracked by the bits
in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in
the grid; each hash contains 128 bits which correspond to individual grid
squares. Each bit of a hash indicates whether that square is free (0) or used
(1).

The hash inputs are a key string (your puzzle input), a dash, and a number from
0 to 127 corresponding to the row. For example, if your key string were
flqrgnkx, then the first row would be given by the bits of the knot hash of
flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so
on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits;
each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits. To
convert to bits, turn each hexadecimal digit to its equivalent binary value,
high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111,
and so on; a hash that begins with a0c2017... in hexadecimal would begin with
10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as
follows, using # to denote used squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle answer was 8292.

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a
group of used squares that are all adjacent, not including diagonals. Every used
square is in exactly one region: lone used squares form their own isolated
regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a
distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V

Of particular interest is the region marked 8; while it does not appear
contiguous in this small view, all of the squares marked 8 are connected when
considering the whole 128x128 grid. In total, in this example, 1242 regions are
present.

How many regions are present given your key string?

Your puzzle answer was 1069.
"""

from typing import List


def reverse(values: List[int], start: int, length: int) -> None:
    for i in range(int(length / 2)):
        index = (start + i) % len(values)
        opposite_index = (start + length - i - 1) % len(values)
        values[index], values[opposite_index] = values[opposite_index], values[index]


def compute_hash(value: str) -> str:
    sparse_hash = list(range(256))
    cur_pos = 0
    skip = 0

    lengths = [ord(c) for c in value] + [17, 31, 73, 47, 23]

    for i in range(64):
        for length in lengths:
            reverse(sparse_hash, cur_pos, length)
            cur_pos = (cur_pos + length + skip) % len(sparse_hash)
            skip = (skip + 1) % len(sparse_hash)

    dense_hash = [0] * 16
    for i in range(16):
        for j in range(16):
            dense_hash[i] ^= sparse_hash[i * 16 + j]

    hash_string = ''.join(('{:02x}'.format(x) for x in dense_hash))
    return hash_string


def count_used_blocks(bit_map: List[List[bool]]) -> int:
    return sum((sum(x) for x in bit_map))


def count_used_regions(bit_map: List[List[int]]) -> int:
    regions_count = 0
    regions_map = [[False] * len(x) for x in bit_map]
    for i in range(len(bit_map)):
        for j in range(len(bit_map[i])):
            # skip unused blocks and blocks that already belong to regions
            if not bit_map[i][j] or regions_map[i][j]:
                continue

            explore_region(bit_map, regions_map, j, i)
            regions_count += 1

    return regions_count


def explore_region(bit_map: List[List[bool]], regions_map: List[List[bool]], x: int, y: int) -> None:
    explore_blocks = [(x, y)]
    while explore_blocks:
        x, y = explore_blocks.pop()
        regions_map[y][x] = True

        # check surrounding blocks
        for i in range(-1, 2, 2):
            y1 = y + i
            if (y1 >= 0) and (y1 < len(bit_map)) and not regions_map[y1][x] and bit_map[y1][x]:
                explore_blocks.append((x, y1))

            x1 = x + i
            if (x1 >= 0) and (x1 < len(bit_map[y])) and not regions_map[y][x1] and bit_map[y][x1]:
                explore_blocks.append((x1, y))


def main():
    key = 'ugkiagan'

    bit_map = []
    for i in range(128):
        hash_string = compute_hash(f"{key}-{i}")
        bit_string = ''.join(('{:04b}'.format(int(x, 16)) for x in hash_string))
        bit_map.append([bool(int(x)) for x in bit_string])

    print(f"Used blocks:  {count_used_blocks(bit_map)}")
    print(f"Used regions: {count_used_regions(bit_map)}")


main()
