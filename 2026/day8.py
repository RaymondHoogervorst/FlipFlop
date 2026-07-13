import sys
from functools import cache
from itertools import pairwise

def part1(evolutions : tuple[str]):
    evolution_map : dict[str, tuple[str]] = {}
    for start, *children in evolutions:
        evolution_map.setdefault(start, children)

    @cache
    def count_evolutions(c : str, k : int):
        if k == 0:
            return 1
        return sum(count_evolutions(child, k-1) for child in evolution_map.get(c, (c,)))
    return count_evolutions('A', 7) + count_evolutions('B', 7)

def part2(evolutions : tuple[tuple[str]], k = 7):
    evolution_map : dict[str, tuple[str]] = {}
    for lhs, rhs, *children in evolutions:
        evolution_map.setdefault((lhs, rhs), children)

    @cache
    def count_evolutions(lhs : str, rhs : str, k : int):
        if k == 0:
            return 0
        children = evolution_map.get((lhs, rhs)) or evolution_map.get((rhs,lhs))
        if children is None:
            return 0
        new_strain = (lhs, *children, rhs)
        return len(children) + sum(count_evolutions(a,b,k-1) for a,b in pairwise(new_strain))
    return 2 + count_evolutions('A', 'B', k)

def main():
    evolutions = tuple(tuple(line.split()) for line in sys.stdin.readlines())

    print("part1 =", part1(evolutions))
    print("part2 =", part2(evolutions))
    print("part3 =", part2(evolutions, 21))

if __name__ == "__main__":
    main()