from enum import Enum
import random as rn
import math
import numpy as np
from model import Model as m
from sim_object import SimObject


class NewLarva(SimObject):

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
        
        @staticmethod
        def is_crawling(state):
            if (state == NewLarva.LarvaState.CRAWL_FWD or
                state == NewLarva.LarvaState.WV_CRAWL_FWD or
                state == NewLarva.LarvaState.WV_CRAWL_FWD_WHILE_CAST or
                state == NewLarva.LarvaState.WV_CHANGE_CAST_DIR):
                return True
            return False

    def p_run_term_new(self):
        lda = 1/(1+np.exp(-(self.g0+self.g1*self.y)))
        return lda*m.get_instance().dt

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

    def p_cast_term_new(self):
        # need to define a good measure for cast termination using the IFB+IFF motif
        lda = 1/(1+np.exp(-(self.g2+self.g3*self.y)))
        return lda*m.get_instance().dt

    def p_cast_term(self):
        r = self.cast_term_base
        dt = m.get_instance().dt
        if len(self.history) > 1:
            term_time = np.minimum(len(self.history) * dt, self.t_cast_term)
            for t in np.arange(0,term_time,dt):
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

        p_wv = self.wv_term_base
        t_wv_long_avg = self.t_wv_long_avg
        t_wv_short_avg = self.t_wv_short_avg
        k_wv_mult = self.k_wv_mult

        dt = m.get_instance().dt
        if len(self.history) > 1:
            term_time = np.minimum(len(self.history) * dt, t_wv_short_avg + t_wv_long_avg)
            for t in np.arange(0, term_time, dt):
                tsteps = int(t/dt)
                C = self.history[len(self.history) - tsteps - 1]
                C_prev = self.history[len(self.history) - tsteps - 2]

                phi = 0

                if len(self.history) - tsteps - 2 >= 0:
                    phi = (np.log(C) - np.log(C_prev))/dt;

                # assuming multiplicative factor of 30 until we go t_short_avg steps back
                # assuming multiplicative factor of -30 in range [t_short_avg, t_short_avg+t_long_avg]
                # all these kernels don't make sense in a few cases because the probabilities
                # might go below 0 or above 1 in certain cases
                kernel = k_wv_mult if t <= t_wv_short_avg else -1*k_wv_mult
                p_wv += kernel*phi

        return m.get_instance().dt * p_wv

    def p_wv_cast_resume(self):
        r_wv_cast_resume = self.r_wv_cast_resume
        return m.get_instance().dt * r_wv_cast_resume

    def perceive(self):
        return m.get_instance().get_arena().concentration_at_loc(self.head_loc)


    def crawl_fwd(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: CRAWL FWD')
        if m.get_instance().time - self.run_start_time > self.t_min_run:
            self.state = NewLarva.LarvaState.WV_CRAWL_FWD
        else:
            self.move_forward()

    def wv(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: WEATHERVANE PSEUDO-STATE')
        if self.state == NewLarva.LarvaState.WV_CRAWL_FWD:
            self.wv_crawl_fwd(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == NewLarva.LarvaState.WV_CRAWL_FWD_WHILE_CAST:
            self.wv_crawl_fwd_while_cast(
                p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)
        elif self.state == NewLarva.LarvaState.WV_CHANGE_CAST_DIR:
            self.wv_change_cast_dir(p_run_term, p_cast_term,
                               p_wv, p_wv_cast_resume, rand)
        if rand < p_run_term:
            # Note: If we terminate a run while in the middle of weathervane casting, we DO NOT
            # modify the velocity to point in the direction of the weathervane cast
            self.state = NewLarva.LarvaState.CAST_START

    def wv_crawl_fwd(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: WV CRAWL FWD')
        self.move_forward()
        if rand < p_wv_cast_resume:
            # Pick a random cast direction? (need to confirm that this is the right thing to do)
            self.cast_dir = np.sign(rand - 0.5)
            self.state = NewLarva.LarvaState.WV_CRAWL_FWD_WHILE_CAST

    def wv_crawl_fwd_while_cast(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: WV CRAWL FWD WHILE CAST')
        self.rotate_weathervane_cast()
        self.move_forward()
        if rand < p_wv:
            # When weathervaning stops, the velocity is updated
            self.update_velocity()
            self.state = NewLarva.LarvaState.WV_CRAWL_FWD
        else:
            if self.get_head_angle() > self.wv_theta_max:
                self.state = NewLarva.LarvaState.WV_CHANGE_CAST_DIR

    def wv_change_cast_dir(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: WV CHANGE CAST DIR')
        self.cast_dir *= -1
        self.state = NewLarva.LarvaState.WV_CRAWL_FWD_WHILE_CAST

    def cast_start(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: CAST START')
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
        while self.cast_dir == 0:
            self.cast_dir = np.sign(rand - 0.5)
        self.state = NewLarva.LarvaState.CAST_TURN

    def cast_turn(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: CAST TURN')
        self.rotate_normal_cast()
        if self.get_head_angle() > self.theta_min:
            self.state = NewLarva.LarvaState.CAST_TURN_AFTER_MIN_ANGLE

    def cast_turn_after_min_angle(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: CAST TURN AFTER MIN ANGLE')
        self.rotate_normal_cast()
        if rand < p_cast_term:
            # Cast termination results in a new velocity vector
            self.update_velocity()
            self.run_start_time = m.get_instance().time
            self.state = NewLarva.LarvaState.CRAWL_FWD
        else:
            if self.get_head_angle() > self.theta_max:
                self.cast_dir *= -1
                self.state = NewLarva.LarvaState.CAST_TURN_TO_MIDDLE

    def cast_turn_to_middle(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: CAST TURN TO MIDDLE')
        self.rotate_normal_cast()
        if abs(self.get_head_angle()) < self.cast_epsilon:
            self.state = NewLarva.LarvaState.CAST_TURN_RANDOM_DIR

    def cast_turn_random_dir(self, p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand):
        self.larva_print('State: CAST TURN RANDOM DIR')
        self.cast_dir = np.sign(rand - 0.5)
        self.state = NewLarva.LarvaState.CAST_TURN

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

    def __init__(self, location, velocity, head_length=1, theta_max=120.0, theta_min=37, cast_speed=240, wv_theta_max=20, wv_cast_speed=60, v_fwd=1.0, t_min_run=1, run_term_base=0.148, cast_term_base=2, wv_term_base=2, wv_cast_resume=1, t_run_term=20, t_cast_term=0.5, r_wv_cast_resume = 1, t_wv_long_avg = 10, t_wv_short_avg = 1, k_wv_mult = 30):
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
        self.k_run_term = np.arange(2, -2, -4*m.get_instance().dt/t_run_term)
        # cast termination time and kernel
        self.t_cast_term = t_cast_term
        self.k_cast_term = np.arange(0, 150, 150*m.get_instance().dt/t_cast_term) # may need piecewise kernel later

        # weathervane parameters
        self.r_wv_cast_resume = r_wv_cast_resume
        self.t_wv_long_avg = t_wv_long_avg
        self.t_wv_short_avg = t_wv_short_avg
        self.k_wv_mult = k_wv_mult
        # init perceptual history array
        self.history = []
        # init larva state (crawl forward)
        self.run_start_time = m.get_instance().time
        self.state = NewLarva.LarvaState.CRAWL_FWD
        self.verbose = False
		
        self.g0 = -0.8156
        self.g1 = -0.011
        self.g2 = 0.8
        self.g3 = 0.045

        self.a1 = 0.13
        self.a2 = 0.26
        self.a3 = 1.1
        self.b1 = 2903.36
        self.b2 = 0.01
        self.b3 = 2.65
        self.b4 = 795.62
        self.b5 = 23.79
        self.theta = 1.88
        self.n = 2
        self.u = 0
        self.y = 0

    def update_osn(self, n):
        x = self.perceive()
        n = self.n
        a1 = self.a1
        a2 = self.a2
        a3 = self.a3
        b1 = self.b1
        b2 = self.b2
        b3 = self.b3
        b4 = self.b4
        b5 = self.b5
        theta = self.theta
        dt = m.get_instance().dt
        for i in range(0, n):
            u = self.u
            y = self.y
            du = a1*x - a2*u + a3*y
            dy = b1*x/(b2 + x + b3*u) - b4*np.power(y,n)/(np.power(theta,n) + np.power(y,n))-b5*y
            self.u += du * dt / n
            self.y += dy * dt / n

    def update(self):
        """Update larva state based on transition probabilities
        """
        # print('Updating a larva')
        # Generate a random number for probabilistic events
        rand = rn.random()  # TODO: seed random in main function instead of here
        # Perceive the surrounding world and calculate probabilities here:
        self.update_osn(20)
        p_run_term = self.p_run_term_new()
        p_cast_term = self.p_cast_term()
        p_wv = self.p_wv()
        p_wv_cast_resume = self.p_wv_cast_resume()

        #print(p_cast_term)

        self.history.append(self.perceive())

        fcn_name = self.state_fcns.get(self.state)
        if not fcn_name:
            raise ValueError("Not a valid Larva State!")
        fcn = getattr(self, fcn_name)
        fcn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)

        m.get_instance().notify_state(self.state, self.head_loc, self.joint_loc, self.velocity, self.get_head_angle())

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
        self.correct_wall_collision()

    def move_forward(self):
        distance = m.get_instance().dt * self.v_fwd  # TODO: set dt in Model
        self.head_loc = self.head_loc + distance * self.velocity
        self.joint_loc = self.joint_loc + distance * self.velocity
        self.correct_wall_collision()
    
    def update_velocity(self):
        """Set velocity to be in the direction of vector from joint to head
        """
        new_vel = self.head_loc - self.joint_loc
        self.velocity = new_vel / np.linalg.norm(new_vel)

    # TODO: Add a signed head angle function as well
    def get_head_angle(self):
        """Get absolute angle of head with respect to the midline (velocity vector)
        """
        head_vec = self.head_loc - self.joint_loc # joint is origin
        cos_theta = np.dot(head_vec, self.velocity) / (np.linalg.norm(head_vec) * np.linalg.norm(self.velocity))
        # We have to clamp the cosine angle because of rounding errors (an issue when the two vectors point in the same direction)
        cos_theta = min(1.0, max(cos_theta, -1.0))
        return math.degrees(math.acos(cos_theta))

    def correct_wall_collision(self):
        head_x = self.head_loc[0]
        head_y = self.head_loc[1]
        origin_head_x = head_x - self.joint_loc[0]
        origin_head_y = head_y - self.joint_loc[1]
        arena = m.get_instance().get_arena()
        head_update = None
        # If out of bounds rotate the head to be aligned with the arena wall
        if head_x <= arena.x_min or head_x >= arena.x_max:
            if origin_head_y == 0:
                # if the collision was "head on" (exactly perpendicular),
                # redirect the head towards the side with more room, away from 
                # other walls
                wall_range = arena.y_max - arena.y_min
                head_vert_dist = (head_y - arena.y_min) / wall_range
                head_update = np.array([0, -1]) if head_vert_dist >= 0.5 else np.array([0, 1])
            else:
                head_update = np.array([0, 1]) if origin_head_y > 0 else np.array([0, -1])
        elif head_y <= arena.y_min or head_y >= arena.y_max:
            if origin_head_x == 0:
                wall_range = arena.x_max - arena.x_min
                head_horiz_dist = (head_x - arena.x_min) / wall_range
                head_update = np.array([-1, 0]) if head_horiz_dist >= 0.5 else np.array([1, 0])
            else:
                head_update = np.array([1, 0]) if origin_head_x >= 0 else np.array([-1, 0])
        else:
            # Wasn't out of bounds
            return
        old_head_loc = self.head_loc
        self.head_loc = self.joint_loc + head_update
        if self.get_head_angle() > 90:
            self.head_loc = old_head_loc
            head_update = np.dot(-1, head_update)
            self.head_loc = self.joint_loc + head_update
        self.update_velocity()
        # If it was casting, restart the cast
        if not NewLarva.LarvaState.is_crawling(self.state):
            self.state = NewLarva.LarvaState.CAST_START

    def larva_print(self, msg):
        if self.verbose:
            print(msg)

    def __str__(self):
        # TODO: Maybe output more things about the larva like current state,
        # head angle, etc
        return ('Location: ' + str(self.head_loc) + '\tVelocity: '
                + str(self.velocity * self.v_fwd))
