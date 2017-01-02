import sys

class Interpreter():
    TOKENS = {
        '<': lambda state: state.chMemPtr(-1),
        '>': lambda state: state.chMemPtr(1),
        '+': lambda state: state.chMem(1),
        '-': lambda state: state.chMem(-1),
        '.': lambda state: state.printMem(),
        ',': lambda state: state.inputMem(),
        '[': '',
        ']': ''
    }

    # init the class with a string, which is tokenized and parsed
    def __init__(self, content):
        self.program = self.parse(self.tokenize(content));
        self.mem = [0]
        self.mem_ptr = 0
        self.pp_stack = [0]

        # reference to the current loop we are in
        self.context = self.program


    # change the memory pointer
    def chMemPtr(self, amount):
        self.mem_ptr += amount
        if len(self.mem) < self.mem_ptr + 1:
            self.mem.extend([0] * (self.mem_ptr + 1 - len(self.mem)))

        if self.mem_ptr < 0:
            print("memory pointer < 0")
            exit()

    # change the memory cell
    def chMem(self, amount):
        self.mem[self.mem_ptr] += amount

        if self.mem[self.mem_ptr] < 0:
            print("memory < 0 at pos " + str(self.mem_ptr))
            exit()

    # output current memory cell as ascii
    def printMem(self):
        print(chr(self.mem[self.mem_ptr]), end="")

    # read number in memory cell
    def readMem(self):
        content = -1

        while content < 0:
            tmp = input("input memory cell content")
            try:
                content = int(tmp)
            except:
                content = -1

        self.mem[self.mem_ptr] = content


    # execute the next command at pp_stack[-1]
    def nextCmd(self):
        # check for end of program
        if len(self.pp_stack) == 1 and self.pp_stack[-1] >= len(self.program):
            return False

        # if there are still commands in the current context
        if self.pp_stack[-1] < len(self.context):
            if isinstance(self.context[self.pp_stack[-1]], list):
                # context switch
                self.context = self.context[self.pp_stack[-1]]
                self.pp_stack.append(-1)
            else:
                # normal command execution
                self.TOKENS[self.context[self.pp_stack[-1]]](self)
        else:
            # check if for end of the program
            if len(self.pp_stack) == 1:
                    return False

            # otherwise we check if we repeat the loop, or jump to parent context
            if self.mem[self.mem_ptr] == 0:
                # pop current program pointer and set parent context
                self.pp_stack.pop()
                # short validy check
                if len(self.pp_stack) == 0:
                    print("error exited main context due to unbalanced brackets")
                    exit()

                # set context
                self.context = self.program
                for i in self.pp_stack[1:]:
                    self.context = self.context[i]
            else:
                self.pp_stack[-1] = -1

        # increase current program pointer
        self.pp_stack[-1] += 1

        # True indicates that the program is still running
        return True



    # run a specific amount of commands
    def run(self, amount = -1):
        if amount < 0:
            # run indefinitely
            while self.nextCmd():
                continue
        else:
            # run amount times
            for i in range(amount):
                if self.nextCmd() == False:
                    return


    # remove unwanted characters
    def tokenize(self, content):
        tokens = []

        for char in content:
            # ignore all other chars which are not tokens
            if not char in self.TOKENS:
                continue
            tokens.append(char)

        return tokens


    # check for balanced loops and create nested arrays for loops
    def parse(self, tokens):
        program = [[]]
        i = 0

        for t in tokens:
            if t == '[':
                program.append([])

                # next char
                continue

            if t == ']':
                # check if at least one bracket was opened
                if len(program) == 1:
                    print("unbalenced brackets at char position " + str(i))
                    print(program[0])
                    exit()

                # pop last element from programm
                loop = program.pop()

                # insert popped element in now last element of program
                program[-1].append(loop)

                # next char
                continue

            # otherwise add current char to last list in program
            program[-1].append(t)

            i += 1


        if len(program) > 1:
            print("whole program parsed, found unbalanced brackets")
            print(program[0])
            exit()

        return program[0]



# main program
if len(sys.argv) < 2:
    print('no source file provided')
    exit()

with open(sys.argv[1], 'r') as f:
    content = f.read()
    interpreter = Interpreter(content)
    interpreter.run()
