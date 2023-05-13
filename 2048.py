#coding=utf8

import copy
import pygame as p
import json
from Game import engine

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
                if e.key == p.K_w:   move = game.reduceUp(game.map)
                elif e.key == p.K_s: move = game.reduceDown(game.map)
                elif e.key == p.K_a: move = game.reduceLeft(game.map)
                elif e.key == p.K_d: move = game.reduceRight(game.map)            
                elif p.key.get_mods() & p.KMOD_CTRL:
                    if e.key == p.K_r:
                        # reload the config file
                        print("Reloading the configuration file..")
                        with open("config.json", "r", encoding="utf-8") as data_file:
                            config = json.load(data_file).get("config")
                    elif e.key == p.K_z: 
                        print("Undoing..")
                        game.undoMove()
                        undo = True
                    elif e.key == p.K_p:
                        info["lost"] = 0
                        info["won"] = 0
                        info["score"] = 0
                        undo = True # Set undo to true so the game doesn't decide that the board moved
                        moves = []
                        game.map = game.makeMap(size)

        # Check if the board moved
        if game.map != map_copy and not undo:
            # if it did add a number
            tile_added = game.addRandomInt(game.map)

            if config["give-points-for-turn"]:
                game.score += tile_added
           
            game.calculatePoints(map_copy)
            

        if info["lost"] < 1 and game.isFail():
            info["lost"] += 0.05
        if info["won"] < 1 and game.isWin():
            info["won"] += 0.05

        drawScreen(screen, game, config, info)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawScreen(screen, game, c, ginfo):
    screen.fill(c["screen-color"])
    drawBoard(screen, game.map, c, ginfo)
    drawScore(screen, game)

def drawScore(screen, game):
    font = p.font.Font('freesansbold.ttf', 32)

    # rect = p.Rect((0, 0), (150, 100))

    text = font.render("Score: " + str(game.score), True, p.Color("black"), p.Color("white"))
    textRect = text.get_rect()
    # textRect.center = rect.center

    screen.blit(text, textRect)

def drawBoard(screen, gameMap, config, ginfo):
    # width and height of the screen
    w = config["WIDTH"]
    h = config["HEIGHT"]

    r_border_radius = config["Rect-Border-Radius"]
    bgoffset = config["background-offset"]

    size = len(gameMap)
    MIDDLE = (w/2, h/2)

    # draw the background
    bgSize = config["background-size"]

    # width and height of the background
    width = w-bgSize
    height = h-bgSize
    loc = (MIDDLE[0]-width/2, h-height-bgoffset)

    rectLocation = (loc[0]-bgoffset, loc[1]-bgoffset)
    bgRect = p.Rect(rectLocation, (width+bgoffset*2, height+bgoffset*2))
    if config["show-tile-background"]:
        p.draw.rect(screen, p.Color("Orange"), bgRect, border_radius=r_border_radius)

    # font
    font = p.font.Font('freesansbold.ttf', 32)
    
    gap = 10
    bwidth = (width-(gap*3))/size
    bheight = (height-(gap*3))/size
    for i in range(size):
        for j in range(size):
            # What tile are we on?
            tile = gameMap[i][j]

            l = (j*bwidth+loc[0]+(gap*j), i*bheight+loc[1]+(gap*i)) # (x, y)
            rect = p.Rect(l, (bwidth, bheight))

            # determine the color
            color = config["colors"][str(tile)]
            backgroundColor = p.Color(color["background"])

            # Draw the tile
            p.draw.rect(screen, backgroundColor, rect, border_radius=r_border_radius)

            if tile != 0:
                fontclr = color["font"]

                text = font.render(str(tile), True, fontclr, backgroundColor)

                textRect = text.get_rect()
                textRect.center = rect.center

                screen.blit(text, textRect)

    if ginfo["lost"] > 0 or ginfo["won"]:
        # text
        text = ""

        s = p.Surface((width, height))
        if ginfo["lost"] > 0:
            s.set_alpha(128 * ginfo["lost"]) # alpha level
            text = "Game Over!"
        else:
            s.set_alpha(128 * ginfo["won"]) # alpha level 
            text = "You won!"
        s.fill((255,255,255))           # this fills the entire surface
        screen.blit(s, loc)    # (0,0) are the top-left coordinates

        f = p.font.Font("freesansbold.ttf", 32)
        textObj = f.render(text, True, (0, 0, 0), (255, 255, 255))
        
        textRect = textObj.get_rect()
        textRect.center = bgRect.center

        screen.blit(textObj, textRect)
        
    
if __name__ == "__main__":
    p.init()

    newGame(4)
