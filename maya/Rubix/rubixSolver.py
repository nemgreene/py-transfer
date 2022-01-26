import maya.cmds as m
import math
import time
from random import random

#vector region
#region
# vector substration
def vecsub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
# vector crossproduct
def veccross(x, y):
    v = [0, 0, 0]
    v[0] = x[1]*y[2] - x[2]*y[1]
    v[1] = x[2]*y[0] - x[0]*y[2]
    v[2] = x[0]*y[1] - x[1]*y[0]
    return v
def Normal(v0, v1, v2):
    return veccross(vecsub(v0, v1),vecsub(v0, v2))
# calculate normal from 3 verts
def Normal4(v0, v1, v2, v3):
    return veccross(vecsub(v0, v2),vecsub(v1, v3))
#endregion

dictionary = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
whiteList = []
edgelist=[]
edgesList = []
select = []
kernelList = []
cube = []

# Obj for each node in cube
class Node:
    def __init__(self,id):
        self.id = id
        self.colors = []
        self.faces = []
        self.normalList = []

        cube = m.ls(id)
        shaders = m.listConnections(m.listHistory(cube,f=1),type='lambert')
        for i in range(1,len(shaders)):
            self.colors.append(shaders[i])

    def height(self):
        ret = [0, 0, 0]
        for i in self.normals():
            ret = [ret[0] + i[0], ret[1] + i[1], ret[2] + i[2]]
        return ret

    def name(self):
        return(self.id)

    def normals(self) :
        ret = []
        for c in self.colors:
            ret.append(self.normal(c))
        return ret
    
    def normal(self, color):
        self.normalList = []
        m.select(self.id)
        m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        m.select(self.id)
        m.hyperShade(smn=1) # that will select the shader
        for i in range(int(len(self.colors))):
            s = m.ls(sl=1)[i + 1] # remember the selected shader
            sg = m.listConnections(color +".oc", s=0, d=1)[0] # figure out the shading group
            # select the faces of the same object with same shader attached
            l = []
            for o in m.sets(sg, q=1):
                if self.id not in o: continue
                l.append(o)
                m.select(l, add=1)
                ns = m.polyInfo(l[0], fn=1)[0]
                # edgeList = m.polyListComponentConversion(l[0], ff = 1, te = 1)
                # vertList = m.polyListComponentConversion(edgeList[0], fe = 1, tv = 1)
                # vertList = vertList + m.polyListComponentConversion(edgeList[2], fe = 1, tv = 1)
                # p0, p1, p2, p3 = vertList
                # p0 =  m.xform(p0, q=True, ws=True, t=True)
                # p1 =  m.xform(p1, q=True, ws=True, t=True)
                # p2 =  m.xform(p2, q=True, ws=True, t=True)
                # p3 =  m.xform(p3, q=True, ws=True, t=True)

                # normal = Normal(p0, p1, p2)

                null, null, x, y, z = ns.split()
                self.normalList.append([int(float(x)), int(float(y)), int(float(z))])
        m.select(cl=1)
        return(self.normalList[0])

    def selfSelect(self):
        m.select(str(self.id), add=1)
    
    def position(self, str):
        x, y, z = self.height()
        global re
        if str == "left":
            if x < 0 and z < 0:
                return "xNeg"
            if x > 0 and z < 0:
                return "zNeg"
            if x < 0 and z > 0:
                return "zPos"
            if x > 0 and z > 0:
                return "xPos"
        if str == "right":
            if x < 0 and z < 0:
                return "zNeg"
            if x < 0 and z > 0:
                return "xNeg"
            if x > 0 and z < 0:
                return "xPos"
            if x > 0 and z > 0:
                return "zPos"

        # calling func to test which side of cube colored face is on
        else:
            nX, nY, nZ = self.normal(str)
            hX, hY, hZ = self.height()
            if nZ == 1:
                if hX == -1: 
                    return ["left", self.position("left")]
                if hX == 1: 
                    return ["right", self.position("right")]
            if nZ == -1:
                if hX == -1: 
                    return ["right", self.position("right")]
                if hX == 1: 
                    return ["left", self.position("left")]
            if nX == 1:
                if hZ == -1: 
                    return ["right", self.position("right")]
                if hZ == 1: 
                    return ["left", self.position("left")]
            if nX == -1:
                if hZ == -1: 
                    return ["left", self.position("left")]
                if hZ == 1: 
                    return ["right", self.position("right")]
                    # will return face that is not up
            # if nY == 1 and nX == 0 and nZ == 0:
