import genomeB1 
import bpy
from enum import Enum
import numpy as np

class Creature:
    def __init__(self, gene_count):
        self.spec = genomeB1.Genome.get_gene_spec()
        self.dna = genomeB1.Genome.get_random_genome(len(self.spec), gene_count)
        self.flat_links = None
        self.exp_links = None
        self.start_position = None
        self.last_position = None

    def get_flat_links(self):
        if self.flat_links == None:
            gdicts = genomeB1.Genome.get_genome_dicts(self.dna, self.spec)
            self.flat_links = genomeB1.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    # def get_expanded_links(self):
    #     self.get_flat_links()
    #     if self.exp_links is not None:
    #         return self.exp_links
        
    #     exp_links = []
    #     for i in self.flat_links:
    #         exp_links.append(i)
    #         genomeB.Genome.expandLinks(i, 
    #                             self.flat_links, 
    #                             exp_links)
    #         #print(i.parent_name)
    #     self.exp_links = exp_links
    #     return self.exp_links

    #change to blend
    def to_edges(self):
        self.get_flat_links()
        edges = []
        for link in self.flat_links[1::]:
            edges.append([link.name,link.connected_to])
        print(edges)
        
        return edges