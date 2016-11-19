import util

class SimObject():
    """Abstract Simulation Object Class
    """
    def __init__(self):
        raise NotImplementedError(util.abstract_class_except_msg)

    def update(self):
        """Update state
        """
        raise NotImplementedError(util.abstract_class_except_msg)

    def __str__(self):
        """Provide string description of current object state
        """
        raise NotImplementedError(util.abstract_class_except_msg)