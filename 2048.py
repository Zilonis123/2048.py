#coding=utf8
#Wei Guannan <kiss.kraks@gmail.com>

import copy
import random
from colorama import Fore, Back, init
from functools import reduce
import numpy as np

def mapReplacement(fun, iter):
    res = []
    for i in iter:
        res.append(fun(i))
    return res

def reduceLineLeft(xs): 
    def aux(acc, y):
        if len(acc) == 0: acc.append(y)
        elif acc[len(acc)-1] == y:
            acc[len(acc)-1] = y * 2
            acc.append(0)
        else: acc.append(y)
        return acc
    res = list(filter(lambda x: x !=0, reduce(aux, filter(lambda x: x!=0, xs), [])))
    res.extend([0 for i in range(0, len(xs)-len(res))])
    return res

def reduceLineRight(xs):
    return reduceLineLeft(xs[::-1])[::-1]

def reduceLeft(a):
    
    return mapReplacement(reduceLineLeft, a)

def reduceRight(a):
    return mapReplacement(reduceLineRight, a)

def reduceUp(a):
    return rotate(reduceRight(rotate(a)))

def reduceDown(a):
    return rotate(reduceLeft(rotate(a)))

def rotate(a):
    rotatedt = list(reversed(list(zip(*a[::-1]))))
    # rotated is a tuple right now, but we need it as an array
    rotated = []
    for t in rotatedt:
        a = list(t)
        rotated.append(a)
    # print(rotated)
    return rotated

def prettyPrint(a):
    def color(x):
        if x == 0:    return Fore.RESET + Back.RESET
        if x == 2:    return Fore.RED + Back.RESET
        if x == 4:    return Fore.GREEN + Back.RESET
        if x == 8:    return Fore.YELLOW + Back.RESET
        if x == 16:   return Fore.BLUE + Back.RESET
        if x == 32:   return Fore.MAGENTA + Back.RESET
        if x == 64:   return Fore.CYAN + Back.RESET
        if x == 128:  return Fore.RED + Back.BLACK
        if x == 256:  return Fore.GREEN + Back.BLACK
        if x == 512:  return Fore.YELLOW + Back.BLACK
        if x == 1024: return Fore.BLUE + Back.BLACK
        if x == 2048: return Fore.MAGENTA + Back.BLACK
        if x == 4096: return Fore.CYAN + Back.BLACK
        if x == 8192: return Fore.WHITE + Back.BLACK

    # print out the game

    text = ""
    for i in a:
        for j in i:
            text += color(j) + ("%4d" % j) + Fore.RESET + Back.RESET
        text += "\n"
    print(text)

def newEmpty(size):
    return [[0 for i in range(0, size)] for i in range(0, size)]

def isWin(a):
    return traverse(a, lambda x: x == 2048)

def isFail(a):
    def aux(a):
        for i in a:
            for j in zip(i, i[1:]):
                if j[0] == 0 or j[1] == 0 or j[0] == j[1]: return False
        return True
    return aux(a) and aux(rotate(a))
    
def traverse(a, f):
    for line in a:
        for ele in line:
            if f(ele): return True
    return False

def randomPoint(size):
    x = random.randint(0, size)
    y = random.randint(0, size)
    return (x, y)

def randomInit(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    v = random.randint(0, len(seed)-1)
    a[x][y] = seed[v]

def randomNum(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    if a[x][y] == 0:
        v = random.randint(0, len(seed)-1)
        a[x][y] = seed[v]
    else: randomNum(a)

def newGame(size):
    print ("press w to move up, a to move left, s to move down, d to move right.")
    print ("press q to quit.")
    won = False

    # Generate empty map
    a = newEmpty(size)
    # add to random values
    randomInit(a)
    randomInit(a)
    # print the map
    prettyPrint(a)
    # start the game loop
    while True:
        b = copy.deepcopy(a)
        key = input()
        if key == "w":   a = reduceUp(a)
        elif key == "a": a = reduceLeft(a)
        elif key == "s": a = reduceDown(a)
        elif key == "d": a = reduceRight(a)
        elif key == "q": break
        if a == b: 
            print ("no numbers to be reduce")
        else: randomNum(a)
        prettyPrint(a)
        if isWin(a) and not won:
            print ("You win")
            won = True
        elif isFail(a):
            print ("You fail")
            break

def test():
    assert reduceLineLeft([4, 4, 4, 4]) == [8, 8, 0, 0]
    assert reduceLineLeft([0, 0, 0, 0]) == [0, 0, 0, 0]
    assert reduceLineLeft([2, 0, 2, 0]) == [4, 0, 0, 0]
    assert reduceLineLeft([2, 0, 0, 2]) == [4, 0, 0, 0]
    assert reduceLineLeft([2, 2, 0, 2]) == [4, 2, 0, 0]
    assert reduceLineLeft([4, 0, 2, 2]) == [4, 4, 0, 0]
    assert reduceLineLeft([2, 0, 2, 2]) == [4, 2, 0, 0]
    assert reduceLineLeft([2, 2, 8, 8]) == [4, 16, 0, 0]
    assert reduceLineRight([2, 2, 0, 2]) == [0, 0, 2, 4]
    assert reduceLineRight([0, 0, 0, 2]) == [0, 0, 0, 2]
    assert reduceLineRight([2, 0, 0, 2]) == [0, 0, 0, 4]
    assert reduceLineRight([4, 4, 2, 2]) == [0, 0, 8, 4]
    assert reduceLineRight([2, 4, 4, 2]) == [0, 2, 8, 2]
    
if __name__ == "__main__":
    init()

    newGame(4)
