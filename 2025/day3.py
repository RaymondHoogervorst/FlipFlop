import sys, statistics, dataclasses

@dataclasses.dataclass
class Color:
    red : int
    green : int
    blue : int

    @staticmethod
    def parse(line : str):
        return Color(*map(int,line.split(',')))

    def __iter__(self):
        yield from (self.red,self.green,self.blue)

    def get_label(self):
        if len(set(self)) != 3:
            return 'Special'
        max_value = max(self)
        if self.red == max_value:
            return 'Red'
        if self.green == max_value:
            return 'Green'
        if self.blue == max_value:
            return 'Blue'
        assert False, 'Impossible'

    def get_price(self):
        return {
            'Red' : 5,
            'Green' : 2,
            'Blue' : 4,
            'Special' : 10
        }[self.get_label()]

    def __str__(self):
        return f'{self.red},{self.green},{self.blue}'

def main():
    colors = tuple(map(Color, sys.stdin))
    print('part1 =', statistics.mode(colors))
    print('part2 =', tuple(map(Color.get_label, colors)).count('Green'))
    print('part3 =', sum(map(Color.get_price, colors)))

if __name__ == "__main__":
    main()
