#Author-Mikkel Unrau
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        # Assign variables
        radius1 = 2
        radius2 = 0.156
        
        # Document setup
        app = adsk.core.Application.get()
        design = app.activeProduct
        rootComp = design.rootComponent
        
        # Use the application to get the user interface
        ui  = app.userInterface
        #ui.messageBox('Hello script')
        
        # Create Sketches
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        sketch2 = sketches.add(xyPlane)
        
        # Draw some circles
        circle1 = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), radius1)
        circle2 = sketch2.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(radius1,0,0), radius2)
        #extrudes = rootComp.features.extrudeFeatures

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
