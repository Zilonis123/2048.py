from functools import reduce
import random
import copy

class Engine():
    def __init__(self, size):
        self.size = size
        self.map = self.makeMap(size)
        
        self.score = 0
        self.moves = []

    def makeMap(self, size):
        # Generate an empty map
        m = [[0 for i in range(0, size)] for i in range(0, size)]

        # Add 2 random tiles
        self.addRandomInt(m)
        self.addRandomInt(m)
        return m

    def getPossibleMoves(self):
        moves = []
        functions = [self.reduceDown, self.reduceLeft, self.reduceUp, self.reduceRight]

        for f in functions:
            move = f(self.map)
            if move.map != move.prev_map:
                moves.append(move)

            self.undoMove()
        return moves


    def calculatePoints(self, b):
        s = 0
        tb = b
        ta = self.map
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
            tb = self.rotate(tb)
            ta = self.rotate(ta)

        self.score += s
        return s
        
    def undoMove(self):
        if len(self.moves) < 1:
            return

        previous_move = self.moves.pop()
        self.score = previous_move.game_score
        self.map = previous_move.prev_map

    def addRandomInt(self, m):
        """
        This function will take a map object and add an integer from the seed Array
        """
        seed = [2, 2, 2, 4]
        done = False
        while not done:
            x, y = self.randomPoint(self.size-1)
            if m[x][y] == 0:
                done = True
        v = random.randint(0, len(seed)-1)
        m[x][y] = seed[v]
        return v

    def randomPoint(self, size):
        x = random.randint(0, size)
        y = random.randint(0, size)
        return (x, y)

    def reduceLineLeft(self, xs):
        
        result = []
        prev = None
        
        for x in xs:
            if x != 0:
                if prev == x:
                    result[-1] *= 2
                    prev = None
                else:
                    result.append(x)
                    prev = x
        result.extend([0] * (len(xs) - len(result)))
        return result


    def reduceLineRight(self, xs):
        return self.reduceLineLeft(xs[::-1])[::-1]

    def reduceLeft(self, m):
        self.map = self._mapReplacement(self.reduceLineLeft, m)
        m = Move(self, m, self.reduceLeft)
        self.moves.append(m)
        return m

    def reduceRight(self, m):
        self.map = self._mapReplacement(self.reduceLineRight, m)
        m = Move(self, m, self.reduceRight)
        self.moves.append(m)
        return m

    def reduceUp(self, m):
        self.map = self.rotate(self.reduceRight(self.rotate(m)).map)
        m = Move(self, m, self.reduceUp)
        self.moves.append(m)
        return m

    def reduceDown(self, m):
        self.map = self.rotate(self.reduceLeft(self.rotate(m)).map)
        m = Move(self, m, self.reduceDown)
        self.moves.append(m)
        return m

    def rotate(self, m):
        """Rotates the map"""

        rotatedt = list(reversed(list(zip(*m[::-1]))))
        # rotated is a tuple right now, but we need it as an array
        rotated = []
        for t in rotatedt:
            m = list(t)
            rotated.append(m)
        return rotated

    def _mapReplacement(self, fun, iter):
        """This function replaced map()"""

        res = []
        for i in iter:
            res.append(fun(i))
        return res

    def _traverse(self, a, f):
        for line in a:
            for ele in line:
                if f(ele): return True
        return False

    def isWin(self):
        return self._traverse(self.map, lambda x: x == 2048)

    def isFail(self):
        def aux(m):
            for i in m:
                for j in zip(i, i[1:]):
                    if j[0] == 0 or j[1] == 0 or j[0] == j[1]: return False
            return True
        return aux(self.map) and aux(self.rotate(self.map))


class Move():
    def __init__(self, game, prev_map, fu):
        self.game = game
        self.map = game.map
        self.prev_map = prev_map
        self.score = -1

        self.game_score = game.score

        self.executedBy = fu

    def score(self):
        if self.score: return self.score

        self.score = game.calculatePoints(self.prev_map)