# obj for machine, rotating relative to view
class Handler :
    def __init__(self, face):
        self.face = face
    
    def top(self, dir):
        direction = "+" if dir == "cw" else "-"
        rotator([0, 1, 0], "pos", direction)
    def bottom(self, dir):
        direction = "-" if dir == "cw" else "+"
        rotator([0, 1, 0], "neg", direction)  
    
    def wingRot(self, orientation, dir):
        wings = [1, 0, 0] if "z" in self.face else [0, 0, 1]
        if self.face == "zNeg" or self.face=="xPos":
            dir = "-" if dir == "cw" else "+"
        else:
            dir = "+" if dir == "cw" else "-"
        rotator(wings, orientation, dir)
    
    def left(self, dir):
        orientation = ("pos" if "Neg" in self.face else "neg") if "z" in self.face else ("pos" if "Pos" in self.face else "neg")
        self.wingRot(orientation, dir)
    
    def right(self, dir):
        orientation = ("pos" if "Neg" in self.face else "neg") if "x" in self.face else ("pos" if "Pos" in self.face else "neg")
        self.wingRot(orientation, dir)

    def facing(self, dir):
        loc = [1, 0, 0] if "x" in self.face else [0, 0, 1]
        orientation = "neg" if "Neg" in self.face else "pos"
        dir = ("+" if dir == "cw" else "-")  if "Neg" in self.face else ("-" if dir == "cw" else "+")
        rotator(loc, orientation, dir)

# generate array of nodes
for i in range(26):
    new = Node(dictionary[i])
    cube.append(new)


def rotator(vec, direction, wise):
    flat = []
    vec = map(lambda x : x * -1 if direction == "neg" else x, vec)
    for i in range(26):
        if vec in cube[i].normals():
            flat.append(cube[i].name())
    m.select(flat)
    m.group(n='rotator')
    m.xform(cp=1)
    vec = map(lambda x :  x if x == 0 else wise + "90deg", vec)
    m.rotate(vec[0], vec[1], vec[2], "rotator")
    m.parent(flat, "cubeGroup")
    m.delete("rotator*")
    m.select(cl=1)
    m.refresh()

def scramble(num):
    dic = ["x", "y", "z"]
    dir = ["pos", "neg"]
    for i in range(num):
        origin = dic[int(random() * 3)]
        input = map(lambda x : 1 if x == origin else 0, dic)
        rotator(input, dir[int(random() * 2)], "+")
        m.refresh()
        
def facingFunction(i, color):
    if len(i.colors) == 2:
        facing = ("x" if i.normal(color)[0] !=0 else "z") + ("Pos" if i.normal(color)[0] + i.normal(color)[2] > 0  else "Neg")
        # facing = ("x" if i.normals()[0][0] !=0 else "z") + ("Pos" if i.normals()[0][0] + i.normals()[0][2] > 0  else "Neg")
        return facing
    if len(i.colors) == 1:
        facing = ("x" if i.normal()[0][0] !=0 else "z") + ("Pos" if i.normals()[0][0] + i.normals()[0][2] > 0  else "Neg")
        return facing

#find all whites and edges
for i in cube:
    if "white" in i.colors:
        whiteList.append(i)
        if len(i.colors) == 2:
            edgelist.append(i)
    if len(i.colors) == 1:
        kernelList.append(i)
    if len(i.colors) == 2:
        edgesList.append(i)

