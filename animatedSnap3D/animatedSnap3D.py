import nuke
import nukescripts.snap3d

def getFrameRange():
  '''Open a dialog to request a Nuke-style frame range
  @return:  a frameRange object if a valid frame range is entered
                None if frame range is invalid or dialog is cancelled
  '''
  firstFrame = int(nuke.numvalue('root.first_frame'))
  lastFrame = int(nuke.numvalue('root.last_frame'))
  step = 1
  _range = str(nuke.FrameRange(firstFrame,lastFrame,step))
  r = nuke.getInput('Enter Frame Range:', _range)

  try:
    return nuke.FrameRange(r)
  except:
    nuke.message('Invalid frame range')
    return


def snapAnimated(node):
  
  if node is None: 
    node = nuke.thisNode() 
    if node is None: 
      return 
   
  if "translate" not in node.knobs() or "rotate" not in node.knobs(): 
    nuke.message("""Can't snap this node - it doesn't have a "translate" or "rotate" knob.""") 
    return 

  points = tuple(nukescripts.snap3d.selectedPoints())
  if len(points) < 3:
    nuke.message("You need at least 3 points for this snap function")
    return

  frames = getFrameRange()
  
  if not frames:  return
  
  
  # Add a CurveTool for the forced-evaluation hack
  temp = nuke.nodes.CurveTool()
  
  for knob in [node['translate'], node['rotate']]:
    if knob.isAnimated():
      knob.clearAnimated()
    knob.setAnimated()

  task = nuke.ProgressTask("animatedSnap3D")
  task.setMessage("Snapping %s to selected vertices" % node.name())
  
  # Loop through the framerange
  for frame in frames:
    if task.isCancelled():
      break
    
    nuke.execute(temp, frame, frame)
    nukescripts.snap3d.snapToPoints(node)
    percent = int(100*(float(frame) / (frames.frames())))
    task.setProgress(frame)
   
  # delete the temp CurveTool node
  nuke.delete(temp)
  
def scaleAnimated(node):
  
  if node is None: 
    node = nuke.thisNode() 
    if node is None: 
      return 
   
  if "scaling" not in node.knobs(): 
    nuke.message("""Can't scale this node - it doesn't have a "scaling" knob.""") 
    return 

  points = tuple(nukescripts.snap3d.selectedPoints())
  if len(points) < 2:
    nuke.message("You need at least 2 points for this snap function")
    return

  frames = getFrameRange()
  
  if not frames:  return
  
  
  # Add a CurveTool for the forced-evaluation hack
  temp = nuke.nodes.CurveTool()
  
  knob =  node['scaling']
  if knob.isAnimated():
    knob.clearAnimated()
  knob.setAnimated()

  task = nuke.ProgressTask("animatedSnap3D")
  task.setMessage("Scaling %s to selected vertices" % node.name())
  
  # Loop through the framerange
  for frame in frames:
    if task.isCancelled():
      break
    
    nuke.execute(temp, frame, frame)
    nukescripts.snap3d.scaleToPoints(node)
    percent = int(100*(float(frame) / (frames.frames())))
    task.setProgress(frame)
   
  # delete the temp CurveTool node
  nuke.delete(temp)


def translateAnimated(node):
  
  if node is None: 
    node = nuke.thisNode() 
    if node is None: 
      return 
   
  if "translate" not in node.knobs(): 
    nuke.message("""Can't translate this node - it doesn't have a "translate" knob.""") 
    return 

  points = tuple(nukescripts.snap3d.selectedPoints())
  if not points:
    nuke.message("Please select one or more vertices.")
    return

  frames = getFrameRange()
  
  if not frames:  return
  
   # Add a CurveTool for the forced-evaluation hack
  temp = nuke.nodes.CurveTool()
  
  knob =  node['translate']
  if knob.isAnimated():
    knob.clearAnimated()
  knob.setAnimated()

  task = nuke.ProgressTask("animatedSnap3D")
  task.setMessage("Translating %s to selected vertices" % node.name())
  
  # Loop through the framerange
  for frame in frames:
    if task.isCancelled():
      break
    
    nuke.execute(temp, frame, frame)
    nukescripts.snap3d.translateToPoints(node)
    percent = int(100*(float(frame) / (frames.frames())))
    task.setProgress(frame)
   
  # delete the temp CurveTool node
  nuke.delete(temp)



  