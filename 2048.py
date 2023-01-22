#coding=utf8

from time import sleep, time
from colorama import Fore, Back, init
from functools import reduce
import pygame as p
import json
<<<<<<< HEAD
from game import game
from game import ai

=======
>>>>>>> parent of 2d4999f (:white_check_mark: Added game directory)

def mapReplacement(fun, iter):
    res = []
    for i in iter:
        res.append(fun(i))
    return res

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




def randomNum(a):
    seed = [2, 2, 2, 4]
    v = random.randint(0, len(seed)-1)
    done = False
    while not done:
        x, y = randomPoint(len(a)-1)
        if a[x][y] == 0:
            a[x][y] = seed[v]
            done = True

    return seed[v]

class Game():
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.lost = 0
        self.won = 0
        self.map = self.makeMap(self.size)
    
    def makeMap(self, size):
        map = self.newEmptyMap(size)
        self.randomInt(map)
        self.randomInt(map)
        return map

    def newEmptyMap(self, size):
        return [[0 for i in range(0, size)] for i in range(0, size)]
    
    def randomInt(self, map):
        seed = [2, 2, 2, 4]
        done = False
        while not done:
            x, y = self.randomPoint(self.size)
            v = random.randint(0, len(seed)-1)
            if map[x][y] == 0:
                done = True
        map[x][y] = seed[v]

    def randomPoint(self, size):
        x = random.randint(0, size)
        y = random.randint(0, size)
        return (x-1, y-1)

    def _reduceLineLeft(self, xs): 
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

    def _reduceLineRight(self, xs):
        return self._reduceLineLeft(xs[::-1])[::-1]

    def reduceLeft(self, a):
        return mapReplacement(self._reduceLineLeft, a)

    def reduceRight(self, a):
        return mapReplacement(self._reduceLineRight, a)

    def reduceUp(self, a):
        return self.rotate(self.reduceRight(self.rotate(a)))

    def reduceDown(self, a):
        return self.rotate(self.reduceLeft(self.rotate(a)))

    def rotate(self, a):
        rotatedt = list(reversed(list(zip(*a[::-1]))))
        # rotated is a tuple right now, but we need it as an array
        rotated = []
        for t in rotatedt:
            a = list(t)
            rotated.append(a)
        # print(rotated)
        return rotated

    def calculatePoints(self, a, b):
        s = 0
        tb = b
        ta = a
        for l in range(3):
            for k in range(len(tb)):
                for i in range(len(ta[k])):
                    if ta[i] == 0:
                        continue;
                    item = ta[k][i]
                    # print(item)
                    for j in range(len(tb[k])):
                        if tb[k][j] < 2:
                            continue
                        if tb[k][j] == item//2:
                            if len(tb) != j+1 and tb[k][j+1] == item//2:
                                # add score
                                s += item//4
                                tb[k][j] == 0
                                tb[k][j+1] == 0
                                break;
            tb = self.rotate(tb)
            ta = self.rotate(ta)

        return s

    def isWin(self, a):
        return self._traverse(a, lambda x: x == 2048)

    def isFail(self, a):
        def aux(a):
            for i in a:
                for j in zip(i, i[1:]):
                    if j[0] == 0 or j[1] == 0 or j[0] == j[1]: return False
            return True
        return aux(a) and aux(self.rotate(a))
        
    def _traverse(self, a, f):
        for line in a:
            for ele in line:
                if f(ele): return True
        return False

