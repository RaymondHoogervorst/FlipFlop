import sys, typing

def parse_flower():
    lines = tuple(map(str.strip, sys.stdin.readlines()))[3:-1]
    leaves : typing.List[int] = []
    for line in reversed(lines):
        if line.startswith('o-|'):
            leaves.append(-1)
        elif line.endswith('|-o'):
            leaves.append(1)
        else:
            leaves.append(0)
    return tuple(leaves)



def main():
    flower = parse_flower()
    print('part1 =', sum(map(bool, flower[400:])))

    leaves = tuple(filter(bool, flower))
    print('part2 =', sum(leaves[i] != leaves[i+1] for i in range(len(leaves) - 1)))

    part3 = 0
    while leaves:
        leaves = tuple(leaves[i] for i in range(len(leaves) - 1) if leaves[i] == leaves[i+1])
        part3 += 1
    print('part3 =', part3)

if __name__ == "__main__":
    main()