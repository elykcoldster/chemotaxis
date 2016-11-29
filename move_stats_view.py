import matplotlib.pyplot as plt
import numpy as np
from view import View
from larva import Larva

class MoveStatsView(View):
    def __init__(self):
        self.numTimeSteps = 0
        self.body_angles = []
        self.reorientation_speeds = []
        self.head_angles = []
        self.bearings = []
        
        #stores 0 if no turn, 1 if left turn, -1 if right turn
        self.isTurn = []
        
        #parameters used for turn detection
        self.time = 0
        self.TURN_REORIENTATION_SPEED = 12
        
        #parameters used for run length histogram calculation
        self.runLengths = []
        self.currRunLength = 0
        
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
        bearing = source_angle - body_angle
        
        #Difference is in range [-360, 360], so we bring it back to [-180, 180]
        if 360 >= bearing > 180:
            bearing = bearing - 360
        elif -360 <= bearing < -180:
            bearing = 360 + bearing
        return bearing
    
    def calcReorientationSpeed(self, body_angles, dt):
        total_reorientation = 0;
        num_samples = int(1/dt);
        for i in range(len(body_angles) - num_samples, len(body_angles)):
            if i < 1:
                break
            #calculate difference
            reorientation = body_angles[i] - body_angles[i-1]
            
            #Difference is in range [-360, 360], so we bring it back to [-180, 180]
            if 360>= reorientation > 180:
                reorientation = reorientation - 360
            elif -360 <= reorientation < -180:
                reorientation = 360 + reorientation
            total_reorientation += reorientation
        #divide by time step to get first order approximation of differential
        return total_reorientation
        
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
            self.isTurn = [0]
        else:
            #calculate time step
            dt = time - self.time
            
            #get reorientation speed from previous and current body angle
            reorientation_speed = self.calcReorientationSpeed(self.body_angles, dt)
            
            #update turn statistics
            self.updateTurns(reorientation_speed, time, dt)
                
            self.updateRunStats(state, dt)
            
            #storing the history of the larva
            self.body_angles.append(body_angle)
            self.head_angles.append(head_angle)
            self.reorientation_speeds.append(reorientation_speed)
            self.bearings.append(bearing)
        
        #updating time
        self.time = time            
        self.numTimeSteps+=1
    
    def updateRunStats(self, state, dt):
        if state in [Larva.LarvaState.CRAWL_FWD, Larva.LarvaState.WV_CRAWL_FWD, Larva.LarvaState.WV_CRAWL_FWD_WHILE_CAST]:
            self.currRunLength += dt
        else:
            if self.currRunLength > 0:
                self.runLengths.append(self.currRunLength)
                self.currRunLength = 0
    
    def updateTurns(self, reorientation_speed, time, dt):
        #storing which direction the larva is turning
        turnDirection = 0
        if abs(reorientation_speed) > self.TURN_REORIENTATION_SPEED:            
            if reorientation_speed > 0:
                turnDirection = 1
            else:
                turnDirection = -1

        self.isTurn.append(turnDirection)

    def draw(self):
        """Prints out the current view
        """
        plt.figure()
        #scatter plot of bearing versus reorientation speed
        plt.subplot(221)
        plt.scatter(self.bearings, self.reorientation_speeds)
        plt.title('Reorientation speed vs Bearing')
        plt.xlabel('Bearing')
        plt.ylabel('Reorientation speed')  
        
        plt.subplot(222)
        bearingFreqs = []
        for i in range(len(self.bearings)):
            bearing = self.bearings[i]
            if self.isTurn[i]==1:
                bearingFreqs.append(bearing)
        
        plt.hist(bearingFreqs, bins = 12, normed=True)
        plt.title('Probability Left Turn vs Bearing')
        plt.xlabel('Bearing')
        plt.ylabel('Left turn frequency')
        
        plt.subplot(223)
        plt.hist(self.runLengths, bins = 5)
        plt.title('Run Length Histogram')
        plt.xlabel('Run lengths (s)')
        plt.ylabel('Proportion of runs')
        plt.tight_layout()
        plt.show()

    def clear(self):
        """Discard the saved information - empty view
        """
        raise NotImplementedError

    def export(self, path):
        """Write out the view to file
        """
        raise NotImplementedError
