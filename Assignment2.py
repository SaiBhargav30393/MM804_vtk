

import vtk

# 1. Read CT dataset.
rdr = vtk.vtkDICOMImageReader()
rdr.SetDirectoryName("img1")
rdr.Update()
print("CT Data Loaded.")
# ---------------------------------------------------------

# 2. Creating a colour transfer function.
cT = vtk.vtkColorTransferFunction()
cT.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
cT.AddRGBPoint(-77, 0.5, 0.2, 0.1)
cT.AddRGBPoint(94, 0.9, 0.6, 0.3)
cT.AddRGBPoint(179, 1.0, 0.9, 0.9)
cT.AddRGBPoint(260, 0.6, 0.0, 0.0)
cT.AddRGBPoint(3071, 0.8, 0.7, 1.0)
print("Colour transfer function")
# ---------------------------------------------------------

# 3. Make an opacity transfer function with the values below.
oT = vtk.vtkPiecewiseFunction()
oT.AddPoint(-3024, 0.0)
oT.AddPoint(-77, 0.0)
oT.AddPoint(180, 0.2)
oT.AddPoint(260, 0.4)
oT.AddPoint(3071, 0.8)
print("Opacity transfer function")
# ---------------------------------------------------------

# 4. Render the CT dataset using the viewports indicated below.
# In viewport 1, we're using the direct volume rendering approach.
ctM = vtk.vtkSmartVolumeMapper()
ctM.SetInputConnection(rdr.GetOutputPort())

# Combine the opacity and colour transfer functions from the previous section.
ctP = vtk.vtkVolumeProperty()
ctP.SetScalarOpacity(oT)
ctP.SetColor(cT)
ctP.ShadeOn()

# Define the role of a volume actor.
ctV = vtk.vtkVolume()
vR = vtk.vtkRenderer()

# Set the attributes of the volume actor
ctV.SetMapper(ctM)
ctV.SetProperty(ctP)

vR.AddVolume(ctV)
print("Volume rendering.")

# ---------------------------------------------------------
# 5. Show the iso-surface derived at intensity in viewport 2. 
# The marching cubes algorithm yielded a result of 300.

iso = vtk.vtkMarchingCubes()
iso.SetInputConnection(rdr.GetOutputPort())
iso.ComputeGradientsOn()
iso.ComputeScalarsOff()
iso.SetValue(0, 300)

# For the iso-surface, there is a polydata mapper.
isoM = vtk.vtkPolyDataMapper()
isoM.SetInputConnection(iso.GetOutputPort())
isoM.ScalarVisibilityOff()

# For the iso surface, there is an actor.
isoA = vtk.vtkActor()
isoA.SetMapper(isoM)
isoA.GetProperty().SetColor(1.,1.,1.)

## renderer and render window
iR = vtk.vtkRenderer()
## add the actors 
iR.AddActor(isoA)
print("ISO surface.")
# ---------------------------------------------------------

# 6. Create a combo rederer
cR = vtk.vtkRenderer()

# Use the same actor and Volume.
cR.AddActor(isoA)
cR.AddVolume(ctV)
# ---------------------------------------------------------

print("Creating render window")
# Create three viewports in a render window.
xmin=[0,0.33,0.66]
xmax=[0.33,0.66,1]
ymin=[0,0,0]
ymax=[1,1,1]

mW = vtk.vtkRenderWindow()
wI = vtk.vtkRenderWindowInteractor()
mW.SetSize(1300,600)
wI.SetRenderWindow(mW)

# SetActiveCameras to the first renderer's ActiveCamera.
# This allows the visualisation to be displayed in all three viewports from the same angle.
iR.SetActiveCamera(vR.GetActiveCamera());
cR.SetActiveCamera(iR.GetActiveCamera());
vR.ResetCamera()

# The renderes should be added to the main window.
mW.AddRenderer(vR)
mW.AddRenderer(iR)
mW.AddRenderer(cR)

# Set the location
vR.SetViewport(xmin[0],ymin[0],xmax[0],ymax[0])
iR.SetViewport(xmin[1],ymin[1],xmax[1],ymax[1])
cR.SetViewport(xmin[2],ymin[2],xmax[2],ymax[2])

mW.Render()

w2I = vtk.vtkWindowToImageFilter()
w2I.SetInput(mW)
w2I.Update()

# Save the output
wr = vtk.vtkJPEGWriter()
wr.SetInputConnection(w2I.GetOutputPort())
wr.SetFileName('sai.jpg')
wr.Write()


wI.Initialize()
wI.Start()













