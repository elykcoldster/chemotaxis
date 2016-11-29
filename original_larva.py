import numpy as np
from model import Model as m
from larva import Larva


class OriginalLarva(Larva):

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
