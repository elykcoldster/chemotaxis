import matplotlib.pyplot as plt
import numpy as np
from view import View

class MoveStatsView(View):
    def __init__(self):
        self.numTimeSteps = 0
        self.body_angles = []
        self.reorientation_speeds = []
        self.head_angles = []
        self.bearings = []
        
    def calcBodyAngle(velocity):
        # dot product between i-cap and velocity is just the x-component of velocity
        alpha = np.arccos(velocity[0])
        # since range of arccos is [0,pi], need to correct by looking at the y-value
        if(velocity[1] < 0):
            alpha = 2*np.pi - alpha
        return np.degrees(alpha)
        
        
    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle):
        """Save information about the movement stats of larva
        """
        body_angle = calcBodyAngle(velocity)
        if self.numTimeSteps == 0:
            self.head_angles = [head_angle]
            self.body_angles = [body_angle]
        else:
            self.head_angles = np.append(self.head_angles, [head_angle], axis=0)
            self.body_angles = np.append(self.body_angles, [body_angle], axis = 0)
            

    def draw(self):
        """Prints out the current view
        """
        plt.plot(self.head_locs[:,0],self.head_locs[:,1],'b',linewidth=3)
        plt.plot(self.joint_locs[:,0],self.joint_locs[:,1],'r',linewidth=2)
        plt.title('Larva Trajectory')
        plt.xlabel('x position')
        plt.ylabel('y position')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def clear(self):
        """Discard the saved information - empty view
        """
        self.head_locs = []
        self.joint_locs = []

    def export(self, path):
        """Write out the view to file
        """
        # Save plot as png
        plt.plot(self.head_locs[:,0],self.head_locs[:,1],'b',linewidth=3)
        plt.plot(self.joint_locs[:,0],self.joint_locs[:,1],'r',linewidth=2)
        plt.title('Larva Trajectory')
        plt.xlabel('x position')
        plt.ylabel('y position')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(path + '.png')
