import json

class RenderFinalObj():

    @staticmethod
    def readFile():
        with open('creatures_json/renderObj.txt', "r") as file:
            data = json.load(file)

        return data
    
    @staticmethod
    def objVertices():
        data = RenderFinalObj.readFile()
        return data['objVerts']
    
    @staticmethod
    def objEdges():
        data = RenderFinalObj.readFile()
        return data['objEdges']