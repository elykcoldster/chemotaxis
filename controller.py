from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from model import Model as m
from larva import Larva


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
            elif cmd == 'v':
                larva = m.get_instance().larvae[0]
                path = larva.path
                head_locs = []
                joint_locs = []
                for i in range(0,len(path)):
                    if len(head_locs) == 0:
                        head_locs = [path[i][0:2]]
                        joint_locs = [path[i][2:4]]
                    else:
                        head_locs = np.append(head_locs,[path[i][0:2]],axis = 0)
                        joint_locs = np.append(joint_locs,[path[i][2:4]],axis = 0)
                plt.plot(head_locs[:,0],head_locs[:,1],'b',linewidth=3)
                plt.plot(joint_locs[:,0],joint_locs[:,1],'r',linewidth=2)
                plt.title('Larva Trajectory')
                plt.xlabel('x position')
                plt.ylabel('y position')

                #axis_min = np.minimum(np.amin(head_locs[:,0]), np.amin(head_locs[:,1]))
                #axis_max = np.maximum(np.amax(head_locs[:,0]), np.amax(head_locs[:,1]))
                #plt.axis([axis_min, axis_max, axis_min, axis_max])
                plt.gca().set_aspect('equal', adjustable='box')
                plt.show()
            else:
                print('Invalid Input')