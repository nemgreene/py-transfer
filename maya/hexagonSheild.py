import maya.cmds as m
import random
random.seed(random.uniform(10, 20))

list = m.ls("*pCylinder*", type="transform", geometry=True)
if len(list) > 0:
    add = m.ls("*targetShape*", type="transform", geometry=True)
    list.append(add[0])
    m.delete(list)

driver = m.polySphere(n="targetShape")

targ = m.polyCylinder(r=1, h=0.1, sx=6, sy=1)
bev = m.polyBevel(targ, oaf=.2)

def randomIzer(x, y):
    return map(lambda i: random.uniform(x, y), [1, 2, 3])
    
instanceGroup = cmds.group(empty=True,  name=targ[0]+"instanceGroup")


for i in range (0, 100):
    instanceResult = m.instance(targ, name = targ[0] + "_instance#")
    m.parent(instanceResult, instanceGroup)

    [x, y, z] = randomIzer(8, -8)
    m.move(x, y, z, instanceResult)

    [x, y, z] = randomIzer(180, -180)
    m.rotate(x, y, z, instanceResult)

    [x, y, z] = randomIzer(1, .5)
    m.scale(x, x, x, instanceResult)

    m.aimConstraint(driver, instanceResult, aim = [0, 1,0 ] )

m.hide(targ)
m.xform(instanceGroup, centerPivots=True)

m.cutKey(instanceGroup, time=(start, end), attribute='rotateY')
m.setKeyframe(instanceGroup, time=start, attribute="rotateY", value=0)
m.setKeyframe(instanceGroup, time=end, attribute="rotateY", value=360)
m.selectKey(instanceGroup, time=(start, end), at="rotateY")
m.keyTangent(itt="linear", ott="linear")
