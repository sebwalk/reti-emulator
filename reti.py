# Quick and dirty ReTi instruction set Emulator
# Author: Sebastian Walker (https://sebastianwalker.org)
# Inspired by Vorlesung Technische Informatik, SoSe 21
# Prof. Dr. Christoph Scholl, Universität Freiburg

import sys

s = dict()
acc = 0
ind = dict()
pc = 0


def LOAD(i):
    global acc, pc
    acc = s[i]
    pc += 1


def LOADI(i):
    global acc, pc
    acc = i
    pc += 1


def STORE(i):
    global pc
    s[i] = acc
    pc += 1


def ADD(i):
    global acc, pc
    acc += s[i]
    pc += 1


def SUB(i):
    global acc, pc
    acc -= s[i]
    pc += 1


def ADDI(i):
    global acc, pc
    acc += i
    pc += 1


def SUBI(i):
    global acc, pc
    acc -= i
    pc += 1


def LOADIN(j, i):
    global acc, pc
    acc = s[ind[j] + i]
    pc += 1


def STOREIN(j, i):
    global pc
    s[ind[j] + i] = acc
    pc += 1


def MOVE(st, d):
    global pc
    set_value_to(d, get_value_from(st))
    if d != 'pc':
        pc += 1


def JUMP(i):
    global pc
    pc += i


def JUMPC(conditional, i):
    global pc
    pc = pc + i if should_jump(conditional) else pc + 1


def PRINT(i):
    global pc
    print(s[i])
    pc += 1


def get_value_from(st):
    st = st.lower()

    if st == 'acc':
        return acc

    if st == 'in1':
        return ind[1]

    if st == 'in2':
        return ind[2]

    if st == 'pc':
        return pc


def set_value_to(d, value):
    d = d.lower()

    global acc, ind, pc
    if d == 'acc':
        acc = value

    if d == 'in1':
        ind[1] = value

    if d == 'in2':
        ind[2] = value

    if d == 'pc':
        pc = value


def should_jump(conditional):
    if conditional == '<':
        return acc < 0

    if conditional == '=':
        return acc == 0

    if conditional == '>':
        return acc > 0

    if conditional == '<=':
        return acc <= 0

    if conditional == '!=':
        return acc != 0

    if conditional == '>=':
        return acc >= 0

    raise NotImplementedError(f'conditional jump JUMPC {conditional} using invalid condition {conditional}')


def read_instructions():
    path = sys.argv[1] if len(sys.argv) > 1 else 'examples/multiply.txt'
    file = open(path, 'r')
    lines = file.readlines()
    return [line.split("#")[0].strip().split(" ") for line in lines
            if not line.startswith('#') and line.strip() != ""]


def execute_instruction(instruction):
    pc_before = pc

    name = instruction[0]
    arg1 = prepare_argument(instruction[1])

    if len(instruction) > 2:
        arg2 = prepare_argument(instruction[2])
        globals()[name](arg1, arg2)
    else:
        globals()[name](arg1)

    return pc_before == pc


def prepare_argument(value):
    try:
        return int(value)
    except ValueError:
        return value


def run():
    instructions = read_instructions()
    verbose = len(sys.argv) > 2

    while True:
        if pc >= len(instructions):
            print("Instruction for PC = " + str(
                pc) + " does not exist, aborting")
            break

        instruction = instructions[pc]

        if verbose:
            print(instruction)

        looped = execute_instruction(instruction)

        if looped:
            break


run()
