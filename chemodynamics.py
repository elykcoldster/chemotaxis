import numpy as np

arena_size = 5 # arbitrary definition, will change later
source_location = np.array([0.0, 0.0, 0.0]) # assume source is at the center of cartesian space
source_value = 10 # again, arbitrary definition, will change later
decay_rate = 1 # ADWCL

def p_run_termination():
	return 0.0

def p_cast_termination():
	return 0.0

def p_weathervane():
	return 0.0