def daisy():
    #make the daisy

    # pass in a machine faced with the node to be flipped 
    def flipEdge(machine):
            machine.facing("cw")
            machine.top("cw")
            machine.right("ccw")

    #check its neighbors to remove adjacent whites

    def neighbors(i):
        passed = [True, "neighhbors"]
        for w in whiteList:
            if i.normal("white") == w.normal("white"):
                x, y, z = i.height()
                if ([x, y + 1, z] == w.height()):
                    passed = [False, "top"]
                elif ([x, y - 1, z] == w.height()):
                    passed = [False, "bottom"]
        return passed
    #daisy Primary
    def primary(i):
        passed = [True, "primary"]
        #make sure were not disrupting daisy already made
        dirV = i.normal("white")
        for l in edgelist:
            # check node is not comparing itself
            if  l.name() == i.name() or l.height()[1] != 1 or passed[0] == False:
                continue
            # if white normal is on the z axis
            if i.normal("white")[2] != 0:
                # the top node on the corresponding X axis must be checked
                if l.height()[0] == i.height()[0]:
                    if l.normal("white")[1] == 1:
                        passed = [False, "primary"]
                    # time.sleep(1)
            #  else if the white normal is on the x axis
            elif i.normal("white")[0] != 0:
                # the top node on the corresponding z axis is checked
                if l.height()[2] == i.height()[2]:
                    if l.normal("white")[1] == 1:
                        #check to see if other rotation is available
                        passed = [False, "primary"]
        return passed
    # finally make sure that moving will not send edge away
    def flat(i):
        passed = [True, "flat"]
        for l in edgelist:
            white = i.normal("white")
            x, y, z = white
            other = filter(lambda x : x != white, i.normals())[0]
            if l.normal("white") == other and l.height()[1] == 0:
                passed = [False, "flat"]
            if l.normal("white") == [x * -1, 0, z * -1]:
                other = filter(lambda x: x != i.normal("white"), i.normals())[0]
                passed = [False, "mirror"]
        return passed
    #check if secondary rotation vector is possible
    def secondary(i):
        passed = [False, "secondary"]
        heightList = []
        for w in whiteList:
            heightList.append(w.height())
        x, y, z = i.normal("white")
        if [x, 1, z] not in heightList:
            passed = [True, "secondary"]
        return passed

    def middleRowUp(i):
        n = neighbors(i)
        p = primary(i)
        s =  secondary(i)
        f = flat(i)

        def recMiddle(i, counter):
            if counter < 0:
                return
            if n[1] == "bottom":
                machine = Handler("xPos")
                machine.bottom("cw")
            if p[0]:
                facing = facingFunction(i, i.colors[0])
                machine = Handler(facing)
                for r in range(4):
                    if i.normal("white")[1] != 1:
                        machine.facing("cw")
                        pass
            if s[0]:
                if i.normal("white")[1] == 1:
                    return
                # run secondary rotation around axis
                machine = Handler(i.position("white")[1])
                for r in range(4):
                    other = filter(lambda x: x != i.normal("white"), i.normals())[0]
                    if other[1] != 1:
                        machine.facing("cw")
            if (p[0] == False and s[0] == False):
                machine = Handler("xPos")
                machine.top("cw")
            #iterate to see if everyone is facing up
                # recMiddle(i, counter - 1)



        recMiddle(i, 4)

    def bottomRowUp(i):
        x, y, z = i.height()
        def rec(counter):
            passed = True
            if counter < 0:
                return
            for w in whiteList:
                if w.height() == [x, 1, z]:
                    passed = False
            if passed == False:
                machine = Handler("xPos")
                machine.top("cw")
                rec(counter - 1)
            elif passed == True:
                face = facingFunction(i, "white")
                machine = Handler(face)
                machine.left("cw")
                machine.facing("cw")

        rec(4)
        
    def bottomFaceUp(obj):

        def rec(i, counter):
            if counter < 0:
                return
            passed = True
            white = i.normal("white")
            other = filter(lambda x : x != white, i.normals())[0]
            face = ("x" if other[0] !=0 else "z") + ("Pos" if other[0] + other[2] > 0  else "Neg")

            for t in edgelist:
                if t.name() == i.name():
                    continue
                x, y, z = obj.height()
                if t.height() == [x, 1, z] and t.name()!= i.name():
                    passed = False

            machine = Handler(face)
            if passed == False:
                machine.top("cw")
                rec(i, counter -1)
            elif passed == True:
                machine.facing("cw")
                machine.facing("cw")


        rec(obj, 4)

    def daisyRec(counter):
        if counter <= 0:
            return
        for i in edgelist:
            # test if edges are at bottom, least likely case
            string = "white"
            if i.normal("white")[1] == -1:
                bottomFaceUp(i)
            #proceed to bottom row
            if i.normal("white")[1] == 0 and i.height()[1] == -1:
                bottomRowUp(i)
            #next middle row up
            if i.normal("white")[1] == 0 and i.height()[1] == 0:
                middleRowUp(i)
            #test if edges have to be flipped
            if i.normal("white")[1] == 0 and i.height()[1] == 1:
                facing = ("x" if i.normal("white")[0] !=0 else "z") + ("Pos" if i.normal("white")[0] + i.normal("white")[2]> 0  else "Neg")
                machine = Handler(facing)
                flipEdge(machine)
            #should leave us with a clear bottom row and top row.
            checklist = []

            for w in edgelist:
                if w.normal(str("white"))[1] != 1:
                    checklist.append(0)
                pass
            if 0 not in checklist:
                return
            else:
                daisyRec(counter - 1)
                pass
    daisyRec(4)

