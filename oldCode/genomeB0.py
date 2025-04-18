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
            "verts-x":{"scale":20}, 
            "verts-y": {"scale":20},
            "verts-recurrence": {"scale":1},
            "edges-parent": {"scale":1}
            }
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1
        #print(gene_spec)
        return gene_spec

    @staticmethod
    def get_gene_dict(gene, spec):
        gdict = {}
        for key in spec:
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gdict[key] = gene[ind] * scale
        return gdict

    @staticmethod
    def get_genome_dicts(genome, spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene, spec))
        #print(gdicts)
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
        parent_names = [link_ind]

        for gdict in gdicts:
            # link_name = str(link_ind)
            link_name = link_ind
            parent_ind = gdict["edges-parent"] * len(parent_names)
            assert parent_ind < len(parent_names), "genome.py: parent ind too high: " + str(parent_ind) + "got: " + str(parent_names)
            parent_name = parent_names[int(parent_ind)]
            #print("available parents: ", parent_names, "chose", parent_name)
            recur = gdict["verts-recurrence"]
            link = JSONLink(name=link_name, 
                            parent_name=parent_name, 
                            recur=recur+1, 
                            verts_x=gdict["verts-x"], 
                            verts_y=gdict["verts-y"], 
                            verts_recurrence=gdict["verts-recurrence"],
                            edges_parent=gdict["edges-parent"])
            links.append(link)
            if link_ind != 0:# don't re-add the first link
                parent_names.append(link_name)
            link_ind = link_ind + 1

        # now just fix the first link so it links to nothing
        links[0].parent_name = "None"
        return links


#add faces
class JSONLink:
    def __init__(self, name, parent_name, recur, 
                verts_x=20, 
                verts_y=20,
                verts_recurrence=0,
                edges_parent=0):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur 
        self.verts_x = verts_x 
        self.verts_y = verts_y
        self.verts_recurrence = verts_recurrence
        self.edges_parent = edges_parent
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