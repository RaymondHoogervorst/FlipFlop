import sys, dataclasses
from typing import Self
from collections import deque

@dataclasses.dataclass
class Point:
    x : int
    y : int

    def __hash__(self):
        return hash((self.y, self.x))

    def __add__(self, other : Self):
        return Point(self.x + other.x, self.y + other.y)

DIRECTIONS = {
    '<' : Point(-1,0),
    '>' : Point(1,0),
    '^' : Point(0,1),
    'v' : Point(0,-1),
}

def part1(movements, fruits):
    snake_head = Point(0,0)
    fruit_i = 0
    n = len(movements)

    for movement in movements[:n//2]:
        snake_head += movement
        if snake_head == fruits[fruit_i]:
            fruit_i += 1
    return fruit_i

def part2(movements, fruits):
    snake_head = Point(0,0)
    snake = deque((snake_head,))
    fruit_i = 0

    for movement in movements:
        snake_head += movement
        if snake_head == fruits[fruit_i]:
            fruit_i += 1
        else:
            snake.popleft()
        if snake_head in snake:
            break
        snake.append(snake_head)
    return fruit_i + 1

def part3(movements, fruits):
    snake_head = Point(0,0)
    snake = deque((snake_head,))
    fruit_i = 0
    self_bites = 0

    for movement in movements:

        snake_head += movement
        if fruit_i < len(fruits) and snake_head == fruits[fruit_i]:
            fruit_i += 1
        else:
            snake.popleft()

        if snake_head in snake:
            body_index = snake.index(snake_head)
            self_bites += 1
            for _ in range(body_index + 2):
                snake.popleft()
        snake.append(snake_head)
    return len(snake) * self_bites

def main():
    movements = tuple(map(DIRECTIONS.__getitem__, input()))
    input()
    fruits = tuple(Point(*map(int, line.split(','))) for line in sys.stdin.readlines())

    print("part1 =", part1(movements, fruits))
    print("part2 =", part2(movements, fruits))
    print("part3 =", part3(movements, fruits))



if __name__ == "__main__":
    main()