import dataclasses, typing, sys

@dataclasses.dataclass
class Point:
    y : int
    x : int
    
    @staticmethod
    def parse(line : str):
        return Point(*map(int, line.split(',')))

    def manhattan_distance(self, other : typing.Self):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def diagonal_distance(self, other : typing.Self):
        return max(abs(self.y - other.y), abs(self.x - other.x))

START_POS = Point(0,0)

def main():
    trash = tuple(map(Point.parse, sys.stdin))

    part1 = part2 = part3 = 0
    previous = START_POS

    for point in trash:
        part1 += previous.manhattan_distance(point)
        part2 += previous.diagonal_distance(point)
        previous = point

    previous = START_POS
    for point in sorted(trash, key=START_POS.manhattan_distance):
        part3 += previous.diagonal_distance(point)
        previous = point

    print("part1 =", part1)
    print("part2 =", part2)
    print("part3 =", part3)

if __name__ == "__main__":
    main()
