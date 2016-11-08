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

    def p_run_term(self):
        r = self.run_term_base
        dt = m.get_instance().dt
        if len(self.history) > 1:
            term_time = np.minimum(len(self.history) * dt, self.t_run_term)
            for t in np.arange(0,term_time,dt):
                tsteps = int(t/dt)
                C = self.history[len(self.history) - tsteps - 1]
                C_prev = self.history[len(self.history) - tsteps - 2]

                phi = 0
                if len(self.history) - tsteps - 2 >= 0:
                    phi = (np.log(C)-np.log(C_prev))/dt
                kernel = self.k_run_term[len(self.k_run_term) - tsteps - 1]
                r += phi * kernel
        return m.get_instance().dt * r

    def p_cast_term(self):
        r = self.cast_term_base
        dt = m.get_instance().dt
        if len(self.history) > 1:
            term_time = np.minimum(len(self.history) * dt, self.t_run_term)
            for t in arange(0,term_time,dt):
                tsteps = int(t/dt)
                C = self.history[len(self.history) - tsteps - 1]
                C_prev = self.history[len(self.history) - tsteps - 2]

                phi = 0
                if len(self.history) - tsteps - 2 >= 0:
                    phi = (np.log(C)-np.log(C_prev))/dt
                kernel = self.k_cast_term[len(self.k_cast_term) - tsteps - 1]
                r += phi * kernel
        return m.get_instance().dt * r

    def p_wv(self):
        pass

    def p_wv_cast_resume(self):
        pass

    def perceive(self):
        h2s = self.head_loc - m.get_instance().source_position
        distance = np.linalg.norm(h2s)
        strength = m.get_instance().source_strength
        sigma = m.get_instance().source_decay_rate
        return strength*1/np.sqrt(2*np.pi*sigma*sigma)*np.exp(-distance * distance/(2*sigma*sigma))


    def crawl_fwd(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CRAWL FWD')
        if m.get_instance().time - self.run_start_time > self.t_min_run:
            self.state = Larva.LarvaState.WV_CRAWL_FWD
        else:
            self.move_forward()

    def wv(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WEATHERVANE PSEUDO-STATE')
        if self.state == Larva.LarvaState.WV_CRAWL_FWD:
            self.wv_crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == Larva.LarvaState.WV_CRAWL_FWD_WHILE_CAST:
            self.wv_crawl_fwd_while_cast(
                p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == Larva.LarvaState.WV_CHANGE_CAST_DIR:
            self.wv_change_cast_dir(p_run_term, p_cast_term,
                               p_wv, p_wv_cast_resume, rand)
        if rand < p_run_term:
            # Note: If we terminate a run while in the middle of weathervane casting, we DO NOT
            # modify the velocity to point in the direction of the weathervane cast
            self.state = Larva.LarvaState.CAST_START

    def wv_crawl_fwd(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WV CRAWL FWD')
        self.move_forward()
        if rand < p_wv_cast_resume:
            # Pick a random cast direction? (need to confirm that this is the right thing to do)
            self.cast_dir = np.sign(rand - 0.5)
            self.state = Larva.LarvaState.WV_CRAWL_FWD_WHILE_CAST

    def wv_crawl_fwd_while_cast(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WV CRAWL FWD WHILE CAST')
        self.rotate_weathervane_cast()
        self.move_forward()
        if rand < p_wv:
            # When weathervaning stops, the velocity is updated
            self.update_velocity()
            self.state = Larva.LarvaState.WV_CRAWL_FWD
        else:
            if self.get_head_angle() > self.wv_theta_max:
                self.state = Larva.LarvaState.WV_CHANGE_CAST_DIR

    def wv_change_cast_dir(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: WV CHANGE CAST DIR')
        self.cast_dir *= -1
        self.state = Larva.LarvaState.WV_CRAWL_FWD_WHILE_CAST

    def cast_start(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST START')
        # Set cast direction in this state
        # If current head location is left of midline, turn direction is counter-clockwise (positive)
        # If current head location is right of midline, turn direction is clockwise (negative)
        # Translate so joint is the origin
        translated_head = self.head_loc - self.joint_loc
        # Turn direction determined by this determinant:
        # | velocity.x   velocity.y |
        # | head.x       head.y     |
        mat = np.array([self.velocity, translated_head])
        self.cast_dir = np.sign(np.linalg.det(mat))
        self.state = Larva.LarvaState.CAST_TURN

    def cast_turn(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN')
        self.rotate_normal_cast()
        if self.get_head_angle() > self.theta_min:
            self.state = Larva.LarvaState.CAST_TURN_AFTER_MIN_ANGLE

    def cast_turn_after_min_angle(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN AFTER MIN ANGLE')
        self.rotate_normal_cast()
        if rand < p_cast_term:
            # Cast termination results in a new velocity vector
            self.update_velocity()
            self.run_start_time = m.get_instance().time
            self.state = Larva.LarvaState.CRAWL_FWD
        else:
            if self.get_head_angle() > self.theta_max:
                self.cast_dir *= -1
                self.state = Larva.LarvaState.CAST_TURN_TO_MIDDLE

    def cast_turn_to_middle(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN TO MIDDLE')
        self.rotate_normal_cast()
        if abs(self.get_head_angle()) < self.cast_epsilon:
            self.state = Larva.LarvaState.CAST_TURN_RANDOM_DIR

    def cast_turn_random_dir(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        print ('State: CAST TURN RANDOM DIR')
        self.cast_dir = np.sign(rand - 0.5)
        self.state = Larva.LarvaState.CAST_TURN

    # Function dispatch table:
    state_fcns = {LarvaState.CRAWL_FWD: 'crawl_fwd',
                  LarvaState.WV_CRAWL_FWD: 'wv',
                  LarvaState.WV_CRAWL_FWD_WHILE_CAST: 'wv',
                  LarvaState.WV_CHANGE_CAST_DIR: 'wv',
                  LarvaState.CAST_START: 'cast_start',
                  LarvaState.CAST_TURN: 'cast_turn',
                  LarvaState.CAST_TURN_AFTER_MIN_ANGLE: 'cast_turn_after_min_angle',
                  LarvaState.CAST_TURN_TO_MIDDLE: 'cast_turn_to_middle',
                  LarvaState.CAST_TURN_RANDOM_DIR: 'cast_turn_random_dir'}

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
        self.k_run_term = np.arange(1, -1, -m.get_instance().dt/t_run_term)
        # cast termination time and kernel
        self.t_cast_term = t_cast_term
        self.k_cast_term = np.arange(0, 150, m.get_instance().dt/t_cast_term) # may need piecewise kernel later
        # init perceptual history array
        self.history = []
        # init larva state (crawl forward)
        self.run_start_time = m.get_instance().time
        self.state = Larva.LarvaState.CRAWL_FWD

    def update(self):
        """Update larva state based on transition probabilities
        """
        print('Updating a larva')
        # Generate a random number for probabilistic events
        rand = rn.random()  # TODO: seed random in main function instead of here
        # Perceive the surrounding world and calculate probabilities here:
        p_run_term = self.p_run_term()
        p_cast_term = rn.random()
        p_wv = rn.random()
        p_wv_cast_resume = rn.random()

        self.history.append(self.perceive())

        fcn_name = self.state_fcns.get(self.state)
        if not fcn_name:
            raise ValueError("Not a valid Larva State!")
        fcn = getattr(self, fcn_name)
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

    def move_forward(self):
        distance = m.get_instance().dt * self.v_fwd  # TODO: set dt in Model
        self.head_loc = self.head_loc + distance * self.velocity
        self.joint_loc = self.joint_loc + distance * self.velocity
    
    def update_velocity(self):
        """Set velocity to be in the direction of vector from joint to head
        """
        new_vel = self.head_loc - self.joint_loc
        self.velocity = new_vel / np.linalg.norm(new_vel)

    def get_head_angle(self):
        """Get absolute angle of head with respect to the midline (velocity vector)
        """
        head_vec = self.head_loc - self.joint_loc # joint is origin
        cos_theta = np.dot(head_vec, self.velocity) / (np.linalg.norm(head_vec) * np.linalg.norm(self.velocity))
        # We have to clamp the cosine angle because of rounding errors (an issue when the two vectors point in the same direction)
        cos_theta = min(1.0, max(cos_theta, -1.0))
        return math.degrees(math.acos(cos_theta))
