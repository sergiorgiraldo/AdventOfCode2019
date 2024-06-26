from collections import deque
from copy import copy

#operations
ADD             = 1
MUL             = 2
INPUT           = 3
OUTPUT          = 4
JUMP_IF_TRUE    = 5
JUMP_IF_FALSE   = 6
LESS_THAN       = 7
EQUALS          = 8
RELATIVE_BASE   = 9
HALT            = 99

#modes
POSITION        = 0
IMMEDIATE       = 1
RELATIVE        = 2

#offsets
RELATIVE_OFFSET = {ADD:2, MUL:2, INPUT:0, LESS_THAN:2,EQUALS:2}

class InputInterrupted(Exception):
    pass

class OutputEmmitted(Exception):
    pass

class Computer:
    def __init__(self, code_):
        code      = copy(code_)          # always operate in own copy of code
        self.code = code + [0] * 10_000  # rqrmnt:available memory should be larger than the initial program
        
        self.ip = 0
        self.relative = 0
        self.max_ip = len(code)          # we get the ips from the code given (code != self.code)
        
        self.inputs  = deque()
        self.outputs = deque()
        
        self.done    = False
        self.waiting = False

    def run(self):
        while True:
            op = self.code[self.ip]
            op, modes = self.parse(op)
            params = self.code[self.ip + 1: self.ip + 5]

            if op == ADD:
                p1 = self.get(modes[0], params[0])
                p2 = self.get(modes[1], params[1])
                out = self.produce(op, params, modes)
                self.code[out] = p1 + p2
                self.ip += 4

            if op == MUL:
                p1 = self.get(modes[0], params[0])
                p2 = self.get(modes[1], params[1])
                out = self.produce(op, params, modes)
                self.code[out] = p1 * p2
                self.ip += 4
            
            if op == INPUT:
                out = self.produce(op, params, modes)
                try:
                    self.code[out] = self.inputs.popleft()
                    self.waiting = False
                except IndexError:
                    self.waiting = True
                    raise InputInterrupted #no more inputs, maybe ask for it
                else:
                    self.ip += 2
            
            if op == OUTPUT:
                p1 = self.get(modes[0], params[0])
                self.outputs.append(p1)
                self.ip += 2
                raise OutputEmmitted
            
            if op == JUMP_IF_TRUE:
                p1 = self.get(modes[0], params[0])
                p2 = self.get(modes[1], params[1])
                if p1:
                    self.ip = p2
                else:
                    self.ip += 3
            
            if op == JUMP_IF_FALSE:
                p1 = self.get(modes[0], params[0])
                p2 = self.get(modes[1], params[1])
                if not p1:
                    self.ip = p2
                else:
                    self.ip += 3
            
            if op == LESS_THAN:
                p1 = self.get(modes[0], params[0])
                p2 = self.get(modes[1], params[1])
                out = self.produce(op, params, modes)
                self.code[out] = 1 if p1 < p2 else 0
                self.ip += 4
            
            if op == EQUALS:
                p1 = self.get(modes[0], params[0])
                p2 = self.get(modes[1], params[1])
                out = self.produce(op, params, modes)
                self.code[out] = 1 if p1 == p2 else 0
                self.ip += 4
            
            if op == RELATIVE_BASE:
                p1 = self.get(modes[0], params[0])
                self.relative += p1
                self.ip += 2
            
            if op == HALT:
                self.done = True
                return

    def parse(self, op):
        try:
            mode3, op = divmod(op, 10000)
            mode2, op = divmod(op, 1000)
            mode1, op = divmod(op, 100)

            return op, [mode1, mode2, mode3]
        except:
            raise Exception(f"Cant parse opcode: {op}")

    def get(self, mode, param) -> int:
        if mode == IMMEDIATE:
            return param
        elif mode == POSITION:
            try:
                return self.code[param]
            except IndexError:
                raise (f"No param found at position {param}")
        elif mode == RELATIVE:
            return self.code[self.relative + param]
        else:
            raise ValueError(f"Unknown mode: {mode}")
  
    def produce(self, op, params, modes):
        try:
            offset = RELATIVE_OFFSET[op]
            return params[offset] if modes[offset] != RELATIVE else self.relative + params[offset]
        except:
            raise Exception(f"Cant determine output for: op-> {op} / params-> {params} / modes-> {modes}")

if __name__ == "__main__":
    code_ = input("Enter the program as comma separated values\n>>> ")
    code = [int(op) for op in code_.split(",")]
    computer = Computer(code)
    
    input_value = input("Enter the input as comma separated values\n>>> ")
    if input_value != "":
        for i in input_value.split(","):
            computer.inputs.append(int(i))
    
    while not computer.done:
        try:
            computer.run()
        except InputInterrupted:
            inp = int(input("Enter input: "))
            computer.inputs.append(inp)
        except OutputEmmitted:
            print(computer.outputs[-1])