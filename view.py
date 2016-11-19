import util

class View:
    """Abstract View Class
    """
    def __init__(self):
        raise NotImplementedError(util.abstract_class_except_msg)

    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle, source_position):
        """Save information about the larva
        """
        raise NotImplementedError(util.abstract_class_except_msg)

    def draw(self):
        """Prints out the current view
        """
        raise NotImplementedError(util.abstract_class_except_msg)

    def clear(self):
        """Discard the saved information - empty view
        """
        raise NotImplementedError(util.abstract_class_except_msg)

    def export(self, path):
        """Write out the view to file
        """
        raise NotImplementedError(util.abstract_class_except_msg)
