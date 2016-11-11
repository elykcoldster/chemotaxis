from collections import deque
import numpy as np
from model import Model as m
from larva import Larva
from view_factory import view_factory

class Controller:
    # Function dispatch table:
    command_fcns = {'a': 'add_larva',
                    'v': 'toggle_verbosity',
                    'r': 'run_model',
                    'p': 'print_larva',
                    'av': 'attach_view',
                    'd': 'draw_view',
                    'e': 'export_view'}

    def __init__(self):
        self.all_views = {}

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

    def attach_view(self, args):
        """Attach a specified view to the Model
        """
        view_type = args.popleft()
        if self.all_views.get(view_type):
            print('View already attached!')
            return
        view = view_factory(view_type)
        if not view:
            return # TODO: Broken record: replace with exceptions
        m.get_instance().attach(view)
        self.all_views[view_type] = view

    def draw_view(self, args):
        """
        """
        view_type = args.popleft()
        if view_type == 'all':
            # Draw all the views
            for v in self.all_views.values():
                v.draw()
        else:
            # Draw just the specified view
            view = self.all_views.get(view_type)
            if not view:
                # TODO: Use exception handling instead of this
                print('Not an attached view!')
                return
            view.draw()

    def export_view(self, args):
        """
        """
        view_type = args.popleft()
        path = args.popleft()
        view = self.all_views.get(view_type)
        if not view:
            # TODO: Use exception handling, that will remove copy-pasted code
            # like this
            print('Not an attached view!')
            return
        view.export(path)

