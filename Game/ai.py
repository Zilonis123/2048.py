from random import shuffle
import numpy as np

DEPTH = 3

def getBestMove(game):
    moves = game.getPossibleMoves() # get all the possible moves
    if len(moves) == 0: # lost the game
        return 
    shuffle(moves)

    bestMoves = []
    for move in moves:
        score = evalGrid(move.map)
        move.score = score
        bestMoves.append(move)

    bestMove = bestMoves[0]
    for move in bestMoves:
        if move.score > bestMove.score: bestMove = move

    return bestMove

def check_tuple(tuple_value):
    if tuple_value[0] in (0, 3) and tuple_value[1] in (0, 3):
        return 0.5
    else:
        return -0.3


def getBestMoveDepth(game, depth=0):
    if depth==DEPTH:
        m = getBestMove(game)
        return m

    moves = game.getPossibleMoves()
    bestMove = -1
    for move in moves:
        m = getBestMoveDepth(game, depth+1)
        if bestMove != -1 and bestMove.score > m.score:
            bestMove = m
        else: bestMove = m

    return bestMove


TEMPLATE = [[0.135, 0.121, 0.102, 0.0999],
            [0.0997, 0.088, 0.076, 0.0724],
            [0.0606, 0.0562, 0.0371, 0.0161],
            [0.0125, 0.0099, 0.0057, 0.0033]]

def evalGrid(grid):
    return np.sum(np.array(grid) * TEMPLATE)