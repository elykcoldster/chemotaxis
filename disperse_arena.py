import numpy as np
from model import Model as m
from sim_object import SimObject

class DisperseArena(SimObject):
    def __init__(self, x_min=-33, x_max=33, y_min=-50, y_max=50, source_position=np.array([0,0]), source_strength=10, sigma_growth_rate=1e-2, sigma_bound=1.5):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.source_position = source_position
        self.source_strength = source_strength
        self.base_source_strength = source_strength
        self.sigma = 1
        self.sigma_bound = 1.5
        self.sigma_growth_rate = sigma_growth_rate

    def update(self):
        self.sigma += (self.sigma_bound - self.sigma) * self.sigma_growth_rate * m.get_instance().dt

    def concentration_at_loc(self, loc):
        distance = np.linalg.norm(loc - self.source_position)
        return self.source_strength*1/np.sqrt(2*np.pi*self.sigma**2)*np.exp(-distance * distance/(2*self.sigma**2))
    def base_concentration(self):
        return self.source_strength
    
    def __str__(self):
        return ('Source Location: ' + str(self.source_position)
                + '\tSource Strength: ' + str(self.source_strength)
                + '\tSource Bound: ' + str(self.sigma_bound)
                + '\tSigma Growth Rate: ' + str(self.sigma_growth_rate))
    