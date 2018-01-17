#Author-Mikkel Unrau
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
         # Assign variables
        radius1 = 2
        radius2 = 0.156
        numTeeth = 10
        height = 8
        
        # Document setup
        app = adsk.core.Application.get()
        design = app.activeProduct
        #rootComp = design.rootComponent
        rootComp = adsk.fusion.Component.cast(design.rootComponent)
        
        # Use the application to get the user interface
        ui  = app.userInterface
       
        
        # Create Sketches
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        sketch2 = sketches.add(xyPlane)
        
        # Draw some circles
        circle1 = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), radius1)
        circle2 = sketch2.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(radius1,0,0), radius2)
        
        # Extrude two cylinders
        #extrudes = rootComp.features.extrudeFeatures
        
        # Ask for them to select two cylinders to get belt length 
        ui.messageBox('Select two cylindrical faces')
        selectedItem1 = ui.selectEntity("Select a cylinder", "CylindricalFaces")
        selectedItem1Value = selectedItem1.point
        selectedItem2 = ui.selectEntity("Select another cylinder", "CylindricalFaces")
        selectedItem2Value = selectedItem2.point
        lengthBetweenPoints = selectedItem1Value.distanceTo(selectedItem2Value)
        
                
        
        # Create pulleys by extruding pattern features
        cutExtrudes = rootComp.features.extrudeFeatures
        # Create the input object and define all the inputs
        extrudeInput2 = cutExtrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeDistance = adsk.core.ValueInput.createByReal(height)
        extrudeInput2.setDistanceExtent(False, extrudeDistance)
        extrude        
        
        circularPatterns = rootComp.features.circularPatternFeatures # Get the circular patterns collection
        # Create the entity collection to pass into the input
        inputEntitiesCollection = adsk.core.ObjectCollection.create()
        inputEntitiesCollection.add(extrude)
        inputAxis = rootComp.zConstructionAxis
        # Create the circular pattern input
        circularPatternInput = circularPatterns.createInput(inputEntitiesCollection, inputAxis)
        circularPatternInput.quantity = adsk.core.ValueInput.createByReal(numTeeth)
        circularPatternInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularPatternInput.isSymmetric = False
                


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
