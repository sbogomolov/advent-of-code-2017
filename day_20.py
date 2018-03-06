"""
--- Day 20: Particle Swarm ---
Suddenly, the GPU contacts you, asking for help. Someone has asked it to
simulate too many particles, and it won't be able to finish them all in time to
render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in order
(starting with particle 0, then particle 1, particle 2, and so on). For each
particle, it provides the X, Y, and Z coordinates for the particle's position
(p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties are
updated in the following order:

Increase the X velocity by the X acceleration.
Increase the Y velocity by the Y acceleration.
Increase the Z velocity by the Z acceleration.
Increase the X position by the X velocity.
Increase the Y position by the Y velocity.
Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would like
to know which particle will stay closest to position <0,0,0> in the long term.
Measure this using the Manhattan distance, which in this situation is simply the
sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay
entirely on the X-axis (for simplicity). Drawing the current states of particles
0 and 1 (in that order) with an adjacent a number line and diagram of current X
positions (marked in parenthesis), the following would take place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)   

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and
so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

Your puzzle answer was 161.

--- Part Two ---
To simplify the problem further, the GPU would like to remove any particles that
collide. Particles collide if their positions ever exactly match. Because
particles are updated simultaneously, more than two particles can collide at the
same time and place. Once particles collide, they are removed and cannot collide
with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)   
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)      
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------    
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)         
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the time
and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?

Your puzzle answer was 438.
"""


from typing import List, Optional, Iterable
import math


class Vec3:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.current = self.x

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        return [self.x, self.y, self.z].__iter__()

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vec3(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Vec3(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vec3(self.x / other, self.y / other, self.z / other)

    def __pow__(self, other):
        return Vec3(self.x ** other, self.y ** other, self.z ** other)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def dist(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __repr__ = __str__


class Particle:
    def __init__(self, p: Vec3, v: Vec3, a: Vec3):
        self.p = p
        self.v = v
        self.a = a

    def __str__(self) -> str:
        return f"(p={self.p}, v={self.v}, a={self.a})"

    __repr__ = __str__


class Solution:
    def __init__(self, n1 = None, n2 = None, is_any = False):
        self.n1 = n1 if (n1 is not None) and (n1 >= 0) else None
        self.n2 = n2 if (n2 is not None) and (n2 >= 0) else None
        self.is_any = is_any
        self.is_none = (n1 is None) and (n2 is None)

    def __str__(self) -> str:
        if self.is_any:
            return '{Any}'
        elif self.is_none:
            return '{None}'
        elif self.n1 is None:
            return f"{self.n2}"
        elif self.n2 is None:
            return f"{self.n1}"
        else:
            return f"{{{self.n1} or {self.n2}}}"

    def get_min(self) -> int:
        if self.n1 is None:
            return self.n2
        elif self.n2 is None:
            return self.n1
        else:
            return min(self.n1, self.n2)

    def combine(self, other):
        if self.is_any and other.is_any:
            return Solution(is_any = True)
        elif self.is_any:
            return Solution(other.n1, other.n2, other.is_any)
        elif other.is_any:
            return Solution(self.n1, self.n2, self.is_any)
        elif self.is_none or other.is_none:
            return Solution()
        else:
            other_solutions = set([other.n1, other.n2])
            return Solution(
                n1 = self.n1 if self.n1 in other_solutions else None,
                n2 = self.n2 if self.n2 in other_solutions else None
            )

    __repr__ = __str__


def check_discriminant(d: int) -> bool:
    if d < 0:
        return False
    return True


def solve_equation(a: int, b: int, c: int) -> Solution:
    if a == 0:
        # this is not a quadratic equation
        if b == 0:
            # this is not an equation at all
            if c == 0:
                # particles are starting collided
                return Solution(is_any = True)
            else:
                # particles are stationary, no collisions
                return Solution()

        # solve b*n + c = 0
        n = -(c / b)
        return Solution(int(n) if n.is_integer() else None)

    # compute discriminant
    d = b**2 - 4*a*c
    if not check_discriminant(d):
        return Solution()

    # compute n where particles might intersect
    n1 = (-b + math.sqrt(d)) / (2*a)
    n2 = (-b - math.sqrt(d)) / (2*a)
    
    return Solution(
        int(n1) if n1.is_integer() else None,
        int(n2) if n2.is_integer() else None
    )


def combine_solutions(solutions: Iterable) -> Solution:
    combined_solution = Solution(is_any = True)
    for s in solutions:
        combined_solution = combined_solution.combine(s)

    return combined_solution


def check_collision(p1: Particle, p2: Particle) -> Optional[int]:
    a = (p1.a - p2.a) / 2
    b = p1.v - p2.v + (p1.a - p2.a) / 2
    c = (p1.p - p2.p)

    solutions = [solve_equation(*x) for x in zip(a, b, c)]
    final_solution = combine_solutions(solutions)

    if final_solution.is_none:
        return None
    elif final_solution.is_any:
        return 0
    else:
        return final_solution.get_min()


def parse_vector(text: str) -> Vec3:
    coords = [int(x.strip()) for x in text.split(',')]
    return Vec3(*coords)


def main() -> None:
    particles = []
    with open('day_20_input.txt') as file:
        for line in file.readlines():
            data = [parse_vector(p.strip(' >')[3:]) for p in line.strip().split('>,')]
            particles.append(Particle(*data))

    # Both Part 1 and Part 2 can be solved analytically

    # Part 1: we find the slowest particle closest to origin
    closest = particles[0]
    for p in particles:
        # compare acceleration
        if p.a.dist() < closest.a.dist():
            closest = p
        elif p.a.dist() == closest.a.dist():
            # compare speeds
            if p.v.dist() < closest.v.dist():
                closest = p
                continue
            elif p.v.dist() == closest.v.dist():
                # compare positions
                if p.p.dist() < closest.p.dist():
                    closest = p
                    continue

    print(particles.index(closest))

    # Part 2: we find all collisions of all particles
    # trajectory of each particle can be described as:
    # p(n) = p(0) + v(0) * n + n*(n+1)/2 * a(0)
    # We can take equations for two particles and find
    # n for which positions for all 3 coordinates are
    # equal. This will be tha tick when they have
    # collided.
    
    # check for particle collisions
    collisions = {}
    for i1, p1 in enumerate(particles[:-1]):
        for p2 in particles[(i1 + 1):]:
            n = check_collision(p1, p2)
            if n is not None:
                if n not in collisions:
                    collisions[n] = set()
                collisions[n].add(p1)
                collisions[n].add(p2)

    # now we need to replay collisions and keep track
    # of destroyed particles to exclude collisions
    # with partickles destroyed in previous collisions
    destroyed_particles = set()
    for n in sorted(collisions.keys()):
        # get particles that have collided at step n and were not destroyed before
        collided_particles = [p for p in collisions[n] if p not in destroyed_particles]

        # if there are more than 1 collided particles - destory them
        if len(collided_particles) > 1:
            for p in collided_particles:
                destroyed_particles.add(p)

    print(len(particles) - len(destroyed_particles))


main()
