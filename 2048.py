#coding=utf8
#Wei Guannan <kiss.kraks@gmail.com>

import copy
import random
from colorama import Fore, Back, init
from functools import reduce
import pygame as p

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
    WIDTH = HEIGHT = 512
    won = False
    MAX_FPS = 30

    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("2048")
    clock = p.time.Clock()

    # Generate empty map
    a = newEmpty(size)
    # add to random values
    randomInit(a)
    randomInit(a)
    # print the map
    # prettyPrint(a)
    # start the game loop
    running = True
    while running:
        b = copy.deepcopy(a)
        # key = input()
        # if key == "w":   a = reduceUp(a)
        # elif key == "a": a = reduceLeft(a)
        # elif key == "s": a = reduceDown(a)
        # elif key == "d": a = reduceRight(a)
        # elif key == "q": break
        # if a == b: 
        #     print ("no numbers to be reduce")
        # else: randomNum(a)
        # prettyPrint(a)
        # if isWin(a) and not won:
        #     print ("You win")
        #     won = True
        # elif isFail(a):
        #     print ("You fail")
        #     break
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            if e.type == p.KEYDOWN:
                if e.key == p.K_w:
                    a = reduceUp(a)
                elif e.key == p.K_s:
                    a = reduceDown(a)
                elif e.key == p.K_a:
                    a = reduceLeft(a)
                elif e.key == p.K_d:
                    a = reduceRight(a)
        # Check if the board moved
        if a != b:
            # if it did add a number
            randomNum(a)

        drawScreen(screen, a, WIDTH, HEIGHT, size)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawScreen(screen, game, w, h, s):
    drawBoard(screen, w, h, s, game)

def drawBoard(screen, w, h, size, game):
    MIDDLE = (w/2, h/2)
    # draw the background
    width = w-50
    height = h-50
    loc = (MIDDLE[0]-width/2, MIDDLE[1]-height/2)
    p.draw.rect(screen, p.Color("Orange"), p.Rect(loc, (width, height)), border_radius=10)

    # draw blank squares
    boxcolor = p.Color("gray")

    # font
    font = p.font.Font('freesansbold.ttf', 32)
    
    gap = 10
    width = height = (width-(gap*3))/size
    for i in range(size):
        for j in range(size):
            l = (j*width+loc[0]+(gap*j), i*height+loc[1]+(gap*i))
            rect = p.Rect(l, (width, height))
            p.draw.rect(screen, boxcolor, rect, border_radius=15)
            if game[i][j] != 0:
                white = (255, 255, 255)
                green = (0, 255, 0)
                blue = (0, 0, 128)
                text = font.render(str(game[i][j]), True, green, blue)

                
                textRect = text.get_rect()

                textRect.center = rect.center

                screen.blit(text, textRect)
    
if __name__ == "__main__":
    init()
    p.init()

    newGame(4)
