Imports required:
	numpy
	opencv-python
  	PyBresenham
  	bpy
  	jupyter
  	matplotlib

Instructions to run the program
	- open cmd and navigate to the program location
  	- copy and paste the following into cmd
    		- python
    		- import evolution
  	- at the next step define the number for the pool size and the number for generations
		- for example: 
			- evolution.Evolution(pool size, generations) will look as following:
			- evolution.Evolution(2,1)
    	- copy and paste amended "evolution.Evolution(2,1)" into cmd
	- the program will take some time to evolve the object. Once it is done, type 'exit()'
	- now open Blender, navigate to the Scripting tab and open the 'start.py' script, run it
	- to add faces to the object, select the object, switch to Edit Mode, and press F

Instructions to change poly num
	- navigate to the program's folder
	- find and open imgPreprocessing.py file
	- scroll down to outlineVertsPoly() and change "poly" value to any even number larger than 2
	- change the same value in oposVerts() as well
	- save file

Instructions to change rendered obj
	- navigate to the program's folder and open "creatures_json" folder
	- choose any object's file and copy its contents 
	- open "renderObj" file, delete all its data and paste new content
	- save the file

Instructions to change the image 
	- remove background from your image at https://www.remove.bg/upload, save image
	- convert saved image from png to jpg at https://www.freeconvert.com/png-to-jpg, apply black background before converting
	- open imgPreprocesing.py file
	- find '#change image' in imgToGrayscale() function
	- change the name to your new .jpg image's name
	- save file 
