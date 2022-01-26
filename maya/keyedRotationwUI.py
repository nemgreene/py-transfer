import maya.cmds as m
import functools

def createUI(pWindowTitle, pCallback):
    windowId = "myWindowId"
    if m.window(windowId, exists=True):
        m.deleteUI(windowId)
    m.window(windowId,  title= pWindowTitle, sizeable= False, rtf=True)
    m.rowColumnLayout( nc=3, cw=[(1, 75), (2, 60), (3, 60)], co=[(1, "right", 3)])

    m.text(label="Time Range:")
    startTimeField = m.intField(value = m.playbackOptions(q=True, minTime=True))
    endTimeField = m.intField(value = m.playbackOptions(q=True, maxTime=True))

    m.text(label="Attribute:")
    textAttributeField = m.textField(text="rotateY")
    m.separator(h=10, style= "none")

    m.separator(h=10, style= "none")
    m.separator(h=10, style= "none")
    m.separator(h=10, style= "none")

    m.separator(h=10, style= "none")
    m.button(label="Apply", command=functools.partial(pCallback,
             startTimeField, endTimeField, textAttributeField))

    def cancelCallback(*pArgs):
        if m.window(windowId, exists=True):
            m.deleteUI(windowId)

    m.button(label="Cancel", command=cancelCallback)

    m.showWindow()

def applyCallback( startTimeField, endTimeField,
 textAttributeField, *pArgs):
    print("apply button pressed")
    startTime = m.intField(startTimeField, query=True, value=True)
    endTime = m.intField(endTimeField, query=True, value=True)
    targetAttribut0e = m.textField(textAttributeField, query=True, text=True)

    # Logic here

createUI("title", applyCallback)


