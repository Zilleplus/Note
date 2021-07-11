import struct as struct

class Function:
    def __init__(self, nparams, returns,code):
        self.nparams = nparams
        self.returns = returns
        self.code = code

class Stack:
    def __init__(self, functions,  memsize=65536):
        self.items = []
        self.memory = bytearray(memsize)
        self.functions = functions

    def load(self, addr):
        return struct.unpack('<d', self.memory[addr:addr+8])[0]

    def store(self, addr,val):
        self.memory[addr:addr+8] = struct.pack('<d', val)

    def push(self,item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def call(self,func,*args):
        locals = dict(enumerate(args)) # { 0: args{0], 1: args[1], 2: args[2] }
        self.execute(func.code, locals)
        if func.returns: 
            return self.pop()

    """
    Execute some code on the stack machine,

    Instructions are of form: (operation, arguments)

    Possible operations are:
        - const: push constant number on stack
            * has 1 argument: the number itself
        - add: pop off last 2 numbers add them together,
            the push the result on the stack
            * has no arguments
        - mul: pop off last 2 numbers multiply them together,
            the push the result on the stack
            * has no arguments
        - call: execute a function
    """
    def execute(self,instructions):
        for op,*args in instructions:
            print(op, args, self.items)
            if op == 'const':
                self.push(args[0])
            elif op == 'add':
                right = self.pop()
                left = self.pop()
                self.push(left+right)
            elif op == 'mul':
                right = self.pop()
                left = self.pop()
                self.push(left*right)
            elif op == 'load':
                addr = self.pop()
                self.push(self.load(addr))
            elif op == 'store':
                val = self.pop()
                addr = self.pop()
                self.store(addr,val)
            elif op == 'local.get':
                self.push(locals[args[0]])
            elif op == 'local.set':
                locals[args[0]] = self.pop()
            elif op == 'call':
                func = self.functions[args[0]]
                fargs = reversed([ self.pop() for _ in range(func.nparams)])
                result = self.call(func, *fargs)
                if func.returns:
                    self.push(result)
            else:
                raise RunTimeError(f'Bad op {op}')

def example():
    # compute 2+3*0.1 = 2.3
    # x =2 
    # v = 3
    # x = x + v*0.1
    x_addr =22
    y_addr = 42

    code = \
        [\
         ('const',22),\
         ('const',22),\
         ('load',),\
         ('const',42),\
         ('load',),\
         ('const',0.1),\
         ('mul',),\
         ('add',),\
         ('store',)\
         ]
    s = Stack()
    s.store(x_addr,2.0)
    s.store(y_addr,3.0)
    s.execute(code)
    print("Result",str(s.load(x_addr)))

if __name__ == '__main__':
    example()

