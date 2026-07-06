import sys, dataclasses, math, itertools

@dataclasses.dataclass
class Grid:
    x : int = 0
    y : int = 0

    @staticmethod
    def parse(line : str):
        return Grid(*map(int, line.strip().split(' ')))

    @staticmethod
    def num_paths(*dimensions):
        path_length = 0
        num_paths = 1
        for dimension in dimensions:
            path_length += dimension - 1
            num_paths *= math.comb(path_length, dimension - 1)
        return num_paths

    def num_2d_paths(self):
        return self.num_paths(self.x, self.y)

    def num_3d_paths(self):
        return self.num_paths(self.x, self.y, self.x)

    def num_xd_paths(self):
        return self.num_paths(*(self.y for _ in range(self.x)))

def main():
    grids = tuple(map(Grid.parse, sys.stdin.readlines()))
    print('part1 =', sum(map(Grid.num_2d_paths, grids)))
    print('part2 =', sum(map(Grid.num_3d_paths, grids)))
    print('part3 =', sum(map(Grid.num_xd_paths, grids)))


if __name__ == "__main__":
    main()
