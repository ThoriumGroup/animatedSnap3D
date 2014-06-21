from animatedSnap3D import *
import nuke
# Add menu items under the Axis Menu
try:
    m = nuke.menu('Axis').findItem('Snap')
    m.addSeparator()
    m.addCommand('Match position - ANIMATED', 'animatedSnap3D.translateThisNodeToPointsAnimated()')
    m.addCommand('Match position, orientation - ANIMATED', 'animatedSnap3D.translateRotateThisNodeToPointsAnimated()')
    m.addCommand('Match position, orientation, scale - ANIMATED', 'animatedSnap3D.translateRotateScaleThisNodeToPointsAnimated()')
except:
    pass