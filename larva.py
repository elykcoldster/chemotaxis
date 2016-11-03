from enum import Enum
import random as rn
class Larva:
    class LarvaState(Enum):
        # Crawl states
        CRAWL_FWD = 1
        # Weathervaning states
        WV_CRAWL_FWD = 2
        WV_CRAWL_FWD_WHILE_CAST = 3
        WV_CHANGE_CAST_DIR = 4
        # Casting states
        CAST_START = 5
        CAST_TURN = 6
        CAST_TURN_AFTER_MIN_ANGLE = 7
        CAST_TURN_TO_MIDDLE = 8
        CAST_TURN_RANDOM_DIR = 9


    def crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def wv_crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def wv_crawl_fwd_while_cast(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def wv_change_cast_dir(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def cast_start(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def cast_turn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def cast_turn_after_min_angle(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def cast_turn_to_middle(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    def cast_turn_random_dir(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        raise NotImplementedError

    # Function dispatch table:
    state_fcns = {LarvaState.CRAWL_FWD: crawl_fwd,
                  LarvaState.WV_CRAWL_FWD: wv_crawl_fwd,
                  LarvaState.WV_CRAWL_FWD_WHILE_CAST: wv_crawl_fwd_while_cast,
                  LarvaState.WV_CHANGE_CAST_DIR: wv_change_cast_dir,
                  LarvaState.CAST_START: cast_start,
                  LarvaState.CAST_TURN: cast_turn,
                  LarvaState.CAST_TURN_AFTER_MIN_ANGLE: cast_turn_after_min_angle,
                  LarvaState.CAST_TURN_TO_MIDDLE: cast_turn_to_middle,
                  LarvaState.CAST_TURN_RANDOM_DIR: cast_turn_random_dir}
        
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
        self.state = LarvaState.CRAWL_FWD

    def update(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume):
        """Update larva state based on transition probabilities
        """
        # Generate a random number for probabilistic events
        rand = rn.random() # TODO: seed random in main function instead of here
        fcn = state_fcns.get(self.state)
        if not fcn:
            raise ValueError("Not a valid Larva State!")
        fcn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)

    # def _terminate_run(self):
    #     """Stop forward motion and begin casting
    #     """
    #     raise NotImplementedError

    # def _terminate_cast(self):
    #     """Stop head casting and resume running in resulting direction
    #     """
    #     raise NotImplementedError
