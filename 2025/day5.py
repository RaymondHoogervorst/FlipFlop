class TunnelNetwork:
    def __init__(self, string : str):
        self.n = len(string)
        self.labels = ['-' for _ in range(self.n)]
        self.exits = [0 for _ in range(self.n)]
        self.lengths : dict[str,int] = {}

        seen : dict[str,int] = {}
        for i,c in enumerate(string):
            self.labels[i] = c
            if (j := seen.pop(c, None)) is not None:
                self.exits[i] = j
                self.exits[j] = i
                self.lengths[c] = abs(i - j)
            else:
                seen[c] = i

    def traverse(self):
        position = 0
        while position < self.n:
            yield self.labels[position]
            position = self.exits[position] + 1

    def part1(self):
        return sum(map(self.lengths.get, self.traverse()))

    def part2(self):
        visited = set(self.traverse())
        result = []
        for c in self.labels:
            if c in visited:
                continue
            result.append(c)
            visited.add(c)
        return ''.join(result)

    def part3(self):
        result = 0
        for tunnel in self.traverse():
            if tunnel.isupper():
                result -= self.lengths[tunnel]
            else:
                result += self.lengths[tunnel]
        return result

def main():
    network = TunnelNetwork(input())
    print('part1 =', network.part1())
    print('part2 =', network.part2())
    print('part3 =', network.part3())

if __name__ == "__main__":
    main()
