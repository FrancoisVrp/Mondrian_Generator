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

HOW TO LAUNCH

To make it run, you just have to drag and drop the script in the blender text editor, then run the script.
Don't hesitate to create multiple materials.

You can activate the automatic delete of all selectable objects in the scene by deleting the # in front oef the 204-205 lines.
"""
