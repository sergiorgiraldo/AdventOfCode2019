ADD = 1
MUL = 2
HALT = 99

class Computer:
    def __init__(self, code):
        self.code = code
        self.ip = 0
        self.max_ip = len(code)
        self.done = False

    def run(self):
        while True:
            op = self.code[self.ip]
            params = self.code[self.ip + 1: self.ip + 4]
            if op == ADD:
                p1 = self.get(params[0])
                p2 = self.get(params[1])
                out = params[2]
                self.code[out] = p1 + p2
                self.ip += 4

            if op == MUL:
                p1 = self.get(params[0])
                p2 = self.get(params[1])
                out = params[2]
                self.code[out] = p1 * p2
                self.ip += 4
            
            if op == HALT:
                self.done = True
                return
            
    def get(self, param):
        return self.code[param]