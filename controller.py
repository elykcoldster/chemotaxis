from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from model import Model as m
from larva import Larva
from arena_view import ArenaView


class Controller:
    def run(self):
        while True:
            input_str = input('Time: {0:.1f}, Enter command: '.format(m.get_instance().time))
            inputs = deque(input_str.split())
            if len(inputs) == 0:
                cmd = ''
            else:
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
            elif cmd == 's':
                # Run specified number of iterations, or just one if no arg given (no prints)
                iters = 0
                if not len(inputs):
                    iters = 1
                else:
                    iters = int(inputs.popleft())
                for i in range(iters):
                    m.get_instance().update(False)
            elif cmd == 'p':
                larvae = m.get_instance().larvae
                for i in range(0,len(larvae)):
                    print('Larva ' + str(i + 1)
                        + '\tLocation: ' + str(larvae[i].head_loc)
                        + '\tVelocity: ' + str(larvae[i].velocity * larvae[i].v_fwd))
                if len(larvae) == 0:
                    print('Nothing to print.')
            elif cmd == 'av':
                # TODO: this has been moved into arena_view.py
                # The code has been left here for reference. To be deleted
                # after implementation in arena_view.py
                arena_view = ArenaView()
                m.get_instance().attach(arena_view)
            elif cmd == 'd':
                for index, view in enumerate(m.get_instance().views):
                    plt.figure(index)
                    view.draw()
                plt.show()
            elif cmd == 'e':
                if not len(inputs):
                    print('Input a filename (without extension)')
                else:
                    for view in m.get_instance().views:
                        view.export(inputs.popleft())
            else:
                print('Invalid Input')