import maya.cmds as m

selection = m.ls(orderedSelection=True)

print selection

if len(selection) >=2:
    print "proceed"
    target = selection[0]
    selection.remove(target)

    for o in selection:
        print o
        m.aimConstraint(target, o, aim=[0, 1, 0])

else:
    print "err"