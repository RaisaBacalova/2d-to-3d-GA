import numpy as np
from numpy import interp
# from matplotlib import pyplot as plt
import math

class ImagePreprocessing():
    @staticmethod
    def imgToGrayscale():
        import cv2 as cv
        #change image
        img0 = cv.imread('images/apple3.jpg')
        RGB_img = cv.cvtColor(img0, cv.COLOR_BGR2RGB)

        gray = RGB_img.copy()

        for y in range(len(gray)):
            for x in range(len(gray[y])):
                r = gray[y][x][0]
                g = gray[y][x][1]
                b = gray[y][x][2]
                gr = r * 0.299 + g * 0.587 + b * 0.0114 #LUMA ratios

                gray[y][x][0] = gray[y][x][1] = gray[y][x][2] = gr

        return gray
        

    @staticmethod
    def edgeDetection():
        import cv2 as cv
        gray = ImagePreprocessing.imgToGrayscale()
        edges = cv.Canny(gray,300,400)

        return edges
        

    @staticmethod
    def outlineVerts():
        edges = ImagePreprocessing.edgeDetection()
        arr = []

        for y in range(len(edges)):
            for x in range(len(edges[y])):
                if edges[y][x] == 255:
                    #display white values
                    #print(y,x, edges[x][y]) 
        
                    arr.append((y,x)) #row - y, col - x
        return arr

    @staticmethod
    def outlineVertsPoly():
        arr = ImagePreprocessing.outlineVerts()
        outVerts = []

        #even only
        poly = 20

        for i in range(len(arr))[::poly]:
            outVerts.append((arr[i][1], arr[i][0]))

        return outVerts

    @staticmethod
    def oposVerts():
        arr = ImagePreprocessing.outlineVerts()
        
        #even only
        poly = 20
        # #couple opposite vertices together based on the same y value
        arr2 = []
        
        for i in range(len(arr))[::poly]:
            for j in range(len(arr)):
                if (arr[i][0] == arr[j][0]):
                    if (arr[i] != arr[j]):
                        arr2.append(arr[i])
                        arr2.append(arr[j])
                        break
        
        # print('Arr2: ', arr2)
        # print('Len: ', len(arr2))
        return arr2

    
    @staticmethod
    def distCalculation():
        arr2 = ImagePreprocessing.oposVerts()
        
        #find distance between opposite vertices
        distArr = []
        
        for i in range(len(arr2)):
            n = i+1
            if (i == 0):
                dist = arr2[i][1] - arr2[n][1]
                distArr.append(abs(dist))
            else:
                if (len(arr2) % 2 != 0):
                    if (n % 2 == 0 and n != len(arr2)-1):
                        dist = arr2[n][1] - arr2[n+1][1]
                        distArr.append(abs(dist))
                else:
                    if (n % 2 == 0 and n != len(arr2)):
                        dist = arr2[n][1] - arr2[n+1][1]
                        distArr.append(abs(dist))
                        
        # print('distArr: ', distArr)
        # print(len(distArr))
        return distArr


    @staticmethod
    def innerVerts():
        import pybresenham as bresenham
        arr2 = ImagePreprocessing.oposVerts()
        arr3 = []
        for i in range(len(arr2)):
            n = i+1
            if (i == 0):
                arr3.append(list(bresenham.line(arr2[i][1], arr2[i][0], arr2[n][1], arr2[n][0])))
            else:
                if (len(arr2) % 2 != 0):
                    if (n % 2 == 0 and n != len(arr2)-1):
                        arr3.append(list(bresenham.line(arr2[n][1], arr2[n][0], arr2[n+1][1], arr2[n+1][0])))
                else:
                    if (n % 2 == 0 and n != len(arr2)):
                        arr3.append(list(bresenham.line(arr2[n][1], arr2[n][0], arr2[n+1][1], arr2[n+1][0])))
        return arr3
    
    @staticmethod
    def addingZ():
        arr3 = ImagePreprocessing.innerVerts()
        distArr = ImagePreprocessing.distCalculation()

        #even only
        poly = 20
        
        for i in range(len(arr3)):
            firstHalf = math.ceil(len(arr3[i])/2)
            secondHalf = len(arr3[i])-firstHalf
            # print(firstHalf, secondHalf)
            # print("Len :", len(arr3[i]), firstHalf, distArr[i])
            for j in range(len(arr3[i]))[:firstHalf:]:
                # print("First half: ")
                # print(arr3[i][j])
                arr3[i][j] += (j + len(arr3[i])/distArr[i],)
                # print(arr3[i][j])
                
            for j in range(len(arr3[i]))[firstHalf::]:
                # print("Second half: ")
                temp = (j-secondHalf)*2
                # print(temp)
                arr3[i][j] += (j + len(arr3[i])/distArr[i] - temp,)    
                # print(arr3[i][j])

        verts = []

        for i in range(len(arr3)):
            for j in range(len(arr3[i])-1)[1::poly]:
                verts.append([arr3[i][j][0], arr3[i][j][1], arr3[i][j][2]])
        
        return verts
    
    @staticmethod
    def beforeEdgeCreation():
        verts = ImagePreprocessing.addingZ()
        
        # couple opposite vertices together based on the same y value
        arr4 = []
        temp = []
        temp1 = []
        
        #add the last singles
        for i in range(len(verts)):
            for j in range(len(verts)):
                if (verts[i][1] == verts[j][1]):
                    v = verts[i]
                    # print(v, verts[j])
                    if (verts[i] == verts[j]):
                        # print("V1: ", v)
                        temp1.append(v)
                    if (verts[i] != verts[j]):
                        # print("I: ", verts[i])
                        if (len(temp1) > 0):
                            temp1.pop()
                            # print("Temp1: ", temp1)
                            for t in range(len(temp1)):
                                arr4.append(list([temp1[t]]))
                            temp1 = []
                        if(verts[i][1] == verts[j][1]):
                            lastV = verts[i+1][1]
                            temp.append(verts[i])
                            if(len(temp) > 1 and verts[i][1] != verts[i-1][1] or verts[i][1] != lastV):
                                arr4.append(temp) 
                                temp = []
                            break

            #sort it
            for i in range(len(arr4)):
                for j in range(len(arr4[i])):
                    arr4[i].sort()

        return arr4


    @staticmethod
    def checkZWithGray():
        arr4 = ImagePreprocessing.beforeEdgeCreation()
        gray = ImagePreprocessing.imgToGrayscale()
        
        for i in range(len(arr4)):
            for j in range(len(arr4[i])):
                x = arr4[i][j][0]
                y = arr4[i][j][1]
                z = arr4[i][j][2]
                gr = gray[y][x][0]
                # print(x, y, z, gr)
        
                if (gr < 127):
                    z = interp(gray[y][x][0],[0,255],[z,z-(gray[y][x][0])/100])
                    arr4[i][j][2] = float(z)
                else:
                    z = interp(gray[y][x][0],[0,255],[z,z+(gray[y][x][0])/100])
                    arr4[i][j][2] = float(z)
                    
        return arr4

    

