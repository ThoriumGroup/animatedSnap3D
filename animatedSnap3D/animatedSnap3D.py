#!/usr/bin/env python
"""

Animated Snap 3D
================

This submodule contains the functions needed to executed an animated snap.

## Public Functions

    run()
        Adds the animatedSnap3D functions to the Axis Snap Menu

## License

The MIT License (MIT)

animatedSnap3D
Copyright (c) 2011 Ivan Busquets

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# ==============================================================================
# IMPORTS
# ==============================================================================

# Nuke Imports
import nuke
import nuke.geo
import nukescripts
from nukescripts import snap3d as s3d

# ==============================================================================
# EXPORTS
# ==============================================================================

__all__ = []

# ==============================================================================
# PUBLIC FUNCTIONS
# ==============================================================================


def get_frange():
    """Open a dialog to request a Nuke-style frame range

    Args:
        N/A

    Returns:
        <nuke.FrameRange>
            Returns a FrameRange object if valid frange is entered, or none.

    Raises:
        N/A

    """

    first_frame = int(nuke.numvalue('root.first_frame'))
    last_frame = int(nuke.numvalue('root.last_frame'))
    step = 1
    default_frange = str(nuke.FrameRange(first_frame, last_frame, step))
    frange = nuke.getInput('Enter Frame Range:', default_frange)

    if not frange:
        return None
    else:
        try:
            return nuke.FrameRange(frange)
        except:  # TODO: Determine exact exception
            nuke.message('Invalid frame range')
            return None

# Lazy functions to determine the vertex selection
# and call animatedSnapFunc with the right arguments

def translateThisNodeToPointsAnimated(node=None):
    if not node:
        node = nuke.thisNode()

    return animatedSnapFunc(node, s3d.getSelection(), \
                          ["translate"],\
                          snapFunc = s3d.translateToPointsVerified)

def translateRotateThisNodeToPointsAnimated(node=None):
    if not node:
        node = nuke.thisNode()

    return animatedSnapFunc(node, s3d.getSelection(), \
                          ["translate", "rotate"],\
                          snapFunc = s3d.translateRotateToPointsVerified)

def translateRotateScaleThisNodeToPointsAnimated(node):
    if not node:
        node = nuke.thisNode()

    return animatedSnapFunc(node, s3d.getSelection(),\
                          ["translate", "rotate", "scaling"],\
                          snapFunc = s3d.translateRotateScaleToPointsVerified)


# Main wrapper function
def animatedSnapFunc(nodeToSnap, vertexSelection, knobsToAnimate, snapFunc = s3d.translateToPointsVerified):
  '''A wrapper to call the relevant snap functions within a framerange loop'''

    knobsToVerify = list(knobsToAnimate)
    minVertices = 1
    if 'translate' in knobsToVerify:
        knobsToVerify.append('xform_order')
    if 'rotate' in knobsToVerify:
        knobsToVerify.append("rot_order")
    if 'scaling' in knobsToVerify:
        minVertices = 3

    temp = None
    try:
        s3d.verifyNodeToSnap(nodeToSnap, knobsToVerify)

        # verify vertex selection once before the loop
        s3d.verifyVertexSelection(vertexSelection, minVertices)

        # now ask for a framerange
        frames = get_frange()

        if not frames:    return    # Exit eary if cancelled or empty framerange

        # Add a CurveTool for the forced-evaluation hack
        temp = nuke.nodes.CurveTool()

        # Set the anim flag on knobs
        for knob in [nodeToSnap[x] for x in knobsToAnimate]:
            # reset animated status
            if knob.isAnimated():
                knob.clearAnimated()
            knob.setAnimated()

        # Set up Progress Task
        task = nuke.ProgressTask("animatedSnap3D")
        task.setMessage("Matching position of %s to selected vertices" % nodeToSnap.name())

        # Loop through the framerange
        for frame in frames:
            if task.isCancelled():
                break

            # Execute the CurveTool node to force evaluation of the tree
            nuke.execute(temp, frame, frame)

            # this is repetitive, but the vertex selection needs to be computed again
            # in order to get the vertices at the right context (time)
            vertexSelection = s3d.getSelection()

            # this is also repetitive. Selection should be already verified
            # but checking again in case topology has changed between frames
            s3d.verifyVertexSelection(vertexSelection, minVertices)

            # Call the passed snap function from the nukescripts.snap3d module
            snapFunc(nodeToSnap, vertexSelection)

    except ValueError, e:
        nuke.message(str(e))

    finally:    # delete temp CurveTool node
        if temp:
            nuke.delete(temp)




