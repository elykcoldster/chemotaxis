from enum import Enum
import random as rn
import math
import numpy as np
from model import Model as m


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

    def p_run_term():
        r = self.run_term_base
        for t in range(0,self.t_run_term):
            r += self.history[len(self.history) - t/dt - 1] * k_run_term[len(k_run_term) - t/dt - 1];
        return m.get_instance().dt * r

    def p_cast_term():
        r = self.cast_term_base
        for t in range(0,self.t_cast_term):
            r += self.history[len(self.history) - t/dt - 1] * k_cast_term[len(k_cast_term) - t/dt - 1];
        return m.get_instance().dt * r
    def p_wv():

    def p_wv_cast_resume():

    def perceive():
        h2s = self.head_loc - m.get_instance().source_position
        distance = np.linalg.norm(h2s)
        strength = m.get_instance().source_strength
        sigma = m.get_instance().source_decay_rate
        return 1/np.sqrt(2*np.pi*sigma*sigma)*np.exp(-distance * distance/(2*sigma*sigma))

    def crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CRAWL FWD')
        if m.get_instance().time - self.cur_run_time > self.t_min_run:
            self.state = LarvaState.WV_CRAWL_FWD
        else:
            distance = m.get_instance().dt * self.cast_speed  # TODO: set dt in Model
            self.head_loc = self.head_loc + distance * self.velocity
            self.joint_loc = self.joint_loc + distance * self.velocity

    def wv(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WEATHERVANE PSEUDO-STATE')
        if self.state == LarvaState.WV_CRAWL_FWD:
            wv_crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == LarvaState.WV_CRAWL_FWD_WHILE_CAST:
            wv_crawl_fwd_while_cast(
                p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == LarvaState.WV_CHANGE_CAST_DIR:
            wv_change_cast_dir(p_run_term, p_cast_term,
                               p_wv, p_wv_cast_resume, rand)
        if rand < p_run_term:
            # Note: If we terminate a run while in the middle of weathervane casting, we DO NOT
            # modify the velocity to point in the direction of the weathervane cast
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
        # Set cast direction in this state
        # If current head location is left of midline, turn direction is counter-clockwise (positive)
        # If current head location is right of midline, turn direction is clockwise (negative)
        # Translate so joint is the origin
        translated_head = self.head_loc - self.joint_loc
        # Turn direction determined by this determinant:
        # | velocity.x   velocity.y |
        # | head.x       head.y     |
        mat = np.array([self.velocity, self.translated_head])
        self.cast_dir = np.sign(np.linalg.det(mat))
        self.state = LarvaState.CAST_TURN

    def cast_turn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN')
        self.rotate_normal_cast()
        if self.get_head_angle() > self.theta_min:
            self.state = LarvaState.CAST_TURN_AFTER_MIN_ANGLE

    def cast_turn_after_min_angle(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN AFTER MIN ANGLE')
        self.rotate_normal_cast()
        if rand < p_cast_term:
            self.state = LarvaState.CRAWL_FWD
        else:
            if self.get_head_angle() > self.theta_max:
                self.cast_dir *= -1
                self.state = LarvaState.CAST_TURN_TO_MIDDLE

    def cast_turn_to_middle(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN TO MIDDLE')
        self.rotate_normal_cast()
        if abs(self.get_head_angle()) < self.cast_epsilon:
            self.state = LarvaState.CAST_TURN_RANDOM_DIR

    def cast_turn_random_dir(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN RANDOM DIR')
        self.cast_dir = np.sign(rand - 0.5)
        self.state = LarvaState.CAST_TURN

    # Function dispatch table:
    state_fcns = {LarvaState.CRAWL_FWD: crawl_fwd,
                  LarvaState.WV_CRAWL_FWD: wv,
                  LarvaState.WV_CRAWL_FWD_WHILE_CAST: wv,
                  LarvaState.WV_CHANGE_CAST_DIR: wv,
                  LarvaState.CAST_START: cast_start,
                  LarvaState.CAST_TURN: cast_turn,
                  LarvaState.CAST_TURN_AFTER_MIN_ANGLE: cast_turn_after_min_angle,
                  LarvaState.CAST_TURN_TO_MIDDLE: cast_turn_to_middle,
                  LarvaState.CAST_TURN_RANDOM_DIR: cast_turn_random_dir}

    def __init__(self, location, velocity, head_length=1, theta_max=120.0, theta_min=37, cast_speed=240, wv_theta_max=20, wv_cast_speed=60, v_fwd=1.0, t_min_run=7, run_term_base=0.148, cast_term_base=2, wv_term_base=2, wv_cast_resume=1, t_run_term=20, t_cast_term=1):
        """Larva ctor

        Args:
        location - initial coordinate of head in the arena (vector)
        velocity - initial velocity vector (a heading(vector))
        head_length - length of head body segment (mm)
        theta_max - maximum head cast angle (degrees)
        theta_min - minimum head cast angle (degrees)
        cast_speed - rotational speed of head casts (degrees/sec)
        wv_theta_max - maximum weathervaning head cast angle (degrees)
        wv_cast_speed - rotational speed of weathervane casts (degrees/sec)
        v_fwd - constant forward speed of head (mm/sec)
        t_min_run - minimum run duration (sec)
        """
        self.head_loc = location
        # Ensure it is a unit vector
        self.velocity = velocity / np.linalg.norm(velocity)
        self.head_length = head_length
        # Initially, the larva body will be straight, so the joint will be
        # behind the head along the velocity vector
        self.joint_loc = self.head_loc - (self.head_length * self.velocity)
        self.theta_max = theta_max
        self.theta_min = theta_min
        self.cast_speed = cast_speed
        self.cast_epsilon = cast_speed * m.get_instance().dt / 0.5
        self.wv_theta_max = wv_theta_max
        self.wv_cast_speed = wv_cast_speed
        self.v_fwd = v_fwd
        self.t_min_run = t_min_run
        self.run_term_base = run_term_base
        self.cast_term_base = cast_term_base
        self.wv_term_base = wv_term_base
        self.wv_cast_resume = wv_cast_resume
        # run termination time and kernel
        self.t_run_term = t_run_term
        self.k_run_term = np.arange(1, -1, m.get_instance().dt/t_run_term)
        # cast termination time and kernel
        self.t_cast_term = t_cast_term
        self.k_cast_term = np.arange(0, 150, m.get_instance().dt/t_cast_term) # may need piecewise kernel later
        # init perceptual history array
        self.history = []
        # init larva state (crawl forward)
        self.state = LarvaState.CRAWL_FWD

    def update(self):
        """Update larva state based on transition probabilities
        """
        # Generate a random number for probabilistic events
        rand = rn.random()  # TODO: seed random in main function instead of here
        # Perceive the surrounding world and calculate probabilities here:
        p_run_term = rn.random()
        p_cast_term = rn.random()
        p_wv = rn.random()
        p_wv_cast_resume = rn.random()

        self.history.append(perceive())

        fcn = state_fcns.get(self.state)
        if not fcn:
            raise ValueError("Not a valid Larva State!")
        fcn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)

    def rotate_normal_cast(self):
        angle = m.get_instance().dt * self.cast_speed * self.cast_dir
        self.rotate_head(angle)

    def rotate_weathervane_cast(self):
        angle = m.get_instance().dt * self.wv_cast_speed * self.cast_dir
        self.rotate_head(angle)

    def rotate_head(self, angle):
        """Rotate the head of the larva by specified angle

        Args:
        angle - rotation angle, positive:counter-clockwise, negative:clockwise, (degrees)
        """
        # Convert angle to radians
        theta = math.radians(angle)
        rotation_matrix = np.array(
            [(math.cos(theta), -math.sin(theta)), (math.sin(theta), math.cos(theta))])
        # Translate rotation point to origin for rotation
        self.head_loc -= self.joint_loc
        self.head_loc = np.dot(rotation_matrix, self.head_loc)
        # Translate back to original region
        self.head_loc += self.joint_loc

    def get_head_angle(self):
        """Get absolute angle of head with respect to the midline (velocity vector)
        """
        head_vec = self.head_loc - self.joint_loc # joint is origin
        cos_theta = np.dot(head_vec, self.velocity) / (np.linalg.norm(head_vec) * np.linalg.norm(self.velocity))
        return = math.degrees(math.acos(cos_theta))
