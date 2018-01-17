#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, os

# Define variables
numberOfTeeth = 18
shaftDiameter = 0.5

def run(context):
    ui = None
    try:
        # Document setup
        app = adsk.core.Application.get()
        ui  = app.userInterface
        #rootComp = adsk.fusion.Component.cast(design.rootComponent)
        
        # Access the import manager and root component
        importManager = app.importManager
        rootComp = app.activeProduct.rootComponent
        
        # Get the file to be imported
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'squaretoothpulley.f3d')
        
        # Create the imput options and import them to the target
        importOptions = importManager.createFusionArchiveImportOptions(filename)
        importManager.importToTarget(importOptions, rootComp)
        
        # Get the occurence of the imported component
        pulleyOccurence = rootComp.occurrences.item(rootComp.occurrences.count-1)
        
        # Accessing the parts parameters
        parameters = pulleyOccurence.component.parentDesign.allParameters
        teethNumParam = parameters.itemByName('teethNum')
        shaftDiamParam = parameters.itemByName('shaftDiameter')
        teethNumParam.expression = str(numberOfTeeth)
        shaftDiamParam.expression = str(shaftDiameter) + 'cm'
        
        # get the proxy of the face of the center hole in the pulley
        pulleyComp = pulleyOccurence.component
        pulleyFace = pulleyComp.features.holeFeatures.item(0).faces.item(0)
        faceProxy = pulleyFace.createForAssemblyContext(pulleyOccurence)
        
        joints = rootComp.joints
        # prompt the user to select a shaft
        ui.messageBox('Please select a cylinder')
        selectedItem1 = ui.selectEntity("Select a cylinder", "CylindricalFaces")
        selectedBaseObj = selectedItem1.entity
        selectedFace = adsk.fusion.BRepFace.cast(selectedBaseObj)
        
        # Constrain the pulley onto the shaft
        geo1 = adsk.fusion.JointGeometry.createByNonPlanarFace(faceProxy, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
        geo2 = adsk.fusion.JointGeometry.createByNonPlanarFace(selectedFace, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
        jointInput = joints.createInput(geo1,geo2)
        jointInput.setAsRigidJointMotion()
        joint1 = joints.add(jointInput)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
