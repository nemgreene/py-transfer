import maya.cmds as m
import math
import time 
import timeit

# start = timeit.default_timer()


# stop = timeit.default_timer()
# print('Time: ', stop - start)

# vA=[3, 1, 1]
# vB=[1, 4, 2]
# vC=[1, 3, 4]

# lA = [0, 2, 2]
# lB = [6, 5, 4]

def vector(o, d):
    return[d[0] - o[0], d[1] - o[1], d[2] - o[2]]

def intersection(vA, vB, vC, lA, lB):
    #plane
    #7x+4y+2z=27
    aB = vector(vA, vB)
    aC = vector(vA, vC)
    N = (aB[1]*aC[2] - aB[2]*aC[1], aB[2]*aC[0] - aB[0]*aC[2], aB[0]*aC[1] - aB[1]*aC[0])
    poly = list(N)
    poly.append((N[0]*vC[0] + N[1]*vC[1] + N[2]*vC[2]))
    
    #line
    #x=6+6t
    #y=5+3t
    #z=4+2t

    dV = vector(lA, lB)
    pX, pY, pZ = [lB[0], dV[0]], [lB[1], dV[1]], [lB[2], dV[2]]
    print pX, pY, pZ
    print poly
    insert = poly[3] - (pX[0] * poly[0] + pY[0] * poly[1] + pZ[0] * poly[2])
    tTotal = pX[1] * poly[0] + pY[1] * poly[1] + pZ[1] * poly[2]
    t = insert / float(tTotal)

    ret = [pX[0] + pX[1] * t, pY[0] + pY[1] * t, pZ[0] + pZ[1] * t]
    print ret
    m.spaceLocator(p = ret)

# intersection(vA, vB, vC, lA, lB)
# vertices = m.ls('* .vtx[*]', fl=1)
# origin = [0, 0, 0]
# passing = []
# for i in vertices:
#     x, y, z = m.xform(i, ws=1, q=1, t=1)
#     if ( 
#         -3< x < 3 and -1.3< y < 1.3 and -3< z < 3
#     ):
#         passing.append(i)
# print len(passing)
# m.select(passing)


# matrix = m.xform(face[0], ws=1, q=1, t=1)


def calc():

    point0 = m.ls("p0")
    point1 = m.ls("p1")
    sphere = m.ls("test")

    c = m.xform(sphere, ws=1, q=1, t=1)
    p0 = m.xform(point0, ws=1, q=1, t=1)
    p1 = m.xform(point1, ws=1, q=1, t=1)
    r = m.getAttr(str(sphere[0])+  ".scaleX")
    # p0 = [1, 1, -1]
    # p1 = [3, 2, 8]
    # r = 2

    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    dz = p1[2] - p0[2]

    a1 = dx * dx + dy * dy + dz * dz
    b1 = 2 *dx * (p0[0] - c[0]) + 2*dy * (p0[1] - c[1]) + 2 *dz * (p0[2] - c[2])
    c1 = c[0]*c[0] + c[1]*c[1] + c[2]*c[2] + p0[0]*p0[0] + p0[1]*p0[1] + p0[2]*p0[2] + (-2 * (c[0]*p0[0] + c[1]*p0[1] + c[2]*p0[2])) - r * r
    disc = (b1 * b1 - 4 * a1 * c1)

    if(disc  > 0 ):
        print ("intersection")
        pointer = m.ls("pointer")
    elif(disc == 0):
        print("tangent")
        return
    else:
        print "no intersesction"
        return


    t = (-1 * b1 - math.sqrt( b1 * b1 - 4 * a1 * c1)) / (2 * a1)

    xf = p0[0] + (t * dx)
    yf = p0[1] + (t * dy)
    zf = p0[2] + (t * dz)

    print [xf, yf, zf]

    m.move( xf, yf, zf, pointer)

# calc()

def biasedRays() :
    print "biased rays"
    loc = m.ls("locator1")
    for i in range(44):
        local = m.instance(loc)
        m.move(2 * math.cos(i) + 5, 0, 2 * math.sin(i) +5, local)

biasedRays()