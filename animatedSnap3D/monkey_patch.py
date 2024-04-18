"""
In Nuke 14.0, the new 3D system was introduced, breaking snap3d.
This is a monkey patch to fix the issue. In Nuke 15.1, foundry is working on fixing the issue.
This patch will only get applied to Nuke 14.0, 14.1 and 15.0.
Even though the patch fixed python errors and makes the script work with the new 3D system,
the new 3D system is still unreliable and will often fail to generate all frames and ignore some transforms.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import nuke
import _nukemath
import nukescripts.snap3d


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'patch_snap3d'
]


# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================
ORIGINAL_SELECTED_VERTEX_INFOS = nukescripts.snap3d.selectedVertexInfos


def patch_snap3d():
    """ Monkey patch for nukescripts.snap3d.selectedVertexInfos """
    if nuke.NUKE_VERSION_MAJOR == 14 or (nuke.NUKE_VERSION_MAJOR == 15 and nuke.NUKE_VERSION_MINOR == 0):
        nukescripts.snap3d.selectedVertexInfos = selectedVertexInfos


def unpatch_snap3d():
    """ Unpatch nukescripts.snap3d.selectedVertexInfos """
    nukescripts.snap3d.selectedVertexInfos = ORIGINAL_SELECTED_VERTEX_INFOS


# =============================================================================
# Patched Functions
# =============================================================================

def selectedVertexInfos(selectionThreshold=0.5):
    """
    selectedVertexInfos(selectionThreshold) -> iterator

    Return an iterator which yields a tuple of the index and position of each
    point currently selected in the Viewer in turn.

    The selectionThreshold parameter is used when working with a soft selection.
    Only points with a selection level >= the selection threshold will be
    returned by this function.
    """
    if not nuke.activeViewer():
        return

    # New 3D system
    try:
        stage = nuke.activeViewer().node().getStage()
    except ValueError:
        stage = None
    if stage:
        sel = nuke.getGeoSelection()
        for o, s in enumerate(sel):
            vertexWeights = s.getVertexWeights()
            points = s.getWorldPoints(stage)
            normals = s.getWorldNormals(stage)
            if len(vertexWeights) == len(points) and len(vertexWeights) == len(normals):
                points = [_nukemath.Vector3(p.x, p.y, p.z) for p in points]
                normals = [_nukemath.Vector3(p.x, p.y, p.z) for p in normals]
                for p in range(len(vertexWeights)):
                    value = vertexWeights[p]
                    if value >= selectionThreshold:
                        yield nukescripts.snap3d.VertexInfo(o, p, value, points[p], normals[p])
            break

    # Old 3D system
    for n in nukescripts.snap3d.allNodesWithGeoSelectKnob():
        geoSelectKnob = n['geo_select']
        sel = geoSelectKnob.getSelection()
        objs = geoSelectKnob.getGeometry()
        if objs:
            for o in range(len(sel)):
                objSelection = sel[o]
                objPoints = objs[o].points()
                objTransform = objs[o].transform()
                invTransform = objTransform.inverse()
                objNormals = objs[o].normals()
                if objNormals is None or len(objNormals) == 0:
                    objNormals = objs[o].constructNormals()
                for p in range(len(objSelection)):
                    value = objSelection[p]
                    if value >= selectionThreshold:
                        pos = objPoints[p]
                        tPos = objTransform * _nukemath.Vector4(pos.x, pos.y, pos.z, 1.0)
                        normal = objNormals[p] if (
                                    objNormals is not None and p < len(objNormals)) else _nukemath.Vector3(0, 0, 0)
                        tNormal = invTransform.ntransform(normal)
                        yield nukescripts.snap3d.VertexInfo(o, p, value, _nukemath.Vector3(tPos.x, tPos.y, tPos.z), tNormal)
