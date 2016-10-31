class Model:
    def __init__(self):
        self.time = 0
        self.larvae = []
        # TODO: add other model objects and params (arena, etc)
    
    def add_larva(self, l):
        self.larvae.append(l)

    def update(self):
        """Increment the time and tell all objects to update themselves"""
        for l in larvae:
            l.update() # TODO: pass probabilities as arguments to larva's update
        # TODO: update the three probabilities
        time = time + 1
