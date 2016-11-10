import matplotlib.pyplot as plt
from view import View

class ArenaView(View):
    def __init__(self):
        self.head_locs = []
        # ? # self.wv_head_locs = [] 
        self.joint_locs = []
        

    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle):
        """Save information about the larva
        """
        self.head_locs.append(head_loc)
        self.joint_locs.append(joint_loc)
        # TODO: Maybe also use state information to draw weathervane casts
        # (head locations during WV casts) different color than normal casts?

    def draw(self):
        """Prints out the current view
        """
        raise NotImplementedError

    def clear(self):
        """Discard the saved information - empty view
        """
        self.head_locs.clear()
        self.joint_locs.clear()

    def export(self, path):
        """Write out the view to file
        """
        # Save plot as png
        raise NotImplementedError
