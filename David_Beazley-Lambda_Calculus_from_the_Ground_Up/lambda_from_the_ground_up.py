#%%
def RIGHT(a):
    def f(b):
        return a
    return f

def LEFT(a):
    def f(b):
        return b
    return f

print(RIGHT("RED")("GREEN")) # should be GREEN
print(LEFT("RED")("GREEN")) # should be RED

#%% 
# Implementing simple boolean algebra rules in lambda calculus.

def TRUE(x):
    return lambda y:x

def FALSE(x):
    return lambda y:y

def NOT(x):
    return x(FALSE)(TRUE)

assert NOT(TRUE) is FALSE
assert NOT(FALSE) is TRUE

def OR(x):
    return lambda y : x(x)(y)

assert OR(TRUE)(FALSE) is TRUE
assert OR(FALSE)(FALSE) is FALSE
assert OR(TRUE)(TRUE) is TRUE

def AND(x):
    return lambda y : x(y)(x)

assert AND(TRUE)(FALSE) is FALSE
assert AND(FALSE)(FALSE) is FALSE
assert AND(TRUE)(TRUE) is TRUE

#%%
# lets do numbers

ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))
TREE = lambda f: lambda x: f(f(f(x)))

# visualize stuff a bit with integers
incr = lambda x : x + 1 # illegal in rules

print(incr(0))
print(ONE(incr)(0))
print(TREE(incr)(0))
print(ZERO(incr)(0))

#%%
# special print function not in talk
printNumber = lambda x: x(incr)(0)

SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
print(SUCC(ONE)(incr)(0)) # a number is function of a function ...
FOUR = SUCC(TREE)
FIVE = SUCC(FOUR)
SIX  = SUCC(FIVE)

# add number n and m
ADD = lambda n: lambda m: n(SUCC)(m)
printNumber(ADD(ONE)(TWO)) # 1+2=3 

MUL = lambda n: lambda m: lambda f: n(m(f))
printNumber(MUL(TREE)(TWO)) # 1+2=3 

#%% Define functions for representing a simple data structure (pair)

# (cons 2 3) -> (2,3) 
# (car p)    -> 2 
# (cdr p)    -> 3

def cons(a,b):
    def select(m):
        if m ==0:
            return a
        elif m==1:
            return b
    return select

def car(p):
    return p(0)

def cdr(p): # works only with pairs obviously
    return p(1)

CONS = lambda a: lambda b: lambda s: s(a)(b)
CAR = lambda p: p(TRUE)
CDR = lambda p: p(FALSE)

p = CONS(TRUE)(FALSE)

#%% How about doing substraction

# (1, 0)
# (2, 1)
# (3, 2)
# (4, 3) <- W
# (5, 4)

T = lambda p: CONS(SUCC(CAR(p)))(CAR(p))
W = FOUR(T)(CONS(ZERO)(ZERO))

printNumber(CAR(W))
printNumber(CDR(W))

PRED = lambda n: CDR(n(T)(CONS(ZERO)(ZERO)))
printNumber(PRED(FOUR))

# SUB(x)(y) = x - y
SUB = lambda x: lambda y: y(PRED)(x)
printNumber(SUB(TREE)(ONE))

#%%

# ISZERO = lambda n: n(AND(FALSE))(TRUE) # <- my own attempt before viewing the answer
ISZERO = lambda n: n(lambda f: FALSE)(TRUE)

#%% recursion -> factorial

# def fact(n):
#     if n ==0 : 
#         return 1
#     else : 
#         return n*fact(n-1)

FACT = lambda n: ISZERO(n)\
    (ONE)\
    (MUL(n)(FACT(PRED(n))))

#%% demo eager evaluation python
def CHOOSE(t,a,b):
    if t:
        return a
    else :
        return b

a =0
CHOOSE(a==0,a,1/a)

#%%

LAZY_TRUE = lambda x: lambda y: x()
LAZY_FALSE = lambda x: lambda y: y()
ISZERO_LAZY = lambda n: n(lambda f: LAZY_FALSE)(LAZY_TRUE)

FACT = lambda n: ISZERO_LAZY(n)\
    (lambda: ONE)\
    (lambda: MUL(n)(FACT(PRED(n))))

# fact(4)=24
printNumber(FACT(FOUR))
#%% no globals -> how to do recursion with the name?

# repeat yourself trick
fact =  (lambda f: lambda n: 1 if n==0 else n*f(f)(n-1)) \
        (lambda f: lambda n: 1 if n==0 else n*f(f)(n-1))
fact(4)

#%%

# original
fact = lambda n: 1 if n==0 else n*fact(n-1)

# variable name trick
fact = (lambda f: lambda n: 1 if n==0 else n*f(n-1))(fact)

# take out the middle
R =  (lambda f: lambda n: 1 if n==0 else n*f(n-1))

# now you get this
# fact = R(fact)
# Y(R) = R(Y(R)) -> replacing fact
# 
# Recursion trick

# Y(R) = (lambda x: R(x))(Y(R))
# Y(R) = (lambda x: R(x))(lambda x: R(x)) -> repeat yourself trick
# Y(R) = (lambda x: R(x(x)))(lambda x: R(x(x)))
# Y(R) = (lambda f: (lambda x: f(x(x)))(lambda x: f(x(x))))(R)

Y = (lambda f: (lambda x: f(x(x)))(lambda x: f(x(x))))

# this gives you again the inf-recusion problem
Y(R)

#%%
# take out the same R but fix Y with lazy eval trick
R = (lambda f: lambda n: 1 if n==0 else n*f(n-1))
Y = (lambda f: (lambda x: f( lambda z: x(x)(z)))(lambda x: f(lambda z: x(x)(z))))

fact = Y(R)

fact(4)