def otherN(i):
    other = filter(lambda x : x != i.normals("white"), i.normals())[0]
    return other

def whiteCross():

    coloredEdgeList = []
    for i in edgelist:
        if i.normal("white")[1] == 1:
            coloredEdgeList.append(i)

    
    def matchingKernel(i):
        # find normal of colored face
        other = filter(lambda x : x != i.normal("white"), i.normals())[0]
        # find matching kernel by normal
        for k in kernelList:
            if k.normals()[0] == other:
                return k

    def flipDown(i):

        def rec(counter, i):
            if counter <= 0:
                return
            # grab matching kernel by normal
            match = matchingKernel(i)
            # select color on edge faces that is not white
            otherColor = filter(lambda x : x != "white", i.colors)
            # check if match
            if otherColor[0] == match.colors[0]:
                machine = Handler(facingFunction(i, otherColor[0]))
                machine.facing("cw")
                machine.facing("cw")
            else:
                machine = Handler("xPos")
                machine.top("cw")
                rec(counter - 1, i)
    
        rec(4, i)
    
    for i in coloredEdgeList:
        flipDown(i)
        pass
        
    # # # # # #  #  # # # # # # # # ## # 

def corners():
    def masterRec(counter):
        if counter <= 0:
            return        
        def bottomRowUp(i):
            def successRotate(i):
                var = "white"
                if i.normal("white")[1] == 1:
                    # this will break the position function, do something else
                    var = i.colors[0]
                if i.position(var)[0] == "left":
                    machine = Handler(i.position(var)[1])
                    machine.top("cw")
                    machine.left("cw")
                    machine.top("ccw")
                    machine.left("ccw")
                    machine.left("ccw")
                    machine.left("ccw")
                    pass
                elif i.position(var)[0] == "right":
                    machine = Handler(i.position("right"))
                    machine.top("cw")
                    machine.left("ccw")
                    machine.top("cw")
                    machine.left("cw")
                    machine.left("cw")
                    machine.left("cw")
                    return
                    pass

            def rec(counter):
                if counter <= 0:
                    return
                # find the colors of the lower not white
                neighbors = filter(lambda x : x != "white", i.colors)
                # find the vectors on the lower not up
                vec = filter(lambda x: x[1] == 0 ,i.normals())
                # find out the nighboring kernel colors
                matchingKernels = []
                matchingColors = []
                for k in kernelList:
                    if k.normals()[0] in vec and k.colors[0] in neighbors:
                        matchingKernels.append(k)
                        matchingColors.append(True)
                #correctly positioned and oriented
                if len(matchingColors) == 2 and i.normal("white")[1] == 0:
                    successRotate(i)
                else :
                    machine = Handler("xPos")
                    machine.top("cw")
                    rec(counter - 1)
                    return

            rec(4)

        def topToBottom(i):
            f = i.position("left")
            machine = Handler(f)
            machine.left("ccw")
            machine.top("cw")
            machine.left("cw")
            machine.left("cw")
            machine.left("cw")

        def downToFront(i):
            f = i.position("left")
            machine = Handler(f)
            machine.facing("cw")
            machine.top("cw")
            machine.facing("ccw")
            machine.top("ccw")
            machine.top("ccw")

        def rec(counter, i):
            if counter <= 0 or i.normal("white")[1] == -1:
                return
            # if normals are facing down, its already in place
            if i.normal("white")[1] == -1:
                return
            # if white is down facing
            if i.normal("white")[1] == 1:
                downToFront(i)
                pass
            # if white is in top layer
            if i.height()[1] == -1 and len(i.colors) == 3:
                topToBottom(i)
            #for bottomlayer 
            if i.height()[1] == 1 and len(i.colors) == 3:
                bottomRowUp(i)
            if i.normal("white")[1] != -1:
                rec(counter - 1, i)
                pass
            return
        
        for i in whiteList:
            rec(4, i)
        masterRec(counter - 1)
    masterRec(4)

