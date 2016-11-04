from enum import Enum
import random as rn
import model
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
        print ('State: CRAWL FWD')
        if model.modelInstance.time - self.cur_run_time > self.t_min_run:
            self.state = LarvaState.WV_CRAWL_FWD

    def wv(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WEATHERVANE PSEUDO-STATE')
        if self.state == LarvaState.WV_CRAWL_FWD:
            wv_crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == LarvaState.WV_CRAWL_FWD_WHILE_CAST:
            wv_crawl_fwd_while_cast(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == LarvaState.WV_CHANGE_CAST_DIR:
            wv_change_cast_dir(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        if rand < p_run_term:
            self.state = LarvaState.CAST_START

    def wv_crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WV CRAWL FWD')
        if rand < p_wv_cast_resume:
            self.state = LarvaState.WV_CRAWL_FWD_WHILE_CAST

    def wv_crawl_fwd_while_cast(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WV CRAWL FWD WHILE CAST')
        if rand < p_wv:
            self.state = LarvaState.WV_CRAWL_FWD
        else:
            if self.get_head_angle() > self.wv_theta_max:
                self.state = LarvaState.WV_CHANGE_CAST_DIR

    def wv_change_cast_dir(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WV CHANGE CAST DIR')
        self.state = LarvaState.WV_CRAWL_FWD_WHILE_CAST

    def cast_start(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST START')
        self.state = LarvaState.CAST_TURN

    def cast_turn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN')
        if self.get_head_angle() > self.theta_min:
            self.state = LarvaState.CAST_TURN_AFTER_MIN_ANGLE

    def cast_turn_after_min_angle(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN AFTER MIN ANGLE')
        if rand < p_cast_term:
            self.state = LarvaState.CRAWL_FWD
        else:
            if self.get_head_angle() > self.theta_max:
                self.state = LarvaState.CAST_TURN_TO_MIDDLE

    def cast_turn_to_middle(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN TO MIDDLE')
        if abs(self.get_head_angle()) < self.cast_epsilon:
            self.state = LarvaState.CAST_TURN_RANDOM_DIR

    def cast_turn_random_dir(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN RANDOM DIR')
        self.state = LarvaState.CAST_TURN

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
    state_fcns = {LarvaState.CRAWL_FWD: crawl_fwd,
                  LarvaState.WV_CRAWL_FWD: wv,
                  LarvaState.WV_CRAWL_FWD_WHILE_CAST: wv,
                  LarvaState.WV_CHANGE_CAST_DIR: wv,
                  LarvaState.CAST_START: cast_start,
                  LarvaState.CAST_TURN: cast_turn,
                  LarvaState.CAST_TURN_AFTER_MIN_ANGLE: cast_turn_after_min_angle,
                  LarvaState.CAST_TURN_TO_MIDDLE: cast_turn_to_middle,
                  LarvaState.CAST_TURN_RANDOM_DIR: cast_turn_random_dir}
        
    def __init__(self, location, theta_max=120.0, theta_min=37, cast_speed=240, wv_theta_max=20, v_fwd=1.0, t_min_run=7):
        """Larva ctor
        
        Args:
        location - initial coordinate of head in the arena
        theta_max - maximum head cast angle (degrees)
        theta_min - minimum head cast angle (degrees)
        cast_speed - rotational speed of head casts (degrees/sec)
        wv_theta_max - maximum weathervaning head cast angle (degrees)
        v_fwd - constant forward speed of head (mm/sec)
        t_min_run - minimum run duration (sec)
        """
        self.location = location
        self.theta_max = theta_max
        self.theta_min = theta_min
        self.cast_speed = cast_speed
        self.cast_epsilon = cast_speed * model.modelInstance.dt / 0.5;
        self.wv_theta_max = wv_theta_max
        self.v_fwd = v_fwd
        self.t_min_run = t_min_run
        self.state = LarvaState.CRAWL_FWD
        # TODO: get a pointer to the Model. Or there should be a global pointer to the singleton Model

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
