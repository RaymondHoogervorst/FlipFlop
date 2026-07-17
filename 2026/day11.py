import sys, itertools, re, bisect

class DnaRule:
    def __init__(self, top : str, left : str, right : str):
        self.top = None if top == 'XX' else int(top)
        self.left = None if left == 'XX' else int(left)
        self.right = None if right == 'XX' else int(right)

class Forest:
    def __init__(self, configurations : tuple[tuple[DnaRule]]):
        self.n = len(configurations)
        seeds = tuple(range(0, 10 * self.n, 10))

        self.age = 0
        self.stem_columns = {}
        self.occupied = {(0,x) for x in seeds}
        self.sprouts = [{(0,x) : 0} for x in seeds]
        self.biomass = [1] * self.n
        self.sunlight = [0] * self.n
        self.alive_trees = [True] * self.n

        self.configurations = configurations

    def reproduce(self):
        fallen_spouts = {}

        for dna_i, sprouts in enumerate(self.sprouts):
            for y,x in sprouts.keys():
                if x not in fallen_spouts or fallen_spouts[x][0] < y:
                    fallen_spouts[x] = (y,dna_i)
        seeds = sorted(fallen_spouts)

        self.age = 0
        self.stem_columns = {}
        self.n = len(seeds)
        self.occupied = {(0,x) for x in seeds}
        self.sprouts = [{(0,x) : 0} for x in seeds]
        self.biomass = [1] * self.n
        self.sunlight = [0] * self.n
        self.alive_trees = [True] * self.n
        self.configurations = [self.configurations[fallen_spouts[seed][1]] for seed in seeds]

    def alive(self):
        if self.age < 5:
            return True
        if self.age > 100:
            return False
        return self.age < 5 or (any(self.alive_trees) and self.age < 100)

    def step_tree(self, tree_i):
        if not self.alive_trees[tree_i]:
            return
        configuration = self.configurations[tree_i]
        tree_sprouts = self.sprouts[tree_i]

        next_sprouts = {}
        for (y,x),sprout_id in tree_sprouts.items():
            rule = configuration[sprout_id]
            for ny,nx,next_sprout_id in ((y+1,x,rule.top),(y,x-1,rule.left),(y,x+1,rule.right)):
                next_pos = (ny,nx)
                if next_sprout_id is None or next_pos in self.occupied:
                    continue
                next_sprouts[next_pos] = max(next_sprouts.get(next_pos, 0), next_sprout_id)
            bisect.insort_left(self.stem_columns.setdefault(x,[]), (y,tree_i))
        self.occupied.update(next_sprouts.keys())

        self.biomass[tree_i] += len(next_sprouts)
        self.sprouts[tree_i] = next_sprouts

    def step(self):
        for i in range(self.n):
            self.step_tree(i)

        self.age += 1

        if self.age < 5:
            return

        self.sunlight = [0] * self.n

        for column in self.stem_columns.values():
            for i,(y,tree_i) in enumerate(column[:-4:-1]):
                self.sunlight[tree_i] += min(y+1,10) * (3 - i)

        for tree_i in range(self.n):
            if self.alive_trees[tree_i] and self.sunlight[tree_i] < (self.biomass[tree_i] * 3):
                self.alive_trees[tree_i] = False


    def run(self):
        while self.alive():
            self.step()

    def calculate_total_biomass(self, generations=1):
        for i in range(generations):
            if i:
                self.reproduce()
            self.run()
        return sum(self.biomass)


def parse_rules(top_line : str, bottom_line : str):
    pattern = re.compile(r'XX|\d{2}')
    top_labels = pattern.findall(top_line)
    bottom_labels = pattern.findall(bottom_line)
    return tuple(DnaRule(top,left,right) for top, (left, _, right) in zip(top_labels, itertools.batched(bottom_labels, 3)))

def main():
    configurations = tuple(parse_rules(lineA,lineB) for lineA, lineB, *_ in itertools.batched(sys.stdin.readlines(), 3))

    part1 = sum(Forest((configuration,)).calculate_total_biomass() for configuration in configurations)
    part2 = Forest(configurations).calculate_total_biomass()
    part3 = Forest(configurations).calculate_total_biomass(generations=3)

    print('part1 =', part1)
    print('part2 =', part2)
    print('part3 =', part3)

if __name__ == "__main__":
    main()