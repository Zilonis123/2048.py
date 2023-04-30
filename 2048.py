#coding=utf8

import copy
import random
from colorama import Fore, Back, init
import pygame as p
import json
from Game import engine


def calculatePoints(game, b):
    s = 0
    tb = b
    ta = game.map
    for l in range(3):
        for k in range(len(tb)):
            for i in range(len(ta[k])):
                if ta[i] == 0:
                    continue
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
                            break
        tb = game.rotate(tb)
        ta = game.rotate(ta)

    return s

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

    game = engine.Engine(size)

    moves = []
    undo = False # keep the track if we undid something in this cycle

    info = {
        "score": 0,
        "lost": 0,
        "won": 0,
    }
   
    # start the game loop
    running = True
    while running:
        undo = False
        map_copy = copy.deepcopy(game.map)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            if e.type == p.KEYDOWN:
                if e.key == p.K_w:
                    game.reduceUp(game.map)
                elif e.key == p.K_s:
                    game.reduceDown(game.map)
                elif e.key == p.K_a:
                    game.reduceLeft(game.map)
                elif e.key == p.K_d:
                    game.reduceRight(game.map)            
                elif p.key.get_mods() & p.KMOD_CTRL:
                    if e.key == p.K_r:
                        # reload the config file
                        print("Reloading the configuration file..")
                        with open("config.json", "r", encoding="utf-8") as data_file:
                            config = json.load(data_file).get("config")
                    # elif e.key == p.K_z: 
                    #     # undo the move
                    #     if len(moves) < 2:
                    #         print("Nothing to undo..")
                    #         continue
                    #     print("Undo..")
                    #     moves.pop()
                    #     prev = moves.pop()
                    #     info["lost"] = 0
                    #     info["won"] = 0
                    #     info["score"] = calculatePoints(prev, moves[len(moves)-1].map)
                    #     game.map = prev
                    #     undo = True
                    elif e.key == p.K_p:
                        info["lost"] = 0
                        info["won"] = 0
                        info["score"] = 0
                        undo = True # Set undo to true so the game doesn't decide that the user moved
                        moves = []
                        game.map = game.makeMap(size)

        # Check if the board moved
        if game.map != map_copy and not undo:
            # if it did add a number
            if config["give-points-for-turn"]:
                info["score"] += game.addRandomInt(game.map)
           
            info["score"] += calculatePoints(game, map_copy)
            moves.append(game)

        if info["lost"] < 1 and game.isFail():
            info["lost"] += 0.05
            # this will be used to make a cool FADING effect
        if info["won"] < 1 and game.isWin():
            info["won"] += 0.05

        drawScreen(screen, game, config, info)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawScreen(screen, game, c, ginfo):
    screen.fill(c["screen-color"])
    drawBoard(screen, game.map, c, ginfo)
    drawScore(screen, ginfo)

def drawScore(screen, ginfo):
    font = p.font.Font('freesansbold.ttf', 32)

    # rect = p.Rect((0, 0), (150, 100))

    text = font.render("Score: " + str(ginfo["score"]), True, p.Color("black"), p.Color("white"))
    textRect = text.get_rect()
    # textRect.center = rect.center

    screen.blit(text, textRect)

def drawBoard(screen, game, config, ginfo):
    w = config["WIDTH"]
    h = config["HEIGHT"]
    size = len(game)
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
    bwidth = (width-(gap*3))/size
    bheight = (height-(gap*3))/size
    for i in range(size):
        for j in range(size):
            l = (j*bwidth+loc[0]+(gap*j), i*bheight+loc[1]+(gap*i))
            rect = p.Rect(l, (bwidth, bheight))

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

    if ginfo["lost"] > 0 or ginfo["won"]:
        # text
        text = ""

        s = p.Surface((width, height))  # the size of your rect
        if ginfo["lost"] > 0:
            s.set_alpha(128 * ginfo["lost"])               # alpha level
            text = "Game Over!"
        else:
            s.set_alpha(128 * ginfo["won"])                # alpha level
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

    newGame(4)
