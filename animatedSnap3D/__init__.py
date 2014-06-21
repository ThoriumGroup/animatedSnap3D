from animatedSnap3D import *
import nuke
# Add menu items under the Axis Menu
try:
    m = nuke.menu('Axis').findItem('Snap')
    m.addSeparator()
    m.addCommand('Snap to (animated)', 'animatedSnap3D.snapAnimated(nuke.thisNode())')
    m.addCommand('Scale to (animated)', 'animatedSnap3D.scaleAnimated(nuke.thisNode())')
    m.addCommand('Transform to (animated)', 'animatedSnap3D.translateAnimated(nuke.thisNode())')
except:
    pass