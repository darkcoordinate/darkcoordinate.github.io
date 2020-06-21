#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
o = open(sys.argv[1]).read().split("\n")
x = [float(i.split(" ")[1]) for i in o[1:-1]]
y = [float(i.split(" ")[2]) for i in o[1:-1]]
plt.plot(x,y)
plt.savefig("mopac.png")
plt.show()
	
