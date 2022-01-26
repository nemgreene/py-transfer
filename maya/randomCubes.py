import maya.cmds as m
import random
import math
random.seed(random.uniform(10, 20))

result = m.polyCube(n="init")

transform = result[0]

def randomIzer(x, y):
    return map(lambda i: math.floor(random.uniform(x, y)), [1, 2, 3])
    
blacklist = cmds.group(empty=True,  name="blacklist")
    
for i in range (0, 200):
    instanceResult = m.instance(transform, name = transform + "_instance#")
    m.parent(instanceResult, blacklist)

    [x, y, z] = randomIzer(10, -10)
    m.move(x, 0, z, instanceResult)

    # [x, y, z] = randomIzer(180, -180)
    # m.rotate(x, y, z, instanceResult)

    # [x, y, z] = randomIzer(1, .5)
    m.scale(.7, .7, .7, instanceResult)

m.hide(transform)
m.xform(blacklist, centerPivots=True)
m.select(cl=1)