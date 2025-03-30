import unittest
import population 

class TestPop(unittest.TestCase):

    def testPopHasIndis(self):
        pop = population.Population(pop_size=3)
        self.assertEqual(len(pop.creatures), 3)

    unittest.main()