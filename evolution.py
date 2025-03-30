import population
import objectCreation

import json
import random

class Evolution():
    def __init__(self, pool_size, gen_size):
        self.pool_size = pool_size #has to be more than 1
        self.gen_size = gen_size
        # self.pool = Evolution.popCreation(self.pool_size, self.gen_size)
        # self.parentID = Evolution.popSelection(self.pool_size, self.gen_size, pool)
        
        # self.parentsArr = Evolution.newGenCreation(self.pool_size, self.gen_size)
        # self.g3 = Evolution.crossover(self.pool_size, self.gen_size, self.parentsArr)
        self.newGen = Evolution.generationCreation(self, self.pool_size, self.gen_size)
    
    @staticmethod
    def popCreation(p, g):
        pop = population.Population(p)
        
        for i in range(len(pop.creatures)):
            pop.creatures[i].toJson(pop.creatures[i], i)

        pool = pop.creatures

        return pool
            
    @staticmethod
    def popSelection(p, g, pool):
        fits = []
        
        for i in range(len(pool)):
            with open('creatures_json/objData_' + str(i) + '.txt', "r") as file:
                data = json.load(file)
                fitN = data['fitNum']
                fits.append(fitN)
          
        print('Fits: ', fits)
              
        #print fitness map
        fitmap = population.Population(len(pool)).get_fitness_map(fits)
        print('Fitmap: ', fitmap)

        #print selected parent
        parentID = population.Population(len(pool)).select_parent(fitmap)
        print('Parent id: ', parentID)

        return parentID

    @staticmethod
    def newGenCreation(self, p, g, end_of_gen, newParent, new_parents_arr):
        if (end_of_gen == False):
            parents = []
            #2 parents
            for i in range(2):
                parent = Evolution.popSelection(self.pool_size, self.gen_size, 
                                                Evolution.popCreation(self.pool_size, self.gen_size))
                print('newGenCreation: ', parent)
                parents.append(parent)
                
                with open('creatures_json/objData_' + str(parent) + '.txt', "r") as file:
                    data = json.load(file)
        
                with open('creatures_json/parentData_pool_' + str(i) + '_parent_'+ str(parent) + '_poolGen_' + str(p) + '_gen_' + str(g) + '.txt', 'w') as json_file:
                    json.dump(data, json_file)
            return parents
        else:
            new_parent = newParent
            print('newParentsCreation: ', new_parent)

            if(len(new_parents_arr) < 2):
                with open('creatures_json/childDict_poolGen_' + str(len(new_parents_arr)-1) + '_gen_' + str(g) + '.txt', "r") as file:
                    data = json.load(file)
                with open('creatures_json/newParentData_pool_'+ str(0) + '.txt', 'w') as json_file:
                    json.dump(data, json_file)
            else:
                with open('creatures_json/childDict_poolGen_' + str(len(new_parents_arr)-1) + '_gen_' + str(g) + '.txt', "r") as file:
                    data = json.load(file)
                with open('creatures_json/newParentData_pool_'+ str(1) + '.txt', 'w') as json_file:
                    json.dump(data, json_file)

            # print(new_parent)

            return new_parent
       
    @staticmethod
    def crossover(p, g, parents, newGen):
        # ps = Evolution(self.pool_size, self.gen_size).newGenCreation(Evolution(self.pool_size, self.gen_size))
        # print(ps)
        pNum = p
        gNum = g

        p1 = {}
        p2 = {}

        if (newGen == False):
            with open('creatures_json/parentData_pool_0_parent_' + str(parents[0]) + '_poolGen_' + str(p) + '_gen_' + str(g) + '.txt', "r") as file:
                    p1 = json.load(file)
    
            with open('creatures_json/parentData_pool_1_parent_' + str(parents[1]) + '_poolGen_' + str(p) + '_gen_' + str(g) + '.txt', "r") as file:
                    p2 = json.load(file)
        else: 
            print('New gen starts')
             
            with open('creatures_json/newParentData_pool_0.txt', "r") as file:
                    p1 = json.load(file)
    
            with open('creatures_json/newParentData_pool_1.txt', "r") as file:
                    p2 = json.load(file)

        # print('Parent1')
        # print(p1)
        # print('Parent2')
        # print(p2)

        g3 = p1['objDict']
        # print(g3)

        #crossover
        for i in range(len(p1['objDict'])):
            for j in range(len(p1['objDict'][i])):
                p = random.randint(0, 100)
                #print(p)
                if (p1['objDict'][i][j]['fitness_val'] > p2['objDict'][i][j]['fitness_val']):
                    fittest = p1['objDict'][i][j]
                    lessFittest = p2['objDict'][i][j]
                else:
                    fittest = p2['objDict'][i][j]
                    lessFittest = p1['objDict'][i][j]    
                # print("Fittest: ", fittest, "Less fittest: ", lessFittest)
                x = abs(p1['objDict'][i][j]['data'][0] - p2['objDict'][i][j]['data'][0])
                # print('X: ', x)
                distX = round(x * p/100)
                # print('DistX: ', distX)
                #check x vals
                if(fittest['data'][0] > lessFittest['data'][0]):
                    fittestXLarger = True
                else:
                    fittestXLarger = False
                # print(fittestXLarger)

                #toward p with lower f.val
                if (fittestXLarger):
                    g3[i][j]['data'][0] = fittest['data'][0] - distX 
                else:
                    g3[i][j]['data'][0] = fittest['data'][0] + distX


                z = abs(p1['objDict'][i][j]['data'][2] - p2['objDict'][i][j]['data'][2])
                # print('Z: ', z)
                distZ = round(z * p/100)
                # print('DistZ: ', distZ)
                #check z vals
                if(fittest['data'][2] > lessFittest['data'][2]):
                    fittestZLarger = True
                else:
                    fittestZLarger = False
                # print(fittestZLarger)

                #toward p with higher f.val
                if (fittestZLarger):
                    g3[i][j]['data'][2] = lessFittest['data'][2] + distZ 
                else:
                    g3[i][j]['data'][2] = lessFittest['data'][2] - distZ
                g3[i][j]['fitness_val'] = 0
                    
        # print('G3: ', g3)

        #mutation
        # rate = 0.01
        for i in range(len(g3)):
            for j in range(len(g3[i])):
                if(len(g3[i]) > 2):
                    if (j != 0 and j != len(g3[i])-1):
                        # print('G3: ', 3[i][j])
                        r = random.randint(0, 10)
                        # print(r)
                        # rp = r/100
                        # if (rp < rate):
                        g3[i][j]['data'][2] += r
                        

        # print('G3M: ', g3)
        
        if (newGen == False):
            with open('creatures_json/childData.txt', 'w') as json_file:
                json.dump(g3, json_file)
    
            with open('creatures_json/childData.txt', "r") as file:
                childData = json.load(file)
                
            g3Json = objectCreation.ObjectCreation.createChildDNA(objectCreation.ObjectCreation(), childData, newGen, pNum, gNum)
        else:
            with open('creatures_json/newChildData.txt', 'w') as json_file:
                json.dump(g3, json_file)
    
            with open('creatures_json/newChildData.txt', "r") as file:
                childData = json.load(file)

            g3Json = objectCreation.ObjectCreation.createChildDNA(objectCreation.ObjectCreation(), childData, newGen, pNum, gNum)

        # print('P: ', pNum, str(pNum))
        
        return g3Json

    @staticmethod
    def generationCreation(self, p, g):
        # parents = Evolution.newGenCreation(p, g)
        new_gen = []
        new_parents = []
        end_of_gen = False
        newGen = False
        
        for j in range(g):
            print('J: ', j)
            new_gen = []
            for i in range(p):
                print('I: ', i)
                print('J: ', j)
                
                self.parentsArr = Evolution.newGenCreation(self, i, j, end_of_gen, None, None)
                self.g3 = Evolution.crossover(i, j, self.parentsArr, newGen)
                
                new_gen.append(self.g3)
                print('New gen1: ', len(new_gen))
                
                if (len(new_gen) == p):
                    print('end of gen')
                    end_of_gen = True
                    
                    fits = []
                    for i in range(len(new_gen)): 
                        with open('creatures_json/childDict_poolGen_' + str(i) + '_gen_' + str(j) + '.txt', "r") as file:
                            data = json.load(file)
                            fitN = data['fitNum']
                            fits.append(fitN)
                    
                    print('Fits: ', fits)
                        
                    #print fitness map
                    fitmap = population.Population(len(new_gen)).get_fitness_map(fits)
                    print('Fitmap: ', fitmap)
            
                    #print selected parent
                    parentID = population.Population(len(new_gen)).select_parent(fitmap)
                    print('Parent id: ', parentID)

                    new_parents.append(parentID)
                    print('New parents arr: ', new_parents)
                    self.parentsArr = Evolution.newGenCreation(self, i, j, end_of_gen, parentID, new_parents)
                    
                    #unblock this for more than 1 gen
                    # new_gen = []
                    end_of_gen = False

                    if(len(new_parents) > 2):
                        new_parents = []
                        print('New parents arr cleared: ', new_parents)
                    
                    if (len(new_parents) > 1):
                        newGen = True
                        self.g3 = Evolution.crossover(p, g, new_parents, newGen)
                        print('New gen2: ', len(new_gen))
                        new_gen.append(self.g3)
                        newGen = False
        
        if(len(new_gen) > 2):
            with open('creatures_json/renderObj.txt', 'w') as json_file:
                json.dump(new_gen[2], json_file)
        else:
            with open('creatures_json/renderObj.txt', 'w') as json_file:
                json.dump(new_gen[0], json_file)
                    
        return new_gen
    