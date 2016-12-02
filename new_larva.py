import random as rn
import numpy as np
from larva import Larva
from model import Model as m
from sim_object import SimObject


class NewLarva(Larva):

    def p_run_term(self):
        lda = 1/(1+np.exp(-(self.g0+self.g1*self.y)))
        return lda*m.get_instance().dt

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
        self.state = Larva.LarvaState.CRAWL_FWD
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
        p_run_term = self.p_run_term()
        p_cast_term = self.p_cast_term()
        p_wv = self.p_wv()
        p_wv_cast_resume = self.p_wv_cast_resume()

        #print(m.get_instance().get_arena().base_concentration())

        self.history.append(self.perceive())

        fcn_name = self.state_fcns.get(self.state)
        if not fcn_name:
            raise ValueError("Not a valid Larva State!")
        fcn = getattr(self, fcn_name)
        fcn(p_run_term, p_cast_term, p_wv, p_wv_cast_resume, rand)

        m.get_instance().notify_state(self.state, self.head_loc, self.joint_loc, self.velocity, self.get_head_angle())
    def __str__(self):
        return ('Location: ' + str(self.head_loc) + '\tVelocity: '
                + str(self.velocity * self.v_fwd))