def edgesToMiddle():

    def masterRec(counter) :
        if counter <= 0:
            return
        def moving(i, string, machine):
            # if "yellow" in i.colors:
            #     return
            if string == "right":
                machine.top("ccw")
                machine.right("cw")
                machine.top("cw")
                machine.right("cw")
                machine.right("cw")
                machine.right("cw")
                machine.top("cw")
                machine.facing("ccw")
                machine.top("ccw")
                machine.facing("cw")
                pass
            if string == "left":
                machine.top("cw")
                machine.left("cw")
                machine.top("ccw")
                machine.left("cw")
                machine.left("cw")
                machine.left("cw")
                machine.top("ccw")
                machine.facing("cw")
                machine.top("cw")
                machine.facing("ccw")
                pass
        
        def directional(i, color1):
            other = filter(lambda x: x != color1, i.colors)[0]
            test = []
            for k in kernelList:
                if k.colors[0] == other:
                    test.append(k)
            k = test[0]
            dir = facingFunction(i, color1)
            nX, nY, nZ = k.normals()[0]
            if "z" in dir:
                if "Pos" in dir:
                    if nX < 0:
                        return "left"
                    if nX > 0:
                        return "right"
                if "Neg" in dir:
                    if nX < 0:
                        return "right"
                    if nX > 0:
                        return "left"
            if "x" in dir:
                if "Pos" in dir:
                    if nZ < 0:
                        return "right"
                    if nZ > 0:
                        return "left"
                if "Neg" in dir:
                    if nZ < 0:
                        return "left"
                    if nZ > 0:
                        return "right"


        # recursively check if vertical bar exists: else rotate top and recurse
        def rec(k, counter):
            # print k.name(), ":"
            if counter <= 0:
                return
            passed = []
            parallel = []
            for i in edgesList:
                if k.normals()[0] in i.normals():
                    if i.height()[1] != 0:
                        # we have found vertical neighbors, now check if colors match:
                        index = i.normals().index(k.normals()[0])
                        if i.colors[index] == k.colors[0]:
                            # if colors match, append to passed
                            passed.append(i)
                    # check to see if the edges are in the wrong area
                    if i.height()[1] == 0:
                        # we have found vertical neighbors, now check if colors match:
                        index = i.normals().index(k.normals()[0])
                        if i.colors[index] != k.colors[0] and "yellow" not in i.colors:
                            # if colors match, append to parallel
                            # print i.name()
                            parallel.append(i)
            if len(passed) == 2:
                for p in passed:
                    if p.height()[1] == -1:
                        continue
                    # found successful node, now decide to move it right or left:
                    if "yellow" in p.colors:
                        continue
                    # checklist[k.name()].append(True)
                    print "passed", p.name()
                    machine = Handler(facingFunction(p, k.colors[0]))
                    moving(p, directional(p, k.colors[0]), machine)
            if len(parallel) == 1:
                p = parallel[0]
                machine = Handler(p.position("right"))
                print "moving", p.name()
                moving(p, "right", machine)
                return


            else:
                checklist = []
                for i in edgesList:
                    if "yellow" in i.colors and i.height()[1] == 1:
                        checklist.append(True)
                if len(checklist) == 4:
                    return
                else :
                    machine = Handler("xPos")
                    machine.top("cw")
                rec(k, counter - 1)
            return

        for k in kernelList:
            if k.height()[1] == -1 or k.normals()[0][1] == 1:
                continue
            rec(k, 4)
        masterRec(counter - 1)
    masterRec(4)

def yellowCross():
    def furf(i, machine):
        machine.facing("cw")
        machine.right("ccw")
        machine.top("ccw")
        machine.right("cw")
        machine.top("cw")
        machine.facing("ccw")

    upwards = []
    yellowList = []
    # check to see which yellow edges are facing up
    for i in edgesList:
        if "yellow" not in i.colors:
            continue
        yellowList.append(i)
        if i.normal("yellow")[1] == 1:
            upwards.append(i)

    if len(upwards) == 0:
        print "standing"
        current = yellowList[0]
        facing1 = facingFunction(current, "yellow")
        machine1 = Handler(facing1)
        furf(i, machine1)
        facing2 = facing1[0] + "Neg" if "Pos" in facing1 else "Neg"
        machine2 = Handler(facing2)
        furf(i, machine2)
        furf(i, machine1)
        print facing1


    

# scramble(30) 
# daisy() 
# whiteCross() 
# corners()
# edgesToMiddle()
yellowCross()








