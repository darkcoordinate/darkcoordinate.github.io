import numpy as np
import re
import ase.io.xyz
import bpy.ops as b
import bpy as bp
import numpy as np
import math as mt
import ase.neighborlist as ng

print("hello")


def load(s):
    return ase.io.read("/home/hagia-sophia/darkcoordinate.github.io/data2.xyz",index=':')

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

mat = {"C":"Material.003", "H":"Material.001"}
size = {"C":0.3, "H":0.2}
l = load('h')
def create_inital_bond():
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

def create_bond(m,bond):
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

bond = create_inital_bond()

atom_name = []
for i in range(len(l[0].positions)):
    print(i)
    atom_name.append(addBalls(l[0].positions[i],size[l[0].symbols[i]],getMaterialByName(mat[l[0].symbols[i]])))

print(atom_name)
bond_name = []
for i in bond:
    bond_name.append(draw_bond(i))

print(bond_name)


for i in range(len(l)):
    for j in range(len(l[i].positions)):
        ob = bp.data.objects[atom_name[j]]
        ob.select_set(state=True)
        ob.location = l[i].positions[j]
        ob.keyframe_insert(data_path="location",frame=(i*2))
        ob.select_set(state=False)
    bond2 = create_bond(int(i),bond)
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
