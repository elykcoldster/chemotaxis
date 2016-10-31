class Larva:
    def __init__(self, location, theta_max=120.0, v_fwd=1.0, t_min_run=7):
        """Larva ctor
        
        Args:
        location - initial coordinate of head in the arena
        theta_max - maximum head cast angle in degrees
        v_fwd - constant forward speed of head, in mm/sec
        t_min_run - minimum run duration in seconds
        """
        self.theta_max = theta_max;
        self.v_fwd = v_fwd;
        self.t_min_run = t_min_run;
        self.location = location

    def update(self):
        """Update larva state based on transition probabilities
        """
        raise NotImplementedError
        
    def _terminate_run(self):
        """Stop forward motion and begin casting
        """
        raise NotImplementedError

    def _terminate_cast(self):
        """Stop head casting and resume running in resulting direction
        """
        raise NotImplementedError
