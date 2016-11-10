from view import View
from tabulate import tabulate

class TableView(View):
    def __init__(self):
        self.header = ["Time", "State", "Head Location", "Joint Location", "Velocity", "Head Angle"]
        self.table = []

    def update_view(self, time, state_str, head_loc, joint_loc, velocity, head_angle):
        self.data.append([time, state_str, head_loc, joint_loc, velocity, head_angle])
        
    def draw(self):
        print(tabulate(self.table, headers=self.header))

    def clear(self):
        self.table.clear()

    def export(self, path):
        with open(path, 'w') as f:
            f.write(tabulate(self.table, headers=self.header))
