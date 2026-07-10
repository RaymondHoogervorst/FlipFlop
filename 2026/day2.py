WALL_SIZE = 100

def part1(movements : tuple[int]):
    walls = [0] * WALL_SIZE
    robot_pos = 0

    for movement in movements:
        robot_pos = (robot_pos + movement) % WALL_SIZE
        walls[robot_pos] += 1

    max_value = max(walls)
    max_i = walls.index(max_value) + 1
    return max_value * max_i

def part2(movements : tuple[int]):
    wall_temp = 0
    wall_pos = 0
    robot_pos = 0
    n = len(movements)

    for i in range(n):
        robot_pos = (robot_pos + movements[i]) % WALL_SIZE
        wall_pos = (wall_pos + movements[-i-1]) % WALL_SIZE
        if wall_pos == robot_pos:
            wall_temp += 1

    return wall_temp

def part3(movements : tuple[int]):
    n = len(movements)
    walls = [0] * WALL_SIZE
    robot_pos = 0

    for i in range(n):
        robot_pos = (robot_pos + movements[i] - movements[-i-1]) % WALL_SIZE
        walls[robot_pos] += 1

    max_value = max(walls)
    max_i = walls.index(max_value) + 1
    return max_value * max_i

def main():
    movements = tuple(1 if c == '>' else -1 for c in input())
    print("part1 =", part1(movements))
    print("part2 =", part2(movements))
    print("part3 =", part3(movements))


if __name__ == "__main__":
    main()