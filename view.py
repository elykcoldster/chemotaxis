abstract_class_except_msg = "Concrete class must implement abstract method"

class View:
    """Abstract View Class
    """
    def __init__(self):
        raise NotImplementedError(abstract_class_except_msg)

    def update_view(self, time, state_str, head_loc, joint_loc, velocity, head_angle):
        """Save information about the larva
        """
        raise NotImplementedError(abstract_class_except_msg)

    def draw(self):
        """Prints out the current view
        """
        raise NotImplementedError(abstract_class_except_msg)

    def clear(self):
        """Discard the saved information - empty view
        """
        raise NotImplementedError(abstract_class_except_msg)

    def export(self, path):
        """Write out the view to file
        """
        raise NotImplementedError(abstract_class_except_msg)
