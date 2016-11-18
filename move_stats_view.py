import matplotlib.pyplot as plt
import numpy as np
from view import View

class MoveStatsView(View):
    def __init__(self):
        self.numTimeSteps = 0
        self.body_angles = []
        self.reorientation_speeds = []
        self.head_angles = []
        self.bearings = []
        self.time = 0
        
    def getAngleWithXAxis(self, unitVector):
        # dot product between i-cap and unit vector is just the x-component of unit vector
        angle = np.arccos(unitVector[0])
        # since range of arccos is [0,pi], need to correct by looking at the y-value
        if(unitVector[1] < 0):
            angle = 2*np.pi - angle
            
        # output is now in range [0, 360]
        return np.degrees(angle)
        
    def calcBodyAngle(self, velocity):
        alpha = self.getAngleWithXAxis(velocity)
        return alpha
        
    def calcBearing(self, velocity, head_loc, source_loc):
        #calculate angles of each of the vectors in consideration first
        larva_to_source = source_loc - head_loc
        body_angle = self.getAngleWithXAxis(velocity)
        source_angle = self.getAngleWithXAxis(larva_to_source/np.linalg.norm(larva_to_source))
        
        #take difference
        bearing = body_angle - source_angle
        
        #Difference is in range [-360, 360], so we bring it back to [-180, 180]
        if 360 >= bearing > 180:
            bearing = bearing - 360
        elif -360 <= bearing < -180:
            bearing = 360 + bearing
        return bearing
    
    def calcReorientationSpeed(self, prev_angle, curr_angle, dt):
        #calculate difference
        reorientation = prev_angle - curr_angle
        
        #Difference is in range [-360, 360], so we bring it back to [-180, 180]
        if 360>= reorientation > 180:
            reorientation = reorientation - 360
        elif -360 <= reorientation < -180:
            reorientation = 360 + reorientation
        
        #divide by time step to get first order approximation of differential
        return reorientation/dt
        
    def update_view(self, time, state, head_loc, joint_loc, velocity, head_angle, source_loc):
        """Save information about the movement stats of larva
        """
        
        #calculate body angle and bearing
        body_angle = self.calcBodyAngle(velocity)
        bearing = self.calcBearing(velocity, head_loc, source_loc)
        if self.numTimeSteps == 0:
            #just starting off
            self.body_angles = [body_angle]
            self.reorientation_speeds = [0]
            self.head_angles = [head_angle]
            self.bearings = [bearing]
        else:
            #calculate time step
            dt = time - self.time
            
            #get reorientation speed from previous and current body angle
            reorientation_speed = self.calcReorientationSpeed(self.body_angles[len(self.body_angles)-1], body_angle, dt)
            
            #storing the history of the larva
            self.body_angles.append(body_angle)
            self.head_angles.append(head_angle)
            self.reorientation_speeds.append(reorientation_speed)
            self.bearings.append(bearing)
        
        #updating time
        self.time = time            
        self.numTimeSteps+=1

            

    def draw(self):
        """Prints out the current view
        """
        #scatter plot of bearing versus reorientation speed
        plt.scatter(self.bearings, self.reorientation_speeds)
        plt.title('Reorientation speed vs Bearing')
        plt.xlabel('Bearing')
        plt.ylabel('Reorientation speed')        
        plt.show()

    def clear(self):
        """Discard the saved information - empty view
        """
        raise NotImplementedError

    def export(self, path):
        """Write out the view to file
        """
        raise NotImplementedError
