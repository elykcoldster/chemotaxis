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
        plt.title('Perception History')
        plt.xlabel('Time (s)')
        plt.ylabel('Perception (uM)')
        plt.show()

    def clear(self):
        """Discard the saved information - empty view
        """
        self.perception_history = []

    def export(self, path):
        """Write out the view to file
        """
        # Save plot as png
        dt = m.get_instance().dt
        self.perception_history = m.get_instance().larvae[0].history
        t = np.arange(0,len(self.perception_history)*dt,dt)
        plt.plot(t,self.perception_history)
        plt.title('Perception History')
        plt.xlabel('Time (s)')
        plt.ylabel('Perception (uM)')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(path + '.png')
