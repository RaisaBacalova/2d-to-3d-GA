import objectCreation
import random

class Population():
    def __init__(self, pop_size):
        self.creatures = [objectCreation.ObjectCreation() for i in range(pop_size)]

    @staticmethod
    def get_fitness_map(fits):
        fitmap = []
        total = 0
        for f in fits:
            total += f
            fitmap.append(round(total, 3))
        return fitmap

    @staticmethod
    def select_parent(fitmap):
        r = round(random.triangular(0, fitmap[-1]), 2)
        print('r: ', r)
        for i in range(len(fitmap)):
            if r <= fitmap[i]:
                return i

        