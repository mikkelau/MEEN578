#Author-Mikkel Unrau
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        # define constants
        radius1 = 3
        radius2 = 4        
        
        # Document setup
        app = adsk.core.Application.get()
        design = app.activeProduct
        #rootComp = design.rootComponent
        rootComp = adsk.fusion.Component.cast(design.rootComponent)
        
        # Use the application to get the user interface
        ui  = app.userInterface
        
        # Ask for them to select two cylinders to get belt length 
        ui.messageBox('Select two cylindrical faces')
        selectedItem1 = ui.selectEntity("Select a cylinder", "CylindricalFaces")
        selectedItem1Value = selectedItem1.point
        selectedItem2 = ui.selectEntity("Select another cylinder", "CylindricalFaces")
        selectedItem2Value = selectedItem2.point
        lengthBetweenPoints = selectedItem1Value.distanceTo(selectedItem2Value)
        
        #Calculate and display Belth length
        beta = 2*math.acos(((radius2-radius1)/lengthBetweenPoints)
        beltLength = 2*lengthBetweenPoints*math.sin(beta/2)+(math.pi)*(radius1+radius2)+(math.pi/180)*(90-beta/2)*2*(radius2-radius1) #convert to radians?
        unitsMgr = design.unitsManager        
        displayBeltLength = unitsMgr.formatInternalValue(beltLength, unitsMgr.defaultLengthUnits, True)
        ui.messageBox('The needed belt length is: ' + displayBeltLength)
                


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
