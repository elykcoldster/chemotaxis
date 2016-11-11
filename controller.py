from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from model import Model as m
from larva import Larva


class Controller:
    # Function dispatch table:
    command_fcns = {'a': 'add_larva',
                    'v': 'toggle_verbosity',
                    'r': 'run_model',
                    'p': 'print_larva'}

    def __init__(self):
        """Ctor, will be necessary soon
        """
        pass

    def run(self):
        """Run loop
        """
        while True:
            input_str = input('Time: {0:.1f}, Enter command: '.format(m.get_instance().time))
            inputs = deque(input_str.split())
            cmd = ''
            if len(inputs):
                cmd = inputs.popleft()
            if cmd == 'q':
                print('Quiting')
                return
            fcn_name = self.command_fcns.get(cmd)
            if not fcn_name:
                print('Invalid input')
                continue
            fcn = getattr(self, fcn_name)
            fcn(inputs)

    def add_larva(self, args):
        """Add a larva with specified characteristics
        """
        loc_x = int(args.popleft())
        loc_y = int(args.popleft())
        vel_x = int(args.popleft())
        vel_y = int(args.popleft())
        new_larva = Larva(np.array([loc_x, loc_y]), np.array([vel_x, vel_y]))
        m.get_instance().add_larva(new_larva)
        print('Added a larva: ' + str(new_larva))

    def toggle_verbosity(self, args):
        """Toggle if Larva prints on each update
        """
        for l in m.get_instance().larvae:
            l.verbose = not l.verbose

    def run_model(self, args):
        """Run specified number of iterations, or just one if no arg given
        """
        iters = 0
        if not len(args):
            iters = 1
        else:
            iters = int(args.popleft())
        print('Running ' + str(iters) + ' iteration(s)')
        for i in range(iters):
            m.get_instance().update()

    def print_larva(self, args):
        larvae = m.get_instance().larvae
        for i in range(0,len(larvae)):
            print('Larva ' + str(i + 1)
                + '\tLocation: ' + str(larvae[i].head_loc)
                + '\tVelocity: ' + str(larvae[i].velocity * larvae[i].v_fwd))
        if len(larvae) == 0:
            print('Nothing to print.')
