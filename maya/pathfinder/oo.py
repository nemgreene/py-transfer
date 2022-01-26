import maya.cmds as m
import math
import time 
import timeit

global blacklist
global start 
global finish

start = [14, 0, -14]
end = [-14, 0, 14]

blacklist = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 255, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
grey = (128, 128, 128)
turquoise = (64, 224, 208)

def parseToVal(str):
    ret = []
    spl = str.split("_")
    spl.pop(0)

    for i in spl:
        rep = i.replace("n", "-")
        rep = rep.replace("p", "+")
        ret.append(rep)

    return map(lambda x: int(x), ret )
def parseToStr(arr):
    ret = []
    for i in arr:
        if i < 0:
            rep = str(i).replace("-", "_n")
        else:
            rep = "_p"+ str(i)
        if i == 0:
            # rep.replact()
            rep = "_n0"
        ret.append(rep)

    return "".join(ret)

# spotNode = m.polyPlane(n="spot" , sx=1, sy=1)
class Spot:
    prev = 0
    def __init__(self,x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.gDist = 0
        # self.nodeArr = m.instance(spotNode, n= self.name())
        self.nodeArr = m.polyPlane(n= self.name(), sx=1, sy=1)
        self.color = white

        self.change_color(white)
        m.move(self.x, self.y, self.z, self.nodeArr[0])
        

    
    def name(self):
        return parseToStr([self.x, self.y, self.z])
    def change_color(self, color):
        self.color = color
        m.setAttr(str(self.name()) + ".overrideEnabled",1)
        m.setAttr(str(self.name()) + ".overrideRGBColors",1)
        m.setAttr(str(self.name()) + ".overrideColorR", color[0])
        m.setAttr(str(self.name()) + ".overrideColorG", color[1])
        m.setAttr(str(self.name()) + ".overrideColorB", color[2])
    def coord(self):
        return [self.x, self.y, self.z]
    def neighbors(self, current):
        current = current[0] if type(current) == list else current
        x, y, z = self.x, self.y, self.z
        corners = []
        straights = []
        def quadrant(curr):
            ret = []
            # for xAdd in range(3):
            #     for yAdd in range(3):
            #         for zAdd in range(3):
            #             add = [x+xAdd-1, y+yAdd-1, z+zAdd-1]
            #             ret.append(add)
            for xAdd in range(3):
                for yAdd in range(3):
                    # for zAdd in range(3):
                    add = [x+xAdd-1, 0, z+yAdd-1]
                    ret.append(add)
            return ret
        def cornerBlockade(home, corner):
            hX, hY, hZ = home
            cX, cY, cZ = corner
            diff = [hX-cX, hY-cY, hZ-cZ]
            #handle far corner 

            #

            if 0 not in diff:
                # print "diagonal", home, corner, diff
                # print [hX - diff[0], hY , hZ],  [hX, hY - diff[1], hZ],   [hX, hY, hZ - diff[2]]
                xB, yB, zB = [hX - diff[0], hY , hZ], [hX, hY - diff[1], hZ], [hX, hY, hZ - diff[2]]
                
                if (xB not in blacklist or yB not in blacklist or zB not in blacklist):
                    test = ((1 if [corner[0]+diff[0], corner[1], corner[2]] in blacklist else 0) + 
                            (1 if [corner[0], corner[1]+diff[1], corner[2]] in blacklist else 0) + 
                            (1 if [corner[0], corner[1], corner[2]+diff[2]] in blacklist else 0) )
                    if test == 2:
                        return True
                    if ((xB in blacklist and yB in blacklist) or (yB in blacklist and zB in blacklist) or (yB in blacklist and zB in blacklist)):
                        return True
                    return False
                return True
            ret = [[hX-diff[0], hY, hZ], [hX, hY-diff[1], hZ], [hX, hY, hZ-diff[2]]]
            ret.remove(home)
            if (ret[0] in blacklist) and (ret[1] in blacklist):
                return True
            else:
                return False
        def cornerCut(arr):
            if (x == arr[0] and y == arr[1]) or (x == arr[0] and z == arr[2]) or (y == arr[1] and z == arr[2]):
                straights.append(arr) 
            else:
                corners.append(arr)
        ret = quadrant([x, y, z])
        map(cornerCut, ret)
        for i in corners:
            if cornerBlockade(current.coord(), i):
                ret.remove(i)

        ret = filter(lambda x : start[0] + 1 not in x and x not in blacklist, ret)
        def new(x):
            if x in blacklist:
                return "x"
            else:
                blacklist.append(x)
                mapSpot = Spot(x[0], x[1], x[2])
                mapSpot.prev = self
                return[mapSpot, mapSpot.fDist()]
        ret = map(lambda x: new(x), ret)
        # ret = filter(lambda x : type(x) != str and x[0].coord() not in blacklist, ret)
        ret = filter(lambda x : type(x) != str, ret)
        for i in ret:
            i[0].gDist = self.gDist + 1
        return ret
    def hDist(self):
        # dx = m.getAttr("end.translateX")
        # dy = m.getAttr("end.translateY")
        # dz = m.getAttr("end.translateZ")
        dx = end[0] 
        dy = end[1]
        dz = end[2]
        # vx = m.getAttr(str(node[0])+".translateX")
        # vy = m.getAttr(str(node[0])+".translateY")
        # vz = m.getAttr(str(node[0])+".translateZ")
        vx = self.x
        vy = self.y
        vz = self.z
        c = math.sqrt(((dx-vx)**2)+((dy-vy)**2)+((dz-vz)**2))
        return c
    def fDist(self) :
        return self.hDist() + self.gDist

def lowest(arr):
    print len(arr)
    return(sorted(arr, key = lambda x: x[1])[0])

def pathify(obj):
    current = obj[0]
    pathLength = current.gDist
    vertexArr = []
    while pathLength > 0:
        vertexArr.append(current.coord())
        current = current.prev
        pathLength = pathLength - 1
    vertexArr.append(start)
    path = m.curve(p=vertexArr)

def blacklistIt():
    m.select("blacklist", hi=1)
    m.select("blacklist", d=1)
    selectionGroup = m.ls(sl=True)
    selectionGroup = filter(lambda x : "Shape" not in x, selectionGroup)
    m.select(cl=1)
    for i in selectionGroup:
        x, y, z = m.getAttr(i + ".translate")[0]
        x, y, z, = int(x), int(y), int(z)
        blacklist.append([x, y, z])
def solve():

    new = Spot(start[0], start[1], start[2])
    open =  new.neighbors(new)
    current = lowest(open)
    current[0].change_color(purple)

    running = 300
    while running > 0:
        if current[0].coord() == end:
            current[0].change_color(red)
            running = 0
            pathify(current)
            print "finished"
            ls = m.ls("_*_*")
            m.group(ls, n="field")
            m.delete("field")
            return

        # time.sleep(.01)
        m.refresh()

        blacklist.append(current[0].coord())
        open = filter(lambda x : x[0].coord() != current[0].coord(), open)
        current[0].change_color(red)
        open = open + current[0].neighbors(current)
        current = lowest(open)
        running = running -1
def cleanup() :
    ls = m.ls("field")
    m.delete(ls)
    ls = m.ls("curve*")
    m.delete(ls)


start = timeit.default_timer()


def cubify(h, x, y, z):
    # group = m.group(em=1, n="blacklist")
    test = m.polySphere(r=h,sa=h*7, sh=h*4, n="planet")
    m.move(x, y, z, test)
    vtxList = m.ls(test[0]+'.vtx[*]', fl=True)
    init = m.polyCube(n="init")
    # m.hide(test)
    for i in vtxList:
        x, y, z = m.xform(i, q=True, ws=True, t=True)
        coord = [int(x-.2) if x > 0 else int(x+.2),int(y-.2) if y > 0 else int(y+.2), int(z-.2) if z > 0 else int(z+.2)]
        if coord not in blacklist:
            local = m.instance(init)
            m.move(coord[0], coord[1], coord[2], local)
            # m.parent(local, group)
            blacklist.append(coord)
            # m.refresh()
    # m.move(0, -2,0, vtx, r=1)



# cleanup()
# cubify(2, -11, 0, 0)
# cubify(6, 0, 0, 0)
cubify(10, 0, 0, 0)

stop = timeit.default_timer()
print('Time: ', stop - start)

# blacklistIt()
# test = Spot(9, -1, -4)
# test.neighbors(test)
# solve()
