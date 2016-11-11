import matplotlib.pyplot as plt
import numpy as np
from view import View

class ArenaView(View):
    def __init__(self):
        self.head_locs = []
        # ? # self.wv_head_locs = [] 
        self.joint_locs = []
        

    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle):
        """Save information about the larva
        """
        if len(self.head_locs) == 0:
            self.head_locs = [head_loc]
            self.joint_locs = [joint_loc]
        else:
            self.head_locs = np.append(self.head_locs, [head_loc], axis=0)
            self.joint_locs = np.append(self.joint_locs, [joint_loc], axis=0)
        # TODO: Maybe also use state information to draw weathervane casts
        # (head locations during WV casts) different color than normal casts?

    def draw(self):
        """Prints out the current view
        """
        plt.plot(self.head_locs[:,0],self.head_locs[:,1],'b',linewidth=3)
        plt.plot(self.joint_locs[:,0],self.joint_locs[:,1],'r',linewidth=2)
        plt.title('Larva Trajectory')
        plt.xlabel('x position')
        plt.ylabel('y position')

        plt.gca().set_aspect('equal', adjustable='box')

    def clear(self):
        """Discard the saved information - empty view
        """
        self.head_locs = []
        self.joint_locs = []

    def export(self, path):
        """Write out the view to file
        """
        # Save plot as png
        self.draw()
        plt.savefig(path + '.png')
