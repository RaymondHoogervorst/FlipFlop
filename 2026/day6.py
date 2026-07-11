import sys, math

def is_prime(x : int):
    for d in range(2, math.floor(math.sqrt(x)) + 1):
        if x % d == 0:
            return False
    return True

class Grid:

    def _in_bounds(self, pos):
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width

    def neighbors(self, pos):
        y, x = pos
        return (
            (neighbor, self.data[neighbor[0]][neighbor[1]])
        for neighbor in filter(self._in_bounds, ((y+1,x), (y-1,x), (y,x+1), (y,x-1))))

    def find_char(self, c):
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] == c:
                    return y,x

    def __init__(self):
        self.data = tuple(map(str.strip, sys.stdin))
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.rotation = [[0] * self.width for _ in range(self.height)]
        self.teleports_enabled = False
        self.part = 1
        self.start = self.find_char('S')
        self.rotation[self.start[0]][self.start[1]] = -1
        assert self.start is not None

    def reset(self):
        self.rotation = [[0] * self.width for _ in range(self.height)]
        self.rotation[self.start[0]][self.start[1]] = -1
        assert self.start is not None

    def score(self):
        self.reset()
        self.expand()
        result = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] != '*' or self.rotation[y][x] == 0:
                    continue
                result *= 2
                result += self.rotation[y][x] == -1
        return result

    def connect_bluetooth(self, c):
        if self.part < 2 or not c.islower():
            return False
        output = self.find_char(c.upper())
        if self.part == 2:
            return output

        queue = [output]
        seen = set()
        while queue:
            pos = queue.pop()
            if pos in seen:
                continue
            seen.add(pos)
            for neighbor, neighbor_c in self.neighbors(pos):
                if neighbor_c in ('#', '3'):
                    queue.append(neighbor)
        gear_count = len(seen) - 1

        return None if is_prime(gear_count) else output

    def expand(self):
        seen = set()
        queue = [self.start]

        while queue:
            pos = queue.pop()
            if pos in seen:
                continue
            seen.add(pos)
            for neighbor, c in self.neighbors(pos):
                self.rotation[neighbor[0]][neighbor[1]] = self.rotation[pos[0]][pos[1]] * -1
                if c == '#' or (self.part >= 2 and c == '3'):
                    queue.append(neighbor)
                elif bluetooth_output := self.connect_bluetooth(c):
                    self.rotation[bluetooth_output[0]][bluetooth_output[1]] = self.rotation[pos[0]][pos[1]]
                    queue.append(bluetooth_output)

def main():
    grid = Grid()
    print("part1 =", grid.score())
    grid.part = 2
    print("part2 =", grid.score())
    grid.part = 3
    print("part3 =", grid.score())

if __name__ == "__main__":
    main()