def newGame(size):
    # load the config file
    with open("config.json", "r", encoding="utf-8") as data_file:
        config = json.load(data_file).get("config")

    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    MAX_FPS = 30

    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("2048")
    clock = p.time.Clock()

    g = game.Game(size, True)

    undo = False # keep the track if we undid something in this cycle
   
    # start the game loop
    running = True
    while running:
        # make an empty move
        move = game.Move(g.map, g.map, g.reduceLeft)
        undo = False

        # st = time()
        # s, move = ai.getBestMove(g)
        # et = time()
        # elapsed_time = et-st
        # if g.lost != 1:
        #     print("Elapsed time " + str(elapsed_time) + "ms with score " + str(s))

        # if move != 0:
        #     g.moveBoard(move.func)
        # else:
        #     v = g.getAllLegalMoves(g.map)
        #     for i in v:
        #         g.moveBoard(i)
        
                
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            if e.type == p.KEYDOWN:
                if g.lost <= 0:
                    if e.key == p.K_w:
                        move = g.moveBoard(g.reduceUp)
                    elif e.key == p.K_s:
                        move = g.moveBoard(g.reduceDown)
                    elif e.key == p.K_a:
                        move = g.moveBoard(g.reduceLeft)
                    elif e.key == p.K_d:
                        move = g.moveBoard(g.reduceRight)         
                if p.key.get_mods() & p.KMOD_CTRL:
                    if e.key == p.K_r:
                        # reload the config file
                        print("Reloading the configuration file..")
                        with open("config.json", "r", encoding="utf-8") as data_file:
                            config = json.load(data_file).get("config")
                    elif e.key == p.K_z: 
                        # undo the move
                        if len(g.moves) < 1:
                            print("Nothing to undo..")
                            continue;
                        g.undoMove()
                    elif e.key == p.K_p:
                        g = game.Game(size)
                        undo = True # Set undo to true so the game doesn't decide that the user moved
        # Check if the board moved
        if move and move.prevmap != move.map and not undo:
            g.giveScoreForMove(move)

        # check/update if won/lost
        g.isFail(g.map)
        g.isWin(g.map)

        drawScreen(screen, g, config, move)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawScreen(screen, g, c, m):
    screen.fill(c["screen-color"])
    drawBoard(screen, g, c, m)
    drawScore(screen, g)

def drawScore(screen, g):
    font = p.font.Font('freesansbold.ttf', 32)

    # rect = p.Rect((0, 0), (150, 100))

    text = font.render("Score: " + str(g.score), True, p.Color("black"), p.Color("white"))
    textRect = text.get_rect()
    # textRect.center = rect.center

    screen.blit(text, textRect)

def drawBoard(screen, g, config, move):
    w = config["WIDTH"]
    h = config["HEIGHT"]
    MIDDLE = (w/2, h/2)
    # draw the background
    width = w-100
    height = h-100
    loc = (MIDDLE[0]-width/2, h-height)
    r = p.Rect(loc, (width, height))
    if config["show-tile-background"]:
        p.draw.rect(screen, p.Color("Orange"), r)

    # font
    font = p.font.Font('freesansbold.ttf', 32)
    
    gap = 10
    bwidth = (width-(gap*3))/g.size
    bheight = (height-(gap*3))/g.size

    map = move.compressMap()
    for i in range(g.size):
        for j in range(g.size):
            l = (j*bwidth+loc[0]+(gap*j), i*bheight+loc[1]+(gap*i))
            rect = p.Rect(l, (bwidth, bheight))

            # determine the color
            color = config["colors"][str(map[i][j])]
            background = p.Color(color["background"])

            p.draw.rect(screen, background, rect, border_radius=15)
            if g.map[i][j] != 0:
                fontclr = color["font"]

                text = font.render(str(map[i][j]), True, fontclr, background)

                textRect = text.get_rect()
                textRect.center = rect.center

                screen.blit(text, textRect)

    if g.lost > 0 or g.won > 0:
        # text
        text = ""

        s = p.Surface((width, height))  # the size of your rect
        if g.lost > 0:
            s.set_alpha(128 * g.lost)               # alpha level
            text = "Game Over!"
        else:
            s.set_alpha(128 * g.won)                # alpha level
            text = "You won!"
        s.fill((255,255,255))           # this fills the entire surface
        screen.blit(s, loc)    # (0,0) are the top-left coordinates

        f = p.font.Font("freesansbold.ttf", 32)
        textObj = f.render(text, True, (0, 0, 0), (255, 255, 255))
        
        textRect = textObj.get_rect()
        textRect.center = r.center

        screen.blit(textObj, textRect)
        
    
if __name__ == "__main__":
    init()
    p.init()

<<<<<<< HEAD
    newGame(4)
=======
    # newGame(4)
    a = Game(4)
    print(a.map)
>>>>>>> parent of 2d4999f (:white_check_mark: Added game directory)
