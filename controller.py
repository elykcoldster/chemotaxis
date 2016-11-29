from collections import deque
import numpy as np
from model import Model as m
from larva import Larva
from new_larva import NewLarva
from arena import Arena
from disperse_arena import DisperseArena
from view_factory import view_factory
from util import Error

class Controller:
    # Function dispatch table:
    # TODO: modify the 'p' = 'print_larva' function to be a command that
    # prints descriptions of ALL simulation objects.
    command_fcns = {'a': 'add_larva',
                    'an': 'add_new_larva',
                    'ar': 'add_arena',
                    'ad': 'add_disperse_arena',
                    'v': 'toggle_verbosity',
                    'r': 'run_model',
                    'p': 'print_larva',
                    'av': 'attach_view',
                    'd': 'draw_view',
                    'e': 'export_view'}

    def __init__(self):
        self.all_views = {}

    def run(self, input_file):
        """Run loop
        """
        input_from_file = deque()
        # Get any input given from file
        if input_file:
            input_from_file = deque([line.rstrip('\n') for line in open(input_file)])

        while True:
            try:
                input_str = ''
                # First read any commands given from a file, then begin to
                # take user input
                if len(input_from_file):
                    input_str = input_from_file.popleft()
                else:
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
                    raise Error('Invalid input!')
                    continue
                fcn = getattr(self, fcn_name)
                fcn(inputs)
            except Error as err:
                print(err)
            except:
                print('Unexpected error!')
                raise

    def add_larva(self, args):
        """Add a larva with specified characteristics
        """
        loc_x = float(args.popleft())
        loc_y = float(args.popleft())
        vel_x = float(args.popleft())
        vel_y = float(args.popleft())
        new_larva = Larva(np.array([loc_x, loc_y]), np.array([vel_x, vel_y]))
        m.get_instance().add_larva(new_larva)
        print('Added a larva: ' + str(new_larva))

    def add_new_larva(self, args):
        """Add a larva with specified characteristics
        """
        loc_x = float(args.popleft())
        loc_y = float(args.popleft())
        vel_x = float(args.popleft())
        vel_y = float(args.popleft())
        new_larva = NewLarva(np.array([loc_x, loc_y]), np.array([vel_x, vel_y]))
        m.get_instance().add_larva(new_larva)
        print('Added a larva: ' + str(new_larva))

    def add_arena(self, args):
        loc_x = float(args.popleft())
        loc_y = float(args.popleft())
        strength = float(args.popleft())
        decay_rate = float(args.popleft())
        new_arena = Arena(source_position=np.array([loc_x, loc_y]), source_strength=strength, source_decay_rate=decay_rate)
        m.get_instance().add_arena(new_arena)
        print('Added Arena: ' + str(new_arena))
    
    def add_disperse_arena(self, args):
        loc_x = float(args.popleft())
        loc_y = float(args.popleft())
        strength = float(args.popleft())
        sigma = float(args.popleft())
        new_arena = DisperseArena(source_position=np.array([loc_x, loc_y]), source_strength=strength, sigma=sigma)
        m.get_instance().add_arena(new_arena)
        print('Added Arena: ' + str(new_arena))

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
            print('Larva {0} {1}'.format(i + 1, larvae[i]))
        if len(larvae) == 0:
            print('Nothing to print.')

    def get_attached_view(self, view_type_str):
        """Helper function that retreives an already attached view

        Throws an error if the view is not attached.
        """
        view = self.all_views.get(view_type_str)
        if not view:
            raise Error('Not an attached view!')
        return view

    def attach_view(self, args):
        """Attach a specified view to the Model

        Example:
            'av ArenaView'
        """
        view_type = args.popleft()
        if self.all_views.get(view_type):
            raise Error('View already attached!')
        view = view_factory(view_type)
        m.get_instance().attach(view)
        self.all_views[view_type] = view

    def draw_view(self, args):
        """Draw a specific view (or all views)

        Example:
            'd ArenaView'
            or
            'd all'
        """
        view_type = args.popleft()
        if view_type == 'all':
            # Draw all the views
            for v in self.all_views.values():
                v.draw()
        else:
            # Draw just the specified view
            view = self.get_attached_view(view_type)
            view.draw()

    def export_view(self, args):
        """Export the specified view to a file

        Example:
            'e TableView tableAsFile.txt'
        """
        view_type = args.popleft()
        path = args.popleft()
        view = self.get_attached_view(view_type)
        view.export(path)
