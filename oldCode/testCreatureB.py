import unittest
import creatureB
import bpy
import os

class TestCreature(unittest.TestCase):
    # def testCreatExists(self):
    #     self.assertIsNotNone(creatureB.Creature)
    
    # def testCreatureGetFlatLinks(self):
    #     c = creatureB.Creature(gene_count=4)
    #     links = c.get_flat_links()
    #     self.assertEqual(len(links), 4)

    # def testExpLinks(self):
    #     for i in range(100):
    #         c = creatureB.Creature(gene_count=4)
    #         links = c.get_flat_links()
    #         exp_links = c.get_expanded_links()
    #         print(len(exp_links))
        #self.assertGreaterEqual(len(exp_links), len(links))

    def testToEdgesNotNone(self):
        c = creatureB.Creature(gene_count=88)
        edges_arr = c.to_edges()
        print(edges_arr)
        #self.assertIsNotNone(edges_arr)

unittest.main()