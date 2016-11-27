import numpy as np
from sim_object import SimObject

class Arena(SimObject):
    def __init__(self, x_min=-33, x_max=33, y_min=-50, y_max=50, source_position=np.array([0,0]), source_strength=10, source_decay_rate=5):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.source_position = source_position
        self.source_strength = source_strength
        self.sigma = source_decay_rate

    def update(self):
        pass

    def concentration_at_loc(self, loc):
        distance = np.linalg.norm(loc - self.source_position)
        return self.source_strength*1/np.sqrt(2*np.pi*self.sigma**2)*np.exp(-distance * distance/(2*self.sigma**2))
    
    def __str__(self):
        return ('Source Location: ' + str(self.source_position)
                + '\tSource Strength: ' + str(self.source_strength)
                + '\tSource Decay Rate: ' + str(self.sigma))
    