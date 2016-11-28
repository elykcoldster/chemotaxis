import numpy as np
from sim_object import SimObject

class Arena(SimObject):
    def __init__(self, source_position=np.array([0,0]), source_strength=10, source_decay_rate=5, arena_length=20, arena_width=16):
        self.source_position = source_position
        self.source_strength = source_strength
        self.sigma = source_decay_rate
        self.length = arena_length # x-size
        self.width = arena_width # y-size

    def update(self):
        pass

    def concentration_at_loc(self, loc):
        distance = np.linalg.norm(loc - self.source_position)
        return self.source_strength*1/np.sqrt(2*np.pi*self.sigma**2)*np.exp(-distance * distance/(2*self.sigma**2))
    
    def __str__(self):
        return ('Source Location: ' + str(self.source_position)
                + '\tSource Strength: ' + str(self.source_strength)
                + '\tSource Decay Rate: ' + str(self.sigma))
    