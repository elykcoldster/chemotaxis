import numpy as np
from view import View
from model import Model as m
from larva import Larva
LarvaState = Larva.LarvaState

class StatsView(View):
    def __init__(self):
        self.clear()
        self.prev_state = None

    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle, source_position):
        # If view just created, and has no previous state, don't calculate
        # anything, wait till the next update
        if self.prev_state:
            if state == LarvaState.WV_CRAWL_FWD and self.prev_state == LarvaState.WV_CRAWL_FWD_WHILE_CAST:
                # Only count a wv cast when it terminates (otherwise, it may not
                # actually resulted in a velocity change)
                self.count_wv_casts += 1
            # Calculating time of a crawl:
            if LarvaState.is_crawling(state):
                if not LarvaState.is_crawling(self.prev_state):
                    # Starting a crawl means a cast was just terminated
                    if self.cur_cast_t:
                        self.cast_times.append(self.cur_cast_t)
                    self.cur_crawl_t = 0
                else:
                    self.cur_crawl_t += m.get_instance().dt
            # Calculating time of a cast
            else:
                if LarvaState.is_crawling(self.prev_state):
                    # Starting a cast means a crawl was terminated
                    if self.cur_crawl_t:
                        self.crawl_times.append(self.cur_crawl_t)
                    self.count_head_casts += 1
                    self.cur_cast_t = 0
                else:
                    self.cur_cast_t += m.get_instance().dt

        self.prev_state = state

    def get_representation(self):
        avg_crawl_time = 0.
        if len(self.crawl_times):
            avg_crawl_time = np.mean(self.crawl_times)
        avg_cast_time = 0.
        if len(self.cast_times):
            avg_cast_time = np.mean(self.cast_times)
        count_str = '{0:15}: {1}\n'
        float_str = '{0:15}: {1:.2f}\n'
        output = count_str.format('# Head Casts', self.count_head_casts)
        output += count_str.format('# WV Casts', self.count_wv_casts)
        output += float_str.format('Avg Crawl Time', avg_crawl_time)
        output += float_str.format('Avg Cast Time', avg_cast_time)
        return output

    def draw(self):
        print(self.get_representation())

    def clear(self):
        self.count_head_casts = 0
        self.count_wv_casts = 0
        self.cur_crawl_t = 0
        self.cur_cast_t = 0
        self.crawl_times = []
        self.cast_times = []

    def export(self, path):
        with open(path, 'w') as f:
            f.write(self.get_representation())
