"""
Author  : Anurag Singh
email   : sagacious112358@gmail.com

============
Licence
============

Copyright (c) 2020 Anurag Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


===========
Description
===========

This is a blender plugin made to run on blender 2.82 If it works some where else 
enjoy.
"""
import bpy
import numpy as np
import re
import ase.io.xyz
import bpy.ops as b
import bpy as bp
import numpy as np
import math as mt
import ase.neighborlist as ng
from bpy_extras.io_utils import ImportHelper

print("hello")


mat = {"C":"Material.003", "H":"Material.001", "B":"Material.004", "O":"Material.005"}
size = {"C":0.3, "H":0.2,"B":0.3,"O":0.3}

def load(s):
    return ase.io.read(s,index=':')

def getMaterialByName(name):
    return bp.data.materials.get(name)

def addBalls(loc, r,material):
    #bp.context.active_object.data.name
    b.mesh.primitive_uv_sphere_add(radius=r,enter_editmode=False, location=loc)
    b.object.shade_smooth()
    print(bp.context.active_object.data.name)
    if(bp.context.active_object.data.materials):
        bp.context.active_object.data.materials[0] = material
    else:
        bp.context.active_object.data.materials.append(material)
    return bp.context.active_object.data.name

def create_inital_bond(l):
    bond = []
    for i in range(len(l[0].positions)-1):
        #print(i)
        for j in range(i+1, len(l[0].positions)):
            v = l[0].positions[j] - l[0].positions[i]
            loc = (l[0].positions[j] + l[0].positions[i])/2.0
            val = np.linalg.norm(v)
            if(val < 2.1 and not(l[0].symbols[i] == "H" and l[0].symbols[j] == "H")):
                bond.append([i,j,val,v, loc])
    return bond

def create_bond(m,bond, l):
    bond2 = []
    for i in range(len(bond)):
        v = l[m].positions[bond[i][1]] - l[m].positions[bond[i][0]]
        loc = (l[m].positions[bond[i][1]] + l[m].positions[bond[i][0]])/2.0
        val = np.linalg.norm(v)
        bond2.append([bond[i][0],bond[i][1],val,v, loc])
    return bond2

def draw_bond(bond):
    theta= mt.acos(bond[3][2]/bond[2])
    #print([-bond[3][1]/bond[2],bond[3][0]/bond[2],0])
    rot = np.array([-bond[3][1]/bond[2],bond[3][0]/bond[2],0])
    b.mesh.primitive_cylinder_add(radius=0.1,vertices=16, depth=bond[2], enter_editmode=False,location=bond[4])
    b.object.shade_smooth()
    b.transform.rotate(value=theta,orient_matrix=[[0,0,1],[0,0,1],rot])
    return bp.context.active_object.data.name 

def draw_everything(s):
    l = load(s)
    bond = create_inital_bond(l)

    atom_name = []
    for i in range(len(l[0].positions)):
        print(i)
        atom_name.append(addBalls(l[0].positions[i],size[l[0].symbols[i]],getMaterialByName(mat[l[0].symbols[i]])))

    print(atom_name)
    bond_name = []
    for i in bond:
        bond_name.append(draw_bond(i))
    print("printint bond name")
    print(bond_name)

    keys = bpy.data.objects.keys()

    atom_name =[]
    bond_name = []
    for i in keys:
        if "Cy" in i:
            bond_name.append(i)
        if "Sp" in i:
            atom_name.append(i)
    for i in range(len(l)):
        print("frame")
        print(i)
        for j in range(len(l[i].positions)):
            ob = bp.data.objects[atom_name[j]]
            ob.select_set(state=True)
            ob.location = l[i].positions[j]
            ob.keyframe_insert(data_path="location",frame=(i*2))
            ob.select_set(state=False)
        bond2 = create_bond(int(i),bond, l)
        for j in range(len(bond_name)):
            theta= mt.acos(bond2[j][3][2]/bond2[j][2])
            #print([-bond[3][1]/bond[2],bond[3][0]/bond[2],0])
            rot = np.array([-bond2[j][3][1]/bond2[j][2],bond2[j][3][0]/bond2[j][2],0])
            ob = bp.data.objects[bond_name[j]]
            bp.ops.object.select_all(action="DESELECT")
            ob.select_set(state=True)
            ob.rotation_mode = "AXIS_ANGLE"
            ob.rotation_axis_angle = [theta,rot[0],rot[1],rot[2]]
            ob.keyframe_insert(data_path="rotation_axis_angle",frame=(i*2))
            ob.location = bond2[j][4]
            ob.keyframe_insert(data_path="location",frame=(i*2))
            ob.select_set(state=False)


class WM_OT_myOp(bpy.types.Operator):
    #Open the add cube Dialog box 
    bl_label = "Add Cube Dialog Box"
    bl_idname = "wm.myop"
    bl_property = bpy.props.StringProperty(name = "Enter ext", default="")
    
    #textse = bpy.props.StringProperty(name = "Enter ext", default="")
    #number = bpy.props.FloatProperty(name = "Scale Z Axiz", default= 1)
    
    def execute(self, context):
        
        #bpy.ops.mesh.primitive_cube_add()
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        
        return context.window_manager.invoke_props_dialog(self)


class ExportSomeData(bpy.types.Operator,ImportHelper):
    """Test exporter which just writes hello world"""
    bl_idname = "export.some_data"
    bl_label = "Export Some Data"
    def execute(self,context):
        print("hello2")
        print(self.filepath)
        draw_everything(self.filepath)
        return {"FINISHED"}


class TestPanel(bpy.types.Panel):
    bl_label = "Object Adder"
    bl_idname = "PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Add Molecule'

    #texre = bpy.props.StringProperty(name = "Enter Text", default="")
    #number = bpy.props.FloatProperty(name = "Scale Z Axiz", default= 1)
    
   
    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
        row.label(text= "Molecule maker ", icon= 'OBJECT_ORIGIN')
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon= 'CUBE')
       
        row.operator("mesh.primitive_uv_sphere_add", icon= 'SPHERE')
        row = layout.row()
        row.operator("export.some_data", icon= 'FILE_FONT', text= "Load File")

       
       
       
def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(ExportSomeData)
    #bpy.utils.register_class(WM_OT_myOp)

def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(ExportSomeData)
    #bpy.utils.unregister_class(WM_OT_myOp)

if __name__ == "__main__":
    register()
    #bpy.ops.export.some_data("INVOKE_DEFAULT")


"""    
def register():
    bpy.utils.register_class(WM_OT_myOp)
        
def unregister():
    bpy.utils.unregister_class(WM_OT_myOp)
    
    
if __name__ == "__main__":
    register()
    
    bpy.ops.wm.myop("INVOKE_DEFAULT")"""