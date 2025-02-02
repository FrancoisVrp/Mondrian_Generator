""" 
This scrit generate a Mondrian inspired shape.

A 3D matrix is created with the size of a global cube. Each element of the
matrix is equal to 0 or 1, 0 for empty, 1 for filled.
Each time a cube is created in the global cube, each matrix element contained in
the generated cube bounds, get a 1.

Each time the script wants to produce a cube, it analyses linearly in x, y and z
if an elements is equal to 1. If not the maximum size of the generated cube 
increase, if it is true, the maximum size of the generated cube is set to the 
element coordinate - 1.

FUTURE UPDATES :

In 1.1, the script analyse linearly and seperately in x, y and z, if a cube is
already here. By this logic, it does not analyse elements far from the edges of
the cube, and to be more precise, the edges starting from the where is the
origin of the cube (to scale from the already filled last element, through 
empty ones).

In 1.2, I would like to solve this problem that generate some clipping objects,
especially on the top of the generated shape.
To do that, I would like to use a OctTree logic, with a treshold limit to check
the inside of the potential generated cube.
It could still start from a corner, but when an edge is analysed (an already
filled element or the boundary is found on the way) it will divide the edge in
two, to analyse in the two other axis if an object is found, and repeat the
action.

In 1.3, I would also like to change the for loop that analyse each matrix
element equal to 0 or 1. As I create shapes in certain order, i would like
to skip some steps where it is obvious that it is already filled.
For example, when a cube is created, all the x+1 in the range of the generated
cube are obviously already filled. I would like to skip whith some conditions,
or a second matrix analyses to be more effective, and reduce the number of 
steps analyses.
"""

__name__ = 'Mondrian Generator'
__version__ = '1.1'
__author__ = 'FrancoisVrp'

# COMMANDS IMPORT :

import bpy
import random
from bpy.types import Panel,Operator



# VARIABLES :

# Shortcuts for all call of a bpy.whatever.
ba = bpy.app
bc = bpy.context
bd = bpy.data
bm = bpy.msgbus
bo = bpy.ops
bpa = bpy.path
bpr = bpy.props
bt = bpy.types
bu = bpy.utils

# Global Cube Variables.
global_length = 20
global_width = 12
global_height = 30

# The max Lenght, Width and Height of a generated cube.
# This value will always change while the free space is analysed.
maxL = 0
maxW = 0
maxH = 0

# Random values in range of the minimum and max length, width and height.
cubeL = 0
cubeW = 0
cubeH = 0

# New cube origin coordinates. 
# The origin is set to the closest corner of the world origin.
xCoordinate = 0
yCoordinate = 0
zCoordinate = 0

# Cursor coordinates.
# The cursor move accross it's axis to analyse if the next elements are filled
# or not.
xCursor = 0
yCursor = 0
zCursor = 0

# The matrix that will keep in mind which space is free or not.
matrix = 0

# Get a list of all materials in the scene
materials = bd.materials

# A percentage of cubes to delete that will change at every generation.
randomRatio = 0

# A seed to control random selecte of cubes.
deleteSeed = 1



# CALLED FUNCTIONS :

# Reduce the max size by analysing if there is an already filled
# space on x, y and z in the matrix. Then it set a new maximum
# distance in function of already filled element or not.
def CursorAnalysis(zCoordinate, yCoordinate, xCoordinate):
    
    global maxL
    global maxW
    global maxH

    global global_length
    global global_width
    global global_height

    for xCursor in range(xCoordinate+1,global_length):
        if matrix[zCoordinate][yCoordinate][xCursor] == 1:
            maxL = xCursor - xCoordinate
            break
    for yCursor in range(yCoordinate+1,global_width):
        if matrix[zCoordinate][yCursor][xCoordinate] == 1:
            maxW = yCursor - yCoordinate
            break                            
    for zCursor in range(zCoordinate+1,global_height):
        if matrix[zCursor][yCoordinate][xCoordinate] == 1:
            maxH = zCursor - zCoordinate
            break
    return maxL, maxW, maxH

# Generate the cube from the CursorAnalysis() data and set its proper location.
def GenerateCubeMesh(zCoordinate, yCoordinate, xCoordinate, cubeL, cubeW, cubeH):

    # Generated a cube of size 1, scaled on each axis.
    bo.mesh.primitive_cube_add(size = 1, 
                               location = (0, 0, 0), 
                               scale = (cubeL, cubeW, cubeH))
                
    # Set the new cube origin to its closest corner to the world origin.
    bc.scene.tool_settings.use_transform_data_origin = True
    bo.transform.translate(value = (-cubeL*0.5, -cubeW*0.5, -cubeH*0.5))
    bc.scene.tool_settings.use_transform_data_origin = False
    
    # Change the cube location to actual matrix element coordinates.
    bc.object.location[0] = xCoordinate
    bc.object.location[1] = yCoordinate
    bc.object.location[2] = zCoordinate

# Change randomly the material of a generated cube.
def SetMaterial():
    # Select a random material to apply to the cube.
    randmaterial = random.choice(materials)
    # Get a reference to the active object and assign the material.
    obj = bpy.context.active_object
    obj.data.materials.append(randmaterial)
     
# Called if a empty element is found in the search empty loop.
def CreateCube(zCoordinate, yCoordinate, xCoordinate):
    
    global global_length
    global global_width
    global global_height

    global maxL
    global maxW
    global maxH

    global cubeL
    global cubeW
    global cubeH

    # Determine the cube maximum size from cursor position.
    maxL = global_length - xCoordinate
    maxW = global_width - yCoordinate
    maxH = global_height - zCoordinate

    CursorAnalysis(zCoordinate, yCoordinate, xCoordinate)

    # Assign random value in range (1, maxDistance) to each axis.
    cubeL = random.randint(1, maxL)
    cubeW = random.randint(1, maxW)
    cubeH = random.randint(1, maxH)

    GenerateCubeMesh(zCoordinate, yCoordinate, xCoordinate, cubeL, cubeW, cubeH)

    SetMaterial()

    # Replace 0 to 1 for each elements in the new cube bounding box.
    for updateCursorZ in range(zCoordinate, zCoordinate+(cubeH)):
        for updateCursorY in range(yCoordinate, yCoordinate+(cubeW)):
            for updateCursorX in range(xCoordinate, xCoordinate+(cubeL)):
                matrix[updateCursorZ][updateCursorY][updateCursorX] = 1



# PROGRAM :

# Delete all selectable objects.
#bo.object.select_all(action='SELECT')
#bo.object.delete(use_global=False, confirm=False)

# Create a 3D matrix with each elements equal to 0.
# 0 is an empty space, 1 will be a filled one.
# The size of the matrix depends on the gloabl cube size.
matrix = [[[0 for xCoordinate in range(global_length)]
            for yCoordinate in range(global_width)]
            for zCoordinate in range(global_height)]

# Search empty loop to generate cube on elements = 0.
for zCoordinate in range(global_height):
    for yCoordinate in range(global_width):
        for xCoordinate in range(global_length):
            # Check if the element is empty or not.
            if matrix[zCoordinate][yCoordinate][xCoordinate] == 0:
                CreateCube(zCoordinate, yCoordinate, xCoordinate)
                
                                        
# Random cube delete.
randomRatio = (random.randint(5,60))*0.01              
bo.object.select_random(ratio=randomRatio, seed=deleteSeed)                
bo.object.delete(use_global=False, confirm=False)


# End of the script.
