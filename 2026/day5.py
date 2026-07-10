import sys, dataclasses
from typing import Self

@dataclasses.dataclass
class Point:
    y : int
    x : int

    def __hash__(self):
        return hash((self.y, self.x))

    def right_turn(self):
        return Point(y = self.x, x = -self.y)

    def __add__(self, other : Self):
        return Point(y = self.y + other.y, x = self.x + other.x)

DIRECTIONS = {
    '<' : Point(0,-1),
    '>' : Point(0,1),
    'v' : Point(1,0),
    '^' : Point(-1,0),
}

def parse_grid():
    return [
        list(map(DIRECTIONS.__getitem__, line.strip()))
    for line in sys.stdin.readlines()]

def traverse(grid : list[list[Point]], illegal_turns = 0):
    seen : set[Point] = set()
    height = len(grid)
    width = len(grid[0])

    def move(pos : Point):
        return pos + grid[pos.y][pos.x]

    curr_pos = Point(0,0)
    
    for _ in range(illegal_turns + 1):
        while curr_pos not in seen:
            seen.add(curr_pos)
            curr_pos = move(curr_pos)
        if curr_pos.y in (0, height-1) or curr_pos.x in (0, width-1):
            break
        curr_pos = curr_pos + grid[curr_pos.y][curr_pos.x].right_turn()
    return seen

def optimize(grid, illegal_turns = 0):
    path = traverse(grid, illegal_turns)
    height = len(grid)
    width = len(grid[0])

    result = len(traverse(grid, illegal_turns))

    for cell in path:
        if cell.y in (0,height-1) or cell.x in (0,width-1):
            continue
        original_value = grid[cell.y][cell.x]
        for direction in DIRECTIONS.values():
            if direction != original_value:
                grid[cell.y][cell.x] = direction
                result = max(result, len(traverse(grid, illegal_turns)))
            grid[cell.y][cell.x] = original_value
    return result

def main():
    grid = parse_grid()
    part1 = len(traverse(grid))
    part2 = optimize(grid)
    part3 = optimize(grid, 3)

    print("part1 =", part1)
    print("part2 =", part2)
    print("part3 =", part3)


if __name__ == "__main__":
    main()