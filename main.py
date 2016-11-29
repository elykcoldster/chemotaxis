#import pdb
import sys
import random as rn
from controller import Controller


def main():
    controller = Controller()
    input_file = None
    if len(sys.argv) > 1:
        if sys.argv[1] == '-f':
            input_file = sys.argv[2]
        else:
            raise ValueError('Unrecognized flag')
    controller.run(input_file)

if __name__ == "__main__":
    #pdb.set_trace()
    rn.seed(1234)
    main()
