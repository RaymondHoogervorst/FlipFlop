import typing, dataclasses, sys

SKY_SIZE = 1000
FRAME_SIZE = SKY_SIZE // 2

FRAME_START = (SKY_SIZE - FRAME_SIZE) // 2
FRAME_END = FRAME_START + FRAME_SIZE

@dataclasses.dataclass
class Point:
    y : int = 0
    x : int = 0
    
    @staticmethod
    def parse(line : str):
        return Point(*map(int, line.split(',')))

    def __add__(self, other : typing.Self):
        return Point((self.y + other.y) % SKY_SIZE, (self.x + other.x) % SKY_SIZE)

    def __mul__(self, factor : int):
        return Point((self.y * factor) % SKY_SIZE, (self.x * factor) % SKY_SIZE)

@dataclasses.dataclass
class Bird:
    position : Point
    velocity : Point

    @staticmethod
    def parse(line : str):
        return Bird(Point(), Point.parse(line))

    def fly(self, n = 1):
        return Bird(self.position + (self.velocity * n), self.velocity)

    def in_frame(self):
        return FRAME_START <= self.position.x < FRAME_END and FRAME_START <= self.position.y < FRAME_END


def main():
    birds = tuple(map(Bird.parse, sys.stdin.readlines()))

    def count_birds_in_frame(t : int):
        return sum(bird.fly(t).in_frame() for bird in birds)

    def count_birds_in_frames(period, k=1000):
        return sum(map(count_birds_in_frame, range(period, period * (k + 1), period)))

    print("part1 =", count_birds_in_frame(100))
    print("part2 =", count_birds_in_frames(3600))
    print("part3 =", count_birds_in_frames(31556926))



if __name__ == "__main__":
    main()
