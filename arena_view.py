import matplotlib.pyplot as plt
import numpy as np
from view import View
from model import Model as m

class ArenaView(View):
    def __init__(self):
        self.head_locs = []
        # ? # self.wv_head_locs = [] 
        self.joint_locs = []
        

    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle, source_position):
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
        nx, ny = 100.,100.
        xmin = m.get_instance().get_arena().x_min
        xmax = m.get_instance().get_arena().x_max
        ymin = m.get_instance().get_arena().y_min
        ymax = m.get_instance().get_arena().y_max
        xgrid, ygrid = np.mgrid[xmin:xmax:(xmax-xmin)/nx,ymin:ymax:(ymax-ymin)/ny]
        cmap = plt.cm.gray
        cmap.set_bad('white')
        im = xgrid * 0;
        for i in range(0, int(nx)):
            for j in range(0, int(ny)):
                im[i][int(ny) - 1 - j] = m.get_instance().get_arena().concentration_at_loc(np.array([xgrid[i][i], ygrid[j][j]]))
        plt.imshow(im.T, cmap=cmap, vmin=0, vmax=m.get_instance().get_arena().base_concentration() ,extent=[xmin, xmax, ymin, ymax])
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
        nx, ny = 100.,100.
        xmin = m.get_instance().get_arena().x_min
        xmax = m.get_instance().get_arena().x_max
        ymin = m.get_instance().get_arena().y_min
        ymax = m.get_instance().get_arena().y_max
        xgrid, ygrid = np.mgrid[xmin:xmax:(xmax-xmin)/nx,ymin:ymax:(ymax-ymin)/ny]
        cmap = plt.cm.gray
        cmap.set_bad('white')
        im = xgrid * 0;
        for i in range(0, int(nx)):
            for j in range(0, int(ny)):
                im[i][j] = m.get_instance().get_arena().concentration_at_loc(np.array([xgrid[i][i], ygrid[j][j]]))
        plt.imshow(im.T, cmap=cmap, vmin=0, vmax=m.get_instance().get_arena().base_concentration() ,extent=[xmin, xmax, ymin, ymax])
        # Save plot as png
        plt.plot(self.head_locs[:,0],self.head_locs[:,1],'b',linewidth=3)
        plt.plot(self.joint_locs[:,0],self.joint_locs[:,1],'r',linewidth=2)
        plt.title('Larva Trajectory')
        plt.xlabel('x position')
        plt.ylabel('y position')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(path + '.png')
