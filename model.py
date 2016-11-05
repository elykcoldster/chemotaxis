class Model:
    # A reference to the singleton object
    __instance = None

    def __init__(self):
        """Model ctor, not meant to be called by the user

        By convention, always call get_instance() when you want a valid
        reference to the singleton Model. Never call the constructor
        explicitly.
        """
        # TODO: provide methods to set these to different values later
        self.time = 0
        self.dt = 0.1
        self.larvae = []
        # TODO: add other model objects and params (arena, etc)
    
    @staticmethod
    def get_instance():
        if not Model.__instance:
            Model.__instance = Model()
        return Model.__instance

    def add_larva(self, l):
        self.larvae.append(l)

    def update(self):
        """Increment the time and tell all objects to update themselves"""
        for l in larvae:
            l.update()
        time = time + 1