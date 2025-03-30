import numpy as np
import copy 
import random

class Genome():
    @staticmethod 
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene
    
    @staticmethod 
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length) for i in range(gene_count)]
        return genome

    #add faces
    @staticmethod
    def get_gene_spec():
        gene_spec =  {
            "x":{"scale":20}, 
            "y": {"scale":20},
            "z": {"scale":20},
            "connected_to": {"scale":0, "data":[]},
            "fitness_val": {"scale":0, "data":0}
            }
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1
        # print(gene_spec)
        return gene_spec

    @staticmethod
    def get_gene_dict(gene, spec):
        gdict = {}
        for key in spec:
            # print(key)
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gdict[key] = gene[ind] * scale
        return gdict

    @staticmethod
    def get_genome_dicts(genome, spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene, spec))
        # print(gdicts)
        return gdicts

    @staticmethod
    #uniq_parent_name, uniq_name,
    def expandLinks(parent_link, flat_links, exp_links):
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        sibling_ind = 1
        for c in children:
            for r in range(int(c.recur)):
                sibling_ind  = sibling_ind + 1
                c_copy = copy.copy(c)
                #c_copy.parent_name = uniq_parent_name
                # uniq_name = c_copy.name + str(len(exp_links))
                #uniq_name = len(exp_links) #index
                # print("exp: ", c.name, " -> ", uniq_name)
                #c_copy.name = uniq_name
                c_copy.sibling_ind = sibling_ind
                exp_links.append(c_copy)
                #assert c.parent_name != c.name, "Genome::expandLinks: link joined to itself: " + c.name + " joins " + c.parent_name 
                Genome.expandLinks(c, flat_links, exp_links)
    
    @staticmethod
    def genome_to_links(gdicts):
        links = []
        link_ind = 0
        connected_to_arr = [link_ind]

        for gdict in gdicts:
            link_name = link_ind
            parent_ind = gdict["connected_to"] * len(connected_to_arr)
            assert parent_ind < len(connected_to_arr), "genome.py: parent ind too high: " + str(parent_ind) + "got: " + str(connected_to_arr)
            connected_to = connected_to_arr[int(parent_ind)]
            #print("available parents: ", parent_names, "chose", parent_name)
            link = JSONLink(name=link_name,
                            connected_to = connected_to, 
                            x=gdict["x"], 
                            y=gdict["y"],
                            z=gdict["z"], 
                            # connected_to=gdict["connected_to"],
                            fitness_val=gdict["fitness_val"])
            links.append(link)
            if link_ind != 0:# don't re-add the first link
                connected_to_arr.append(link_name)
            link_ind = link_ind + 1

        # now just fix the first link so it links to nothing
        # links[0].parent_name = "None"
        return links


#add faces
class JSONLink:
    def __init__(self, name, connected_to,
                x=20, 
                y=20,
                z=20,
                # connected_to=[],
                fitness_val=0):
        self.name = name
        self.x = x 
        self.y = y
        self.z = z
        self.connected_to = connected_to
        self.fitness_val = fitness_val
        self.sibling_ind = 1

    #code for blend
    #    def to_link_element(self, adom):
    #     #         <link name="base_link">
    #     #     <visual>
    #     #       <geometry>
    #     #         <cylinder length="0.6" radius="0.25"/>
    #     #       </geometry>
    #     #     </visual>
    #     #     <collision>
    #     #       <geometry>
    #     #         <cylinder length="0.6" radius="0.25"/>
    #     #       </geometry>
    #     #     </collision>
    #     #     <inertial>
    #     # 	    <mass value="0.25"/>
    #     # 	    <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
    #     #     </inertial>
    #     #   </link>
  
    #     link_tag = adom.createElement("link")
    #     link_tag.setAttribute("name", self.name)
    #     vis_tag = adom.createElement("visual")
    #     geom_tag = adom.createElement("geometry")
    #     cyl_tag = adom.createElement("cylinder")
    #     cyl_tag.setAttribute("length", str(self.link_length))
    #     cyl_tag.setAttribute("radius", str(self.link_radius))
        
    #     geom_tag.appendChild(cyl_tag)
    #     vis_tag.appendChild(geom_tag)
        
        
    #     coll_tag = adom.createElement("collision")
    #     c_geom_tag = adom.createElement("geometry")
    #     c_cyl_tag = adom.createElement("cylinder")
    #     c_cyl_tag.setAttribute("length", str(self.link_length))
    #     c_cyl_tag.setAttribute("radius", str(self.link_radius))
        
    #     c_geom_tag.appendChild(c_cyl_tag)
    #     coll_tag.appendChild(c_geom_tag)
        
    #     #     <inertial>
    #     # 	    <mass value="0.25"/>
    #     # 	    <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
    #     #     </inertial>
    #     inertial_tag = adom.createElement("inertial")
    #     mass_tag = adom.createElement("mass")
    #     # pi r^2 * height
    #     mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
    #     mass_tag.setAttribute("value", str(mass))
    #     inertia_tag = adom.createElement("inertia")
    #     # <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
    #     inertia_tag.setAttribute("ixx", "0.03")
    #     inertia_tag.setAttribute("iyy", "0.03")
    #     inertia_tag.setAttribute("izz", "0.03")
    #     inertia_tag.setAttribute("ixy", "0")
    #     inertia_tag.setAttribute("ixz", "0")
    #     inertia_tag.setAttribute("iyx", "0")
    #     inertial_tag.appendChild(mass_tag)
    #     inertial_tag.appendChild(inertia_tag)
        

    #     link_tag.appendChild(vis_tag)
    #     link_tag.appendChild(coll_tag)
    #     link_tag.appendChild(inertial_tag)
        
    #     return link_tag