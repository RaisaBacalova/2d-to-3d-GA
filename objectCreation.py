import imgPreprocessing
import numpy as np
from numpy import interp
import math
import random

class ObjectCreation():
    def __init__(self):
        self.vertsToDicts = ObjectCreation.vertsToDicts()
        self.fitnessArr = ObjectCreation.fitnessDict(self.vertsToDicts)
        self.objF = ObjectCreation.objFitness(self.fitnessArr)
        self.blenderVerts = ObjectCreation.vertsForBlender(self.fitnessArr)
        self.blenderEdges = ObjectCreation.edgesForBlender(self.vertsToDicts)
    
    @staticmethod
    #gene creation
    def vertsToDicts():
        arr4 = imgPreprocessing.ImagePreprocessing.checkZWithGray()
        
        arr5 = arr4
        count = -1
        
        for i in range(len(arr4)):
            for j in range(len(arr4[i])):
                count +=1
                arr5[i][j] = {"id": count, "data": arr4[i][j], "fitness_val": 0}

        #randomize internal vectors' x and z values
        for i in range(len(arr5)):
            for j in range(len(arr5[i])):
                if(len(arr5[i]) > 2):
                    if (j != 0 and j != len(arr5[i])-1):
                        randX = random.randrange(arr5[i][j-1]['data'][0], arr5[i][j+1]['data'][0])
                        randZ = random.triangular(arr5[i][j-1]['data'][2], arr5[i][j+1]['data'][2])
                        arr5[i][j]['data'] = [randX, arr5[i][j]['data'][1], randZ]
                        
        return arr5

    @staticmethod
    def fitnessDict(vToDicts):
        arr5 = vToDicts
        fitArr = arr5
        
        for i in range(len(arr5)):
            for j in range(len(arr5[i])):
                randomForce = round(random.triangular(0, 100), 2)
                # print(randomForce, fitArr[i][j]['data'])

                qx = round(randomForce/fitArr[i][j]['data'][0], 2)
                qy = round(randomForce/fitArr[i][j]['data'][1], 2)
                qz = round(randomForce/fitArr[i][j]['data'][2], 2)

                #the lesser the better - more resistance
                q = 0
                qMain = (qx + qy + qz)
                if (qMain != 0):
                    q = round(1/qMain, 3)
                else:
                    q = round(1/1, 3)
                # print(q)
                fitArr[i][j]['fitness_val'] = q

        return fitArr
    
    @staticmethod
    def objFitness(fitArrPassed):
        # fitArr = ObjectCreation.fitnessDict()
        fitArr = fitArrPassed

        objF = 0

        for i in range(len(fitArr)):
            for j in range(len(fitArr[i])):
                # print(fitArr[i][j]['data'], fitArr[i][j]['fitness_val'])
                objF += fitArr[i][j]['fitness_val']

        return round(objF, 3)
        
    
    @staticmethod
    def vertsForBlender(fitDict):
        # arr5 = ObjectCreation.fitnessDict()
        arr5 = fitDict
        
        #blender ready verts arr
        verts = []
        
        for i in range(len(arr5)):
            for j in range(len(arr5[i])):
                verts.append(arr5[i][j]['data'])

        return verts


    @staticmethod
    def edgesForBlender(vToDicts):
        arr5 = vToDicts
        #add to edges array in the form of [[0, 1], [1, 2]]
        edges = []
        
        for i in range(len(arr5)):
            for j in range(len(arr5[i])):
                if(len(arr5[i]) < 2):  
                    edges.append([arr5[i][j]['id'], arr5[i+1][j]['id']])
                else:
                    #when next array is larger or smaller than the current array
                    if (i != len(arr5)-1):
                        if (len(arr5[i]) != len(arr5[i+1])):
                            #when j is not the last index
                            if (j != len(arr5[i])-1):
                                edges.append([arr5[i][j]['id'], arr5[i][j+1]['id']])
                
                                if (i != len(arr5)-1):  
                                    tempDist = []
                
                                    if(j == 0):
                                        count = 0
                                    else:
                                        count = ind
                
                                    for c in range(len(arr5[i+1]))[count::]:
                                        x = pow(abs(arr5[i][j]['data'][0] - arr5[i+1][c]['data'][0]), 2)
                                        y = pow(abs(arr5[i][j]['data'][1] - arr5[i+1][c]['data'][1]), 2)
                                        dist = round(math.sqrt(x + y), 2)
                
                                        edges.append([arr5[i][j]['id'], arr5[i+1][c]['id']])
                                        tempDist.append(dist)
                                        # print(arr5[i][j]['id'], arr5[i+1][c]['id'], tempDist)
                                        
                                        if (len(tempDist) > 0 and dist > tempDist[0]):
                                            edges.pop()
                                            ind = c-1
                                            break
                            # when j is the last index
                            else:
                                if(i != len(arr5)-1):
                                    for c in range(len(arr5[i+1]))[ind::]:
                                      edges.append([arr5[i][j]['id'], arr5[i+1][c]['id']])
                        #when arrays are equal
                        else:
                            if (j != len(arr5[i])-1):
                                edges.append([arr5[i][j]['id'], arr5[i][j+1]['id']])
                                if (i != len(arr5)-1):
                                    edges.append([arr5[i][j]['id'], arr5[i+1][j]['id']])
                            else:
                                if(i != len(arr5)-1):
                                    edges.append([arr5[i][j]['id'], arr5[i+1][len(arr5[i+1])-1]['id']])
        return edges

    @staticmethod
    def toJson(self, id):
        import json

        crDict = {
            'objDict': [],
            'fitNum': 0,
            'objEdges': []
        
        }

        crDict['objDict'] = self.fitnessArr
        crDict['fitNum'] = self.objF
        crDict['objEdges'] = self.blenderEdges

        with open('creatures_json/objData_' + str(id) + '.txt', 'w') as json_file:
            json.dump(crDict, json_file)

        return json_file

    
    @staticmethod
    def createChildDNA(self, child, newGen, pool_gen, gen):
        import json
        
        self.vertsToDicts = child
        self.fitnessArr = ObjectCreation.fitnessDict(self.vertsToDicts)
        self.objF = ObjectCreation.objFitness(self.fitnessArr)
        self.blenderVerts = ObjectCreation.vertsForBlender(self.fitnessArr)
        self.blenderEdges = ObjectCreation.edgesForBlender(self.vertsToDicts)

        chDict = {
        'objDict': [],
        'fitNum': 0,
        'objVerts': [],
        'objEdges': []
        }

        chDict['objDict'] = self.fitnessArr
        chDict['fitNum'] = self.objF
        chDict['objVerts'] = self.blenderVerts
        chDict['objEdges'] = self.blenderEdges

        if (newGen == False):
            with open('creatures_json/childDict_poolGen_' + str(pool_gen) + '_gen_' + str(gen) + '.txt', 'w') as json_file:
                json.dump(chDict, json_file)
        else:
            with open('creatures_json/newChildDict_poolGen_' + str(pool_gen) + '_gen_' + str(gen) + '.txt', 'w') as json_file:
                json.dump(chDict, json_file)

        return chDict