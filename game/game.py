import random
import copy
from functools import reduce


def mapReplacement(fun, iter):
    res = []
    for i in iter:
        res.append(fun(i))
    return res

class Game():
    def __init__(self, size, graduallyIncrease=False):
        self.size = size
        self.score = 0
        self.lost = 0
        self.won = 0
        self.map = self.makeMap(self.size)
        self.graduallyIncrease = graduallyIncrease

        self.moves = [] # initalize the moves

    def getAllLegalMoves(self, map):
        func = [self.reduceLeft, self.reduceRight, self.reduceUp, self.reduceDown]
        mapbefore = copy.deepcopy(map)
        legalmoves = []

        for legal in func:
            movedone = legal(self.map)
            self.undoMove(True)
            if mapbefore != movedone.map:
                legalmoves.append(legal)

        return legalmoves


    def undoMove(self, dontremovescore=False):
        if len(self.moves) <= 0:
            return
        m = self.moves.pop() # get the move to undo and remove it

        # set the variables back what they were
        if not dontremovescore:
            self.score -= m.calculatePoints()
        self.lost = 0
        self.won = 0
        self.map = m.prevmap
    
    def makeMap(self, size):
        map = self.newEmptyMap(size)
        self.randomInt(map)
        self.randomInt(map)
        return map

    def newEmptyMap(self, size):
        return [[0 for i in range(0, size)] for i in range(0, size)]
    
    def randomInt(self, map, op=-1):
        seed = [2, 2, 2, 4]
        done = False
        v = op
        while not done:
            x, y = self.randomPoint(self.size)
            if op != -1:
                v = random.randint(0, len(seed)-1)
            if map[x][y] == 0:
                done = True
        map[x][y] = seed[v]

    def giveScoreForMove(self, move):
        self.score += move.calculatePoints()

    def randomPoint(self, size):
        x = random.randint(0, size)
        y = random.randint(0, size)
        return (x-1, y-1)

    def moveBoard(self, func, op=-1):
        m = func(self.map)
        if m.prevmap != m.map:
            self.randomInt(self.map, op)
        return m

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
        b = mapReplacement(self._reduceLineLeft, a)
        m = Move(a, b, self.reduceLeft)
        self.map = m.map
        self.moves.append(m)
        return m

    def reduceRight(self, a):
        b = mapReplacement(self._reduceLineRight, a)
        m = Move(a, b, self.reduceRight)
        self.map = m.map
        self.moves.append(m)
        return m

    def reduceUp(self, a):
        map = self.reduceRight(self.rotate(a)).map
        self.map = map
        self.undoMove(True)

        b = self.rotate(map)
        m = Move(a, b, self.reduceUp)
        self.map = m.map
        self.moves.append(m)
        return m

    def reduceDown(self, a):
        map = self.reduceLeft(self.rotate(a)).map
        self.map = map
        self.undoMove(True)

        b = self.rotate(map)

        m = Move(a, b, self.reduceDown)
        self.map = m.map
        self.moves.append(m)
        return m

    def rotate(self, a):
        rotatedt = list(reversed(list(zip(*a[::-1]))))
        # rotated is a tuple right now, but we need it as an array
        rotated = []
        for t in rotatedt:
            a = list(t)
            rotated.append(a)
        # print(rotated)
        return rotated


    def isWin(self, a):
        win = self._traverse(a, lambda x: x == 2048)
        if win:
            if self.graduallyIncrease:
                self.won += 0.1
            else:
                self.won = 1
        return self.won

    def isFail(self, a):
        legal = self.getAllLegalMoves(a)
        if len(legal) == 0:
            # if self.graduallyIncrease:
            #     self.lost += 0.1
            # else:
                self.lost = 1
        return self.lost
        
    def _traverse(self, a, f):
        for line in a:
            for ele in line:
                if f(ele): return True
        return False

class Move():
    def __init__(self, prevmap, map, func, score=-69420):
        self.prevmap = prevmap
        self.map = map
        self._score = score;
        self.func = func
        pass

    def calculatePoints(self):
        if not self._score == -69420:
            return self._score
        s = 0
        tb = self.prevmap
        ta = self.map
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

        self.score = s
        return s

    def rotate(self, a):
        rotatedt = list(reversed(list(zip(*a[::-1]))))
        # rotated is a tuple right now, but we need it as an array
        rotated = []
        for t in rotatedt:
            a = list(t)
            rotated.append(a)
        # print(rotated)
        return rotated
