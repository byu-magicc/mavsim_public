"""
mavsim_python: drawing tools
    - Beard & McLain, PUP, 2012
    - Update history:
        3/30/2022 - RWB
"""
import numpy as np
from numpy import cos, sin
from numpy.linalg import norm
import pyqtgraph.opengl as gl
import tools.rotations
import parameters.camera_parameters as CAM


class DrawFov:
    def __init__(self, state, window):
        """
        Draw the camera field of view
        """
        #self.mygrey1 = np.array([0.8, 0.8, 0.8, 1])  # light
        self.mygrey1 = np.array([0, 0, 0, 1])  # light
        self.mygrey2 = np.array([0.6, 0.6, 0.6, 1])
        self.mygrey3 = np.array([0.5, 0.5, 0.5, 1])
        self.mygrey4 = np.array([0.3, 0.3, 0.3, 1])  # dark
        # get points that define the non-rotated, non-translated mav and the mesh colors
        self.fov_points, self.fov_meshColors = self.getPoints()
        mesh = self.getTransformedMesh(state)
        self.fov = gl.GLMeshItem(vertexes=mesh,  # defines the triangular mesh (Nx3x3)
                                 vertexColors=self.fov_meshColors,  # defines mesh colors (Nx1)
                                 drawEdges=True,  # draw edges between mesh elements
                                 smooth=False,  # speeds up rendering
                                 computeNormals=False)  # speeds up rendering
        self.fov.setGLOptions('translucent')
        self.fov.setGLOptions('additive')
        # ============= options include
        # opaque        Enables depth testing and disables blending
        # translucent   Enables depth testing and blending
        #               Elements must be drawn sorted back-to-front for
        #               translucency to work correctly.
        # additive      Disables depth testing, enables blending.
        #               Colors are added together, so sorting is not required.
        # ============= ======================================================
        window.addItem(self.fov)  # add body to plot


    def update(self, state):
        mesh = self.getTransformedMesh(state)
        # draw MAV by resetting mesh using rotated and translated points
        self.fov.setMeshData(vertexes=mesh, vertexColors=self.fov_meshColors)

    def getTransformedMesh(self, state):
        mav_position = np.array([[state.north], [state.east], [-state.altitude]])  # NED coordinates
        # attitude of mav as a rotation matrix R from body to inertial
        R = tools.rotations.euler_to_rotation(state.phi, state.theta, state.psi)
        Rcam = tools.rotations.euler_to_rotation(0, state.camera_el, state.camera_az)
        # rotate and translate points defining mav
        rotated_points = self.rotatePoints(self.rotatePoints(self.fov_points, Rcam), R)
        projected_points = self.projectOnGroundPlane(rotated_points, mav_position)
        # convert North-East Down to East-North-Up for rendering
        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        projected_points = R @ projected_points
        # convert points to triangular mesh defined as array of three 3D points (Nx3x3)
        return( self.pointsToMesh(projected_points) )

    def rotatePoints(self, points, R):
        "Rotate points by the rotation matrix R"
        rotated_points = R @ points
        return rotated_points

    def translatePoints(self, points, translation):
        "Translate points by the vector translation"
        translated_points = points + np.dot(translation, np.ones([1, points.shape[1]]))
        return translated_points

    def projectOnGroundPlane(self, points, mav_position):
        "project fov points onto ground plane"
        pn = mav_position.item(0)
        pe = mav_position.item(1)
        pd = mav_position.item(2)
        projected_points = points
        projected_points[0, 0] = pn
        projected_points[1, 0] = pe
        projected_points[2, 0] = pd
        for i in range(1,5):
            alpha = np.arctan2(points[2, i], norm(points[0:2, i]))
            if alpha > 0:
                # normal case when the frustrum line intersects the ground plane
                projected_points[0, i] = pn - pd * points[0, i] / points[2, i]
                projected_points[1, i] = pe - pd * points[1, i] / points[2, i]
            else:
                # frustrum line is above the horizon, and needs to extend to infinity
                projected_points[0, i] = pn + 9999 * points[0, i]
                projected_points[1, i] = pe + 9999 * points[1, i]
            projected_points[2, i] = 0
        return projected_points

    def getPoints(self):
        """"
            define unit vectors along fov in the camera gimbal frame
        """
        az = CAM.fov / 2
        el = CAM.fov / 2
        points = np.array([
            [0, 0, 0], # point 1 [0]
            [cos(el) * cos(az), sin(az), -sin(el) * cos(az)],  # point 2 [1]
            [cos(el) * cos(-az), sin(-az), -sin(el) * cos(-az)],  # point 3 [2]
            [cos(-el) * cos(-az), sin(-az), -sin(-el) * cos(-az)],  # point 4 [3]
            [cos(-el) * cos(az), sin(az), -sin(-el) * cos(az)],  # point 5 [4]
            ]).T

        #   define the colors for each face of triangular mesh
        meshColors = np.empty((6, 3, 4), dtype=np.float32)
        meshColors[0] = self.mygrey1  # up side (looking forward
        meshColors[1] = self.mygrey1  # right side
        meshColors[2] = self.mygrey1  # down side
        meshColors[3] = self.mygrey1  # left side
        return points, meshColors

    def pointsToMesh(self, points):
        """"
        Converts points to triangular mesh
        Each mesh face is defined by three 3D points
          (a rectangle requires two triangular mesh faces)
        """
        points = points.T
        mesh = np.array([[points[0], points[1], points[2]],  # up side (looking forward)
                         [points[0], points[1], points[4]],  # right side
                         [points[0], points[3], points[4]],  # down side
                         [points[0], points[2], points[3]],  # left side
                         ])
        return mesh
