import numpy as np
from sim_object import SimObject

class DecayArena(SimObject):
    def __init__(self, source_position=np.array([0,0]), source_strength=10, source_variance=5, decay_rate=1e-3):
        self.source_position = source_position
        self.source_strength = source_strength
        self.sigma = source_variance
        self.decay_rate = decay_rate

    def update(self):
        self.source_strength -= self.decay_rate * self.source_strength

    def concentration_at_loc(self, loc):
        distance = np.linalg.norm(loc - self.source_position)
        return self.source_strength*1/np.sqrt(2*np.pi*self.sigma**2)*np.exp(-distance * distance/(2*self.sigma**2))
    
    def __str__(self):
        return ('Source Location: ' + str(self.source_position)
                + '\tSource Strength: ' + str(self.source_strength)
                + '\tSource Variance: ' + str(self.sigma)
                + '\tSource Decay: ' + str(self.decay_rate))
    