import sys, itertools, typing, math

ROW_SIZE = 5

class IntRef:
    def __init__(self):
        self.value = 0

    def __str__(self):
        return str(self.value)

    def increment(self):
        self.value += 1
        return self.value

class BingoCard:
    def __init__(self, numbers : typing.Collection[int]):
        self.dimensions = int(math.log(len(numbers), ROW_SIZE))
        assert len(numbers) == ROW_SIZE ** self.dimensions
        self.line_references : typing.Dict[int, typing.List[IntRef]] = {}

        for line in self._build_lines(numbers):
            line_reference = IntRef()
            for x in line:
                self.line_references.setdefault(x, []).append(line_reference)

    @staticmethod
    def _get_coord_from_axis_flow(i,x):
        if isinstance(x, int):
            return x
        elif x == '+':
            return i
        else:
            return ROW_SIZE - 1 - i

    def _build_lines(self, numbers):
        axis_patterns  = (*range(ROW_SIZE), '+', '-')

        for axis_flows in itertools.product(axis_patterns, repeat=self.dimensions):
            variable_axes = tuple(movement for movement in axis_flows if movement in ('+','-'))
            if not variable_axes or variable_axes[0] == '+':
                continue
            
            line = []
            for i in range(ROW_SIZE):
                coords = tuple(self._get_coord_from_axis_flow(i,axis_flow) for axis_flow in axis_flows)
                number_index = sum(coord * (ROW_SIZE ** i) for i,coord in enumerate(coords))
                line.append(numbers[number_index])
                yield line

    def mark(self, number : int):
        bingos = 0
        for line_reference in self.line_references.get(number, []):
            bingos += line_reference.increment() == ROW_SIZE
        return bingos

class BingoCube(BingoCard):
    def __init__(self, numbers):
        super().__init__(numbers)

def solve(read_out_numbers : typing.Iterable[int], bingo_card_numbers : typing.Iterable[int], dimensions=2):
    bingo_cards = tuple(map(BingoCard, itertools.batched(bingo_card_numbers, ROW_SIZE**dimensions)))
    num_bingo = 0
    for x in read_out_numbers:
        for card in bingo_cards:
            num_bingo += card.mark(x)
        if num_bingo >= 5:
            return x

def main():
    read_out_numbers = []
    bingo_card_numbers = []

    active_array = read_out_numbers
    for line in map(str.split,sys.stdin):
        if line:
            active_array.extend(map(int,line))
        else:
            active_array = bingo_card_numbers

    print('part1 =', solve(read_out_numbers, bingo_card_numbers, 2))
    print('part2 =', solve(read_out_numbers, bingo_card_numbers, 3))
    print('part3 =', solve(read_out_numbers, bingo_card_numbers, 4))

if __name__ == "__main__":
    main()