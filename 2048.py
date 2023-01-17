#coding=utf8

import copy
import random
from colorama import Fore, Back, init
from functools import reduce
import pygame as p
import json

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
    done = False
    while not done:
        x, y = randomPoint(len(a)-1)
        v = random.randint(0, len(seed)-1)
        if a[x][y] == 0:
            done = True
    a[x][y] = seed[v]

def randomNum(a):
    seed = [2, 2, 2, 4]
    x, y = randomPoint(len(a)-1)
    if a[x][y] == 0:
        v = random.randint(0, len(seed)-1)
        a[x][y] = seed[v]
    else: randomNum(a)

def makeMap(size):
    # Generate empty map
    a = newEmpty(size)
    # add to random values
    randomInit(a)
    randomInit(a)
    return a

def newGame(size):
    # load the config file
    with open("config.json", "r", encoding="utf-8") as data_file:
        config = json.load(data_file).get("config")

    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    won = False
    MAX_FPS = 30

    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("2048")
    clock = p.time.Clock()

    a = makeMap(size)

    moves = []
    undo = False # keep the track if we undid something in this cycle
   
    # start the game loop
    running = True
    while running:
        undo = False
        b = copy.deepcopy(a)
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
                elif p.key.get_mods() & p.KMOD_CTRL:
                    if e.key == p.K_r:
                        # reload the config file
                        print("Reloading the configuration file..")
                        with open("config.json", "r", encoding="utf-8") as data_file:
                            config = json.load(data_file).get("config")
                    elif e.key == p.K_z: 
                        # undo the move
                        if len(moves) < 2:
                            print("Nothing to undo..")
                            continue;
                        print("Undo..")
                        moves.pop()
                        prev = moves.pop()
                        a = prev
                        undo = True
        # Check if the board moved
        if a != b and not undo:
            # if it did add a number
            randomNum(a)

            moves.append(a)

        drawScreen(screen, a, WIDTH, HEIGHT, size, config)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawScreen(screen, game, w, h, s, c):
    drawBoard(screen, w, h, s, game, c)

def drawBoard(screen, w, h, size, game, config):
    MIDDLE = (w/2, h/2)
    # draw the background
    width = w-50
    height = h-50
    loc = (MIDDLE[0]-width/2, MIDDLE[1]-height/2)
    p.draw.rect(screen, p.Color("Orange"), p.Rect(loc, (width, height)), border_radius=10)

    # font
    font = p.font.Font('freesansbold.ttf', 32)
    
    gap = 10
    width = (width-(gap*3))/size
    height = (height-(gap*3))/size
    for i in range(size):
        for j in range(size):
            l = (j*width+loc[0]+(gap*j), i*height+loc[1]+(gap*i))
            rect = p.Rect(l, (width, height))

            # determine the color
            color = config["colors"][str(game[i][j])]
            background = p.Color(color["background"])

            p.draw.rect(screen, background, rect, border_radius=15)
            if game[i][j] != 0:
                fontclr = color["font"]

                text = font.render(str(game[i][j]), True, fontclr, background)

                
                textRect = text.get_rect()

                textRect.center = rect.center

                screen.blit(text, textRect)
    
if __name__ == "__main__":
    init()
    p.init()

    newGame(4)
