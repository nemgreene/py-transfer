import maya.cmds as m
import math

global start
global finish

start = [12, 0, 12]
end = [-12, 0, -12]

white = (255, 255, 255)
black = (0, 0, 0)


def line(s, e, color):
    diff = [e[0]-s[0], e[1]-s[1], e[2]-s[2]]
    len = diff[0] + diff[1] + diff[2]
    mult = -1 if (diff[0] < 0 or diff[1] < 0 or diff[2] < 0) else 1
    for i in range(abs(len) + 1):
        x = s[0] + (i * mult if diff[0] != 0 else 0)
        y = s[1] + (i * mult if diff[1] != 0 else 0)
        z = s[2] + (i * mult if diff[2] != 0 else 0)
        print [x, y, z]
        if ([x, y, z] != start and [x, y, z] != end):
            inst = m.polyCube(n="mazeWall*")
            m.setAttr(str(inst[0]) + ".overrideEnabled",1)
            m.setAttr(str(inst[0]) + ".overrideRGBColors",1)
            m.setAttr(str(inst[0]) + ".overrideColorR", color[0])
            m.setAttr(str(inst[0]) + ".overrideColorG", color[1])
            m.setAttr(str(inst[0]) + ".overrideColorB", color[2])
            m.move(x, y, z, inst)

def init(s, e):
    line([s[0] + 1, 0, s[2] + 1], [e[0] - 1, 0, s[2] + 1], black)
    line([s[0] + 1, 0, s[2] + 1], [s[0] + 1, 0, e[2] - 1], black)
    line([e[0] - 1, 0, e[2] - 1], [e[0] - 1, 0, s[2] + 1], black)
    line([e[0] - 1, 0, e[2] - 1], [s[0] + 1, 0, e[2] - 1], black)

def pathfiy(s, e):
    print s, e


init(start, end)
pathfiy(start, end)
