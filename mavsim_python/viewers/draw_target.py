"""
mavsim_python: drawing tools
    - Beard & McLain, PUP, 2012
    - Update history:
        3/30/2022 - RWB
"""
import numpy as np
import pyqtgraph.opengl as gl


class DrawTarget:
    def __init__(self, position, window):
        # get points that define the target and the mesh colors
        self.target_points, self.target_meshColors = self.getPoints()
        mesh = self.getTransforedMesh(position)
        self.target_body = gl.GLMeshItem(vertexes=mesh,  # defines the triangular mesh (Nx3x3)
                                         vertexColors=self.target_meshColors,  # defines mesh colors (Nx1)
                                         drawEdges=True,  # draw edges between mesh elements
                                         smooth=False,  # speeds up rendering
                                         computeNormals=False)  # speeds up rendering
        self.target_body.setGLOptions('translucent')  # puts waypoint behind obstacles
        # ============= options include
        # opaque        Enables depth testing and disables blending
        # translucent   Enables depth testing and blending
        #               Elements must be drawn sorted back-to-front for
        #               translucency to work correctly.
        # additive      Disables depth testing, enables blending.
        #               Colors are added together, so sorting is not required.
        # ============= ======================================================
        window.addItem(self.target_body)  # add body to plot

    def update(self, position):
        mesh = self.getTransforedMesh(position)
        # draw MAV by resetting mesh using rotated and translated points
        self.target_body.setMeshData(vertexes=mesh, vertexColors=self.target_meshColors)

    def getTransforedMesh(self, position):
        # translate points defining target
        translated_points = self.translatePoints(self.target_points, position)
        # convert North-East Down to East-North-Up for rendering
        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        translated_points = R @ translated_points
        # convert points to triangular mesh defined as array of three 3D points (Nx3x3)
        return( self.pointsToMesh(translated_points) )

    def translatePoints(self, points, translation):
        "Translate points by the vector translation"
        translated_points = points + np.dot(translation, np.ones([1, points.shape[1]]))
        return translated_points

    def getPoints(self):
        """"
            Points that define the target, and the colors of the triangular mesh
        """
        # define MAV body parameters
        length = 15

        # points are in NED coordinates
        #   define the points on the target (box
        points = np.array([[length / 2, length / 2, 0],  # point 0
                           [length / 2, -length / 2, 0],  # point 1
                           [-length / 2, -length / 2, 0],  # point 2
                           [-length / 2, length / 2, 0],  # point 3
                           [length / 2, length / 2, -length],  # point 4
                           [length / 2, -length / 2, -length],  # point 5
                           [-length / 2, -length / 2, -length],  # point 6
                           [-length / 2, length / 2, -length],  # point 7
                           ]).T

        #   define the colors for each face of triangular mesh
        red = np.array([1., 0., 0., 1])
        green = np.array([0., 1., 0., 1])
        blue = np.array([30, 144, 255, 255])/255.
        yellow = np.array([1., 1., 0., 1])
        orange = np.array([255, 102, 0, 255])/255.
        meshColors = np.empty((13, 3, 4), dtype=np.float32)
        meshColors[0] = blue  # east face
        meshColors[1] = blue  # east face
        meshColors[2] = green  # north face
        meshColors[3] = green  # north face
        meshColors[4] = yellow  # west face
        meshColors[5] = yellow  # west face
        meshColors[6] = orange  # south face
        meshColors[7] = orange  # south face
        meshColors[8] = red   # top
        meshColors[9] = red   # top
        return points, meshColors

    def pointsToMesh(self, points):
        """"
        Converts points to triangular mesh
        Each mesh face is defined by three 3D points
          (a rectangle requires two triangular mesh faces)
        """
        points = points.T
        mesh = np.array([
            [points[0], points[4], points[7]],  # east face
            [points[0], points[3], points[7]],  # east face
            [points[0], points[4], points[1]],  # north face
            [points[5], points[4], points[1]],  # north face
            [points[5], points[1], points[2]],  # west face
            [points[5], points[6], points[2]],  # west face
            [points[6], points[2], points[3]],  # south face
            [points[6], points[7], points[3]],  # south face
            [points[5], points[6], points[7]],  # top
            [points[5], points[4], points[7]],  # top
            ])
        return mesh
