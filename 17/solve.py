#!/usr/bin/env python3

import re
from dataclasses import dataclass, field


@dataclass
class CPU:
    a: int
    b: int
    c: int
    program: list[int]
    ip: int = 0
    output: list = field(default_factory=list)

    def tick(self):
        instruction, operand = self.program[self.ip : self.ip + 2]

        match instruction:
            case 0:
                self.a //= 2 ** self.get_operand(operand)

            case 1:
                self.b ^= operand

            case 2:
                self.b = self.get_operand(operand) % 8

            case 3:
                self.ip = operand - 2 if self.a != 0 else self.ip

            case 4:
                self.b ^= self.c

            case 5:
                self.output.append(self.get_operand(operand) % 8)

            case 6:
                self.b = self.a // (2 ** self.get_operand(operand))

            case 7:
                self.c = self.a // (2 ** self.get_operand(operand))

        self.ip += 2

    def get_operand(self, operand):
        if operand in range(0, 4):
            return operand

        if operand == 4:
            return self.a

        if operand == 5:
            return self.b

        if operand == 6:
            return self.c

        else:
            raise KeyError

    def run(self):
        while True:
            try:
                self.tick()
            except ValueError:
                break
        return self.output


def solve(cpu):
    return ",".join(map(str, cpu.run()))


def parse(data):
    a = int(re.search("Register A: (?P<a>\d+)", data).group("a"))
    b = int(re.search("Register B: (?P<b>\d+)", data).group("b"))
    c = int(re.search("Register C: (?P<c>\d+)", data).group("c"))
    program = list(
        map(
            int, re.search("Program: (?P<program>.+)", data).group("program").split(",")
        )
    )
    return CPU(a, b, c, program)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", "4,6,3,5,6,3,5,2,1,0")
    main("input.txt")
