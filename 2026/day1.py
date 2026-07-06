import sys

def main():
    temperatures = tuple(map(int, sys.stdin.readlines()))

    part1 = sum(max(0, 60 - temperature) for temperature in temperatures)
    part2 = part1 + sum(max(0, temperature - 60) for temperature in temperatures) * 5


    n = len(temperatures)
    real_temperatures = temperatures[:n//2]
    target_temperatures = temperatures[n//2:]

    part3 = 0
    for real_temperature, target_temperature in zip(real_temperatures, target_temperatures):
        if real_temperature > target_temperature:
            part3 += 5 * (real_temperature - target_temperature)
        else:
            part3 += target_temperature - real_temperature

    print("part1 =", part1)
    print("part2 =", part2)
    print("part3 =", part3)


if __name__ == "__main__":
    main()