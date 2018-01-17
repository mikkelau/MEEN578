#Author-Mikkel Unrau
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
         # Assign variables
        radius2 = 0.156 # cm?
        numTeeth = 30
        circumference = numTeeth*0.5        
        height = 1.5
        radius1 = circumference/(2*math.pi) #cm?
        radius3 = 0.5
        radius4 = radius1*1.1
        heightFlange = 0.2
        
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
        sketch1 = sketches.add(xyPlane)
        sketch2 = sketches.add(xyPlane)
        sketch3 = sketches.add(xyPlane)
        sketch4 = sketches.add(xyPlane)
        
        # Draw some circles
        circle1 = sketch1.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), radius1)
        profile1 = sketch1.profiles.item(0)
        circle2 = sketch2.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(radius1,0,0), radius2)
        profile2 = sketch2.profiles.item(0)
        circle3 = sketch3.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), radius3)
        profile3 = sketch3.profiles.item(0)
        circle4 = sketch4.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), radius4)
        profile4 = sketch4.profiles.item(0)
                      
        # Create pulleys by extruding pattern features
        extrudes = rootComp.features.extrudeFeatures #grab the extrudes collection
        # Extrude the first sketch
        # Create the input object and define all the inputs
        extrudeInput1 = extrudes.createInput(profile1, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)
        extrudeDistance = adsk.core.ValueInput.createByReal(height)
        extrudeInput1.setDistanceExtent(False, extrudeDistance)
        # Pass in the input object to create a new extrude
        extrude1 =  extrudes.add(extrudeInput1)        
        
        # Extrude the cutting sketch for the teeth
        # Create the input object and define all the inputs
        extrudeInput2 = extrudes.createInput(profile2, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput2.setDistanceExtent(False, extrudeDistance)
        # Pass in the input object to create a new extrude
        extrude2 = extrudes.add(extrudeInput2)
        # Create the pattern feature
        circularPatterns = rootComp.features.circularPatternFeatures # Get the circular patterns collection
        # Create the entity collection to pass into the input
        inputEntitiesCollection = adsk.core.ObjectCollection.create()
        inputEntitiesCollection.add(extrude2)
        inputAxis = rootComp.zConstructionAxis
        # Create the circular pattern input
        circularPatternInput = circularPatterns.createInput(inputEntitiesCollection, inputAxis)
        circularPatternInput.quantity = adsk.core.ValueInput.createByReal(numTeeth)
        circularPatternInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularPatternInput.isSymmetric = False
        # Create the ciruclar pattern
        circularPattern = circularPatterns.add(circularPatternInput)
        
        # Extrude the cutting sketch for the center hole 
        # Should the center hole go through the flange?
        extrudeInput3 = extrudes.createInput(profile3, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput3.setDistanceExtent(False, extrudeDistance)
        extrude3 = extrudes.add(extrudeInput3)
        
        # Extrude the back flange
        extrudeInput4 = extrudes.createInput(profile4, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        extrudeDistance2 = adsk.core.ValueInput.createByReal(heightFlange)
        extrudeInput4.setDistanceExtent(False, extrudeDistance2)
        extrude4 = extrudes.add(extrudeInput4)
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
