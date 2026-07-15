import sys, dataclasses 

@dataclasses.dataclass
class Script:
    labels : dict[int,int]
    instructions : tuple[tuple[int]]

class Program:
    MODULO = 2 ** 16

    def __init__(self, script : Script):
        self.script = script
        self.reg = [0] * 16
        self.pc = 0
        self.done = False

    def step(self):
        assert not self.done
        match self.script.instructions[self.pc]:
            case 0, val, dest_reg:
                self.reg[dest_reg] = val % self.MODULO
            case 1, src_reg, des_reg:
                self.reg[des_reg] = self.reg[src_reg]
            case 2, src_reg1, src_reg2, des_reg:
                self.reg[des_reg] = (self.reg[src_reg1] + self.reg[src_reg2]) % self.MODULO
            case 3, src_reg1, src_reg2, des_reg:
                self.reg[des_reg] = (self.reg[src_reg1] - self.reg[src_reg2]) % self.MODULO
            case 4, src_reg1, src_reg2, des_reg:
                self.reg[des_reg] = (self.reg[src_reg1] * self.reg[src_reg2]) % self.MODULO
            case 5, src_reg1, src_reg2, des_reg:
                if self.reg[src_reg2] == 0:
                    self.reg[des_reg] = 0
                else:
                    self.reg[des_reg] = self.reg[src_reg1] % self.reg[src_reg2]
            case 6, reg:
                self.reg[reg] = (self.reg[reg] + 1) % self.MODULO
            case 7, reg:
                self.reg[reg] = (self.reg[reg] - 1) % self.MODULO
            case 8, label:
                self.pc = self.script.labels[label] - 1
            case 9, reg, label:
                if self.reg[reg] == 0:
                    self.pc = self.script.labels[label] - 1
            case 10, reg, label:
                if self.reg[reg] != 0:
                    self.pc = self.script.labels[label] - 1
        self.pc += 1
        if self.pc >= len(self.script.instructions):
            self.done = True

    def run(self):
        while not self.done:
            self.step()
    
    def run_with_limit(self, limit : int):
        for _ in range(limit):
            if self.done:
                return
            self.step()


def parse_instructions():
    labels : dict[int,int] = {}
    instructions : list[tuple[int]] = []

    for line in sys.stdin.readlines():
        prefix = line[:2]
        core = line[2:].strip()

        if prefix == 'be':
            labels[len(core) // 2] = len(instructions)
        else:
            instructions.append(tuple(len(segment) // 2 for segment in core.split('ne')))

    return Script(labels, tuple(instructions))

def main():
    script = parse_instructions()

    labels = [0] * len(script.instructions)
    for label, pos in script.labels.items():
        labels[pos] = label

    program = Program(script)
    program.run()
    print("part1 =", program.reg[0])

    part2 = 0
    for starting_val in range(100):
        program = Program(script)
        program.reg[0] = starting_val
        program.run_with_limit(5_000_000)
        if not program.done:
            part2 += 1

    print("part2 =", part2)

    # The value in reg[0] is always divided modulo 16 near the start of the program.
    # Thus the pattern repeats every 16 values of reg[0]
    part3 = 0
    for reg0 in range(16):
        for reg1 in range(16):
            program = Program(script)
            program.reg[0] = reg0
            program.reg[1] = reg1
            program.run_with_limit(5_000_000)
            if not program.done:
                part3 += 1

    # 65536 divided by 16 equals 4096
    print("part3 =", part3 * 4096)

if __name__ == "__main__":
    main()