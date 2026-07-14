from typing import Self, Protocol, Callable, Iterable, Optional
import sys, dataclasses, heapq, functools

@functools.total_ordering
class Node(Protocol):
    def __hash__(self) -> int: ...
    def __lt__(self, other : Self, /): ...

@functools.total_ordering
@dataclasses.dataclass
class Point:
    x : int
    y : int

    def __hash__(self):
        return hash((self.y, self.x))

    def __add__(self, other : Self):
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

DIRECTIONS = frozenset((
    Point(-1,0),
    Point(1,0),
    Point(0,1),
    Point(0,-1),
))

def next_wall(pos, direction, maze):
    new_pos = pos
    while (new_pos + direction) in maze:
        new_pos += direction
    return new_pos

def part1_neighbors(pos : Point, maze : set[Point]):
    for direction in DIRECTIONS:
        new_pos = pos + direction
        if new_pos in maze:
            yield 1, new_pos

def part2_neighbors(pos : Point, maze : set[Point]):
    for direction in DIRECTIONS:
        new_pos = pos + direction
        if new_pos in maze:
            for next_pos in {new_pos, next_wall(pos, direction, maze)}:
                yield 1, next_pos

def part3_neighbors(state : tuple[Point, bool], maze : set[Point]):
    pos, on_portal = state

    portal_targets : set[Point] = set()
    neighbours : set[Point] = set()

    for direction in DIRECTIONS:
        new_pos = pos + direction
        if new_pos in maze:
            neighbours.add(new_pos)
            portal_targets.add(next_wall(new_pos, direction, maze))

    for neighbour in neighbours:
        yield 1, (neighbour, False)

    if len(neighbours) == 4:
        return
         

    portal_cost = 2 if on_portal else 3
    for portal_target in portal_targets:
        if portal_target != pos:
            yield portal_cost, (portal_target, True)

def bfs[S: Node, M](
    start : S,
    maze : M,
    neighbor_fn : Callable[[S,M], Iterable[tuple[int, S]]],
    end_condition : Callable[[S], bool]
) -> Optional[int]:
    queue = [(0, start)]
    seen : set[Point] = set()
    while queue:
        steps, state = heapq.heappop(queue)
        if end_condition(state):
            return steps
        if state in seen:
            continue
        seen.add(state)

        for cost, neighbor in neighbor_fn(state, maze):
            heapq.heappush(queue, (steps + cost, neighbor))

def parse_maze():
    start = end = None
    maze : set[Point] = set()
    for y,row in enumerate(sys.stdin):
        for x,c in enumerate(row.strip()):
            if c == 'S':
                start = Point(x,y)
            elif c == 'E':
                end = Point(x,y)
            if c != '#':
                maze.add(Point(x,y))
    assert start is not None
    assert end is not None
    return start, end, maze

def main():
    start, end, maze = parse_maze()
    print("part1 =", bfs(start, maze, neighbor_fn=part1_neighbors, end_condition = end.__eq__ ))
    print("part2 =", bfs(start, maze, neighbor_fn=part2_neighbors, end_condition = end.__eq__))
    print("part3 =", bfs((start, False), maze, neighbor_fn=part3_neighbors, end_condition = lambda pos : pos[0] == end))

if __name__ == "__main__":
    main()