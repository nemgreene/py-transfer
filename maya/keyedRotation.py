import maya.cmds as m


filtered = m.ls(selection=True, type="transform")


if len(filtered) >=1:
    start = cmds.playbackOptions (query=True, minTime=True)
    end = cmds.playbackOptions (query=True, maxTime=True)
    print start, end

    for i in filtered:
        m.cutKey(i, time=(start, end), attribute='rotateY')
        m.setKeyframe(i, time=start, attribute="rotateY", value=0)
        m.setKeyframe(i, time=end, attribute="rotateY", value=360)
        m.selectKey(i, time=(start, end), at="rotateY")
        m.keyTangent(itt="linear", ott="linear")
    

else:
    print("err")