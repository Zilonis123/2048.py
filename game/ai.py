
# all of these functions take the game object from game.py as a pramater
import random

CYCLES = 4
WIN = 100000
LOST = -100000

def getBestMove(game, cycle=1, move=0, bestscore=-100):
    if cycle == CYCLES:
        score = calculate(game, move)
        return score, move


    valid = game.getAllLegalMoves(game.map)
    score = bestscore
    bestmove = move
    for i in range(4):
        for v in valid:
            m = game.moveBoard(v, i)
            score, bm = getBestMove(game, cycle+1, m, bestscore)
            if score > bestscore:
                bestscore = score
                if move != 0:
                    bestmove = move
                else:
                    bestmove = bm

                s = calculate(game, m)
                
                if s > bestscore:
                    bestscore = s
                    bestmove = m

                if s > bestscore+250 and cycle >= 2:
                    game.undoMove(True)
                    return s, bestmove

                
                
            game.undoMove(True) # dont add score to the game
    
    
    return bestscore, bestmove


def calculate(game, move):
    if move == 0:
        valid = game.getAllLegalMoves(game.map)
        v = random.randint(0, len(valid)-1)
        move = valid[v]
        move = game.moveBoard(move)
        game.undoMove(True)
           
    score = move.calculatePoints()
    if game.isWin(game.map):
        score += WIN
    elif game.isFail(game.map):
        score -= LOST


    for i in range(len(move.map)):
        for j in range(len(move.map)):
            if move.map[i][j] == 0:
                score += 15
    return score