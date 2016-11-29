import matplotlib.pyplot as plt
import numpy as np
from view import View
from model import Model as m

class PerceptionView(View):
    def __init__(self):
        self.perception_history=[]
        

    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle, source_position):
        """Save information about the larva
        """
        pass

    def draw(self):
        """Prints out the current view
        """
        dt = m.get_instance().dt
        self.perception_history = m.get_instance().larvae[0].history
        t = np.arange(0,len(self.perception_history)*dt,dt)
        plt.plot(t,self.perception_history)
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
