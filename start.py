import bpy
import sys
import os 

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import renderFinalObj


verts = []
edges = []
faces = []

verts = renderFinalObj.RenderFinalObj.objVertices()
edges = renderFinalObj.RenderFinalObj.objEdges()
        

#blender code
new_mesh = bpy.data.meshes.new('new_mesh')
new_mesh.from_pydata(verts, edges, faces)
new_mesh.update()

# make object from mesh
new_object = bpy.data.objects.new('new_object', new_mesh)

# make collection
new_collection = bpy.data.collections.new('new_collection') #or use get
bpy.context.scene.collection.children.link(new_collection)

# add object to scene collection
new_collection.objects.link(new_object)