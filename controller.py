from collections import deque
import numpy as np
from model import Model as m
from larva import Larva


class Controller:
    def run(self):
        while True:
            input_str = input('Time: ' + str(m.get_instance().time) + ', Enter command: ')
            inputs = deque(input_str.split())
            cmd = inputs.popleft()
            if cmd == 'q':
                print('Quiting')
                return
            elif cmd == 'a':
                # Add a larva with specified characteristics
                loc_x = int(inputs.popleft())
                loc_y = int(inputs.popleft())
                vel_x = int(inputs.popleft())
                vel_y = int(inputs.popleft())
                new_larva = Larva(np.array([loc_x, loc_y]), np.array([vel_x, vel_y]))
                m.get_instance().add_larva(new_larva)
                print('Added a larva: ' + str(new_larva))
            elif cmd == 'r':
                # Run specified number of iterations, or just one if no arg given
                iters = 0
                if not len(inputs):
                    iters = 1
                else:
                    iters = int(inputs.popleft())
                print('Running ' + str(iters) + ' iteration(s)')
                for i in range(iters):
                    m.get_instance().update()