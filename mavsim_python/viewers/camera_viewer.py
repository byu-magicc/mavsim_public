"""
mavsim: camera viewer (for chapter 13)
    - Beard & McLain, PUP, 2012
    - Update history:
        4/15/2019 - RWB
        3/31/2022 - RWB
"""
import numpy as np
import matplotlib.pyplot as plt
import parameters.camera_parameters as CAM
from message_types.msg_camera import MsgCamera

class CameraViewer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        # Initializes a list of objects (patches and lines)
        self.handle = []
        # Specify the x,y axis limits
        plt.axis([-500, 500, -500, 500])
        # label axes
        plt.xlabel('eps_x')
        plt.ylabel('eps_y')
        self.plot_initialized = False
        self.blue = np.array([30, 144, 255, 255])/255.
        self.red = np.array([[1., 0., 0., 1]])
        self.green = np.array([0., 1., 0., 1])
        #blue = np.array([0., 0., 1., 1])
        self.yellow = np.array([1., 1., 0., 1])
        self.orange = np.array([255, 102, 0, 255])/255.

    def updateDisplay(self, projected_points):
        # draw plot elements: cart, bob, rod
        self.drawTargetOnScreen(projected_points)
        # Set initialization flag to False after first call
        if self.plot_initialized is False:
            self.plot_initialized = True
        plt.pause(0.001)

    def drawTargetOnScreen(self, projected_points):
        patch = []
        patch.append(projected_points[:, (4, 5, 6, 7)])  # top
        patch.append(projected_points[:, (4, 7, 3, 0)])  # east
        patch.append(projected_points[:, (1, 0, 4, 5)])  # north
        patch.append(projected_points[:, (1, 2, 6, 5)])  # west
        patch.append(projected_points[:, (2, 3, 7, 6)])  # south
        patch.append(projected_points[:, (0, 1, 2, 3)])  # bottom
        # create rectangle on first call, update on subsequent calls
        if self.plot_initialized is False:
            # Create the Rectangle patch and append its handle
            # to the handle list
            for i in range(0, 6):
                self.handle.append( plt.Polygon(patch[i].T) )
            #color for each patch
            self.handle[0].set_color(self.red)  # top
            self.handle[1].set_color(self.blue) # east
            self.handle[2].set_color(self.green) # north
            self.handle[3].set_color(self.yellow) # west
            self.handle[4].set_color(self.orange) # south
            self.handle[5].set_color(self.red)  # bottom
            # Add the patch to the axes
            for i in range(0, 6):
                self.ax.add_patch(self.handle[i])
        else:
            for i in range(0, 6):
                self.handle[i].set_xy(patch[i].T) # Update patch