import hou
def bakeIt():
    baking_node = hou.node("/obj/geo1/maps_baker1")
    if baking_node:
        baking_node.cook()
        print("cooked")
    else:
        print("error")
pass

ColorDict = {"Blond" : {"r":0.98,"g":0.94,"b":0.74}, "Black" : {"r":0,"g":0.01,"b":0}, "Brown" : {"r":0.59,"g":0.29,"b":0}, "Red" : {"r":0.9,"g":0.2,"b":0}}

#print(ColorDict["Red"]["r"])

text = "Blond"
rough = True
color_node = hou.node("/obj/geo1/color1")
if color_node:
    color_params = color_node.parms()
    rcolor = color_node.parm("colorr")
    gcolor = color_node.parm("colorg")
    bcolor = color_node.parm("colorb")
    print (rcolor.eval())
    for parm in color_params:
        parm_template = parm.parmTemplate()
        print(f"Parameter name: {parm.name()}, Type: {parm_template.type().name()}, Current value: {parm.eval()}")
        
def colorSet():
    if text == "Blond":
        Bred = ColorDict["Blond"]["r"]
        Bgreen = ColorDict["Blond"]["g"]
        Bblue = ColorDict["Blond"]["b"]
    elif text == "Black":
        Bred = ColorDict["Black"]["r"]
        Bgreen = ColorDict["Black"]["g"]
        Bblue = ColorDict["Black"]["b"]
    elif text == "Red":
        Bred = ColorDict["Red"]["r"]
        Bgreen = ColorDict["Red"]["g"]
        Bblue = ColorDict["Red"]["b"]
    elif text == "Brown":
        Bred = ColorDict["Brown"]["r"]
        Bgreen = ColorDict["Brown"]["g"]
        Bblue = ColorDict["Brown"]["b"]
        
    rcolor.set(Bred)
    gcolor.set(Bgreen)
    bcolor.set(Bblue)
       
pass

def setRoughness():
    control_node = hou.node("/obj/geo1/Control")
    control_param = control_node.parm("roughcontrol")
    if rough == True:
        control_param.set(True)
    else :
        control_param.set(False)
        pass
pass  

colorSet()
setRoughness()
bakeIt()