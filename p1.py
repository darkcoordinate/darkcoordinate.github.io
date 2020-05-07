import bpy.ops as b
import bpy as bp
import numpy as np
import math as mt
import re 
print("hello")

k = open("/home/hagia-sophia/darkcoordinate.github.io/c3.xyz").read().split("\n")
l = [i.split(" ") for i in k[2:]][:-1]
k = []
for i in l:
	d = []
	d.append(i[1])
	d.append(float(i[2]))
	d.append(float(i[3]))
	d.append(float(i[4]))
	k.append(d)
	r=0.2
	material = bp.data.materials.get("Material")
	if(i[1].lower() == "c"):
		r = 0.30
		material = bp.data.materials.get("Material.002")
	elif(i[1].lower() == "f"):
		r = 0.30
		material = bp.data.materials.get("Material.001")
	elif(i[1].lower() == "b"):
		r = 0.30
		material = bp.data.materials.get("Material.004")
	elif(i[1].lower() == "n"):
		r = 0.30
		material = bp.data.materials.get("Material.003")
	b.mesh.primitive_uv_sphere_add(radius=r,enter_editmode=False, location=d[1:])
	b.object.shade_smooth()
	if(bp.context.active_object.data.materials):
		bp.context.active_object.data.materials[0] = material
	else:
		bp.context.active_object.data.materials.append(material)
print(k)

for i in range(len(k)-1):
	for j in range(i+1, len(k)):
		v1 = np.array(k[i][1:])
		v2 = np.array(k[j][1:])
		v = v2 -v1
		val = np.linalg.norm(v)
		print("printing %d %d %f %f %f %f"%(i,j,v[0],v[1],v[2],val))
		if(val <= 1.9 and k[i][0].lower() != "h" and k[i][0].lower() != "h" ):
			loc = (v1+v2)/2.0
			theta= mt.acos(v[2]/val)
			rot = np.array([-v[1]/val,v[0]/val,0])
			b.mesh.primitive_cylinder_add(radius=0.1,vertices=16, depth=val, enter_editmode=False,location=loc)
			b.object.shade_smooth()
			b.transform.rotate(value=theta,orient_matrix=[[0,0,1],[0,0,1],rot])