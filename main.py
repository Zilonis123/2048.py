#coding=utf8

import copy
import pygame as p
import json
from src import engine, ai
from src.draw import *

class SoftwareRenderer():
    def __init__(self):
        # Reload config file
        self.reloadConfig()

        RES = self.WIDTH, self.HEIGHT = self.config["RES"]
        self.FPS = 30

        # Create screen
        self.screen = p.display.set_mode(RES)
        p.display.set_caption("2048")
        self.clock = p.time.Clock()

        # generate game object
        self.game = engine.Engine(4)


    def run(self) -> None:
        while True:
            self.handleEvents()

            self.draw()
            
            p.display.flip()
            self.clock.tick(self.FPS)

    def draw(self) -> None:
        self.screen.fill(self.config["screen-color"])
        drawBoard(self)
    
    def handleEvents(self) -> None:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
            elif e.type == p.KEYDOWN:
                self.handleKeypress(e.key)

    def handleKeypress(self, key) -> None:
        # simple switch
        # if key == p.K_w:
        # elif key == p.K_s: 
        # elif key == p.K_a: 
        # elif key == p.K_d: 
        if key == p.K_r:
            self.reloadConfig()
        pass

    def reloadConfig(self) -> dict:  
        with open("config.json") as data:
            self.config = json.load(data).get("config", {})
            return self.config

if __name__ == "__main__":
    p.init()

    software = SoftwareRenderer()
    software.run()