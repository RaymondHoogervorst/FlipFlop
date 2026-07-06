import sys

def main():
    lines = map(str.strip, sys.stdin.readlines())

    part1 = 0
    part2 = 0
    part3 = 0

    for line in lines:
        score = len(line) // 2
        part1 += score
        if score % 2 == 0:
            part2 += score
        if 'e' not in line:
            part3 += score

    print('part1 =', part1)
    print('part2 =', part2)
    print('part3 =', part3)

if __name__ == "__main__":
    main()