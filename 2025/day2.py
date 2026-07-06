from typing import Iterable
from itertools import accumulate

def part1(movements : Iterable[int]):
    return accumulate(movements)

def part2(movements : Iterable[int]):
    height = 0
    momentum = 0
    direction = 0
    for movement in movements:
        if direction == movement:
            momentum += 1
        else:
            direction = movement
            momentum = 0
        height += momentum * direction
        yield height

def part3(movements : Iterable[int]):
    height = 0
    direction = 0
    prev, curr = 0, 1
    for movement in movements:
        if direction == movement:
            height += prev * direction
            prev, curr = curr, prev + curr
        else:
            prev, curr = 0, 1
            direction = movement
            height += direction
        yield height

def main():
    movements = tuple(1 if c == '^' else -1 for c in input())

    print('part1 =', max(part1(movements)))
    print('part2 =', max(part2(movements)))
    print('part3 =', max(part3(movements)))


if __name__ == "__main__":
    main()