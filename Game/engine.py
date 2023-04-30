from functools import reduce
import random


class Engine():
    def __init__(self, size):
        self.size = size
        self.map = self.makeMap(size)

    def makeMap(self, size):
        # Generate an empty map
        m = [[0 for i in range(0, size)] for i in range(0, size)]

        # Add 2 random tiles
        self.addRandomInt(m)
        self.addRandomInt(m)
        return m
    

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
        return self.map

    def reduceRight(self, m):
        self.map = self._mapReplacement(self.reduceLineRight, m)
        return self.map

    def reduceUp(self, m):
        self.map = self.rotate(self.reduceRight(self.rotate(m)))
        return self.map

    def reduceDown(self, m):
        self.map = self.rotate(self.reduceLeft(self.rotate(m)))
        return self.map

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