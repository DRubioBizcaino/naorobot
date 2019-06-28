#import naoqi
#import qi#there are too many ways to use naoqi and every part of the documentation tells you something different
from naoqi import ALProxy
from numpy import argwhere
from time import sleep

class Controller:
    
    ip = "127.0.0.1"
    port = 9559

    #session = None
    motion = None
    posture = None

    #variables for position workaround
    est_x = 0 #chess coordinates
    est_y = 0 #amount of seconds walked in that direction multplied by the speed percentage
    est_orientation = 'n' #north, south, east, west as char
    
    def __init__(self):
        #self.session = qi.Session()
        #try:
        #    self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        #except RuntimeError:
        #    print ("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port))
        #    sys.exit(1)
        #posture_service = self.session.service("ALRobotPosture")
        #posture_service.goToPosture("StandInit", 1.0)
        self.motion = ALProxy("ALMotion", self.ip, self.port)
        self.posture = ALProxy("ALRobotPosture", self.ip, self.port)
        self.posture.goToPosture("StandInit", 1.0)

    def update_position(self, distance):
        """simple workaround to get chess coordinates"""
        if(self.est_orientation == 'n'):
            self.est_y += distance
        elif(self.est_orientation == 's'):
            self.est_y -= distance
        elif(self.est_orientation == 'e'):
            self.est_x += distance
        elif(self.est_orientation == 'w'):
            self.est_x -= distance
 
    def update_rotation(self, angle):#positive angle = counterclockwise
        """simple workaround to get chess coordinates"""
        if(self.est_orientation == 'n'):
            if(angle>0):
                self.est_orientation = 'w'
            else:
                self.est_orientation = 'e'
        elif(self.est_orientation == 's'):
            if(angle>0):
                self.est_orientation = 'e'
            else:
                self.est_orientation = 'w'
        elif(self.est_orientation == 'e'):
            if(angle>0):
                self.est_orientation = 'n'
            else:
                self.est_orientation = 's'
        elif(self.est_orientation == 'w'):
            if(angle>0):
                self.est_orientation = 's'
            else:
                self.est_orientation = 'n'

    def getPosition(self):
        return self.est_x * 1.0, self.est_y *1.0

    def getAngle(self):
        if(self.est_orientation == 'n'):
            return 0.0
        elif(self.est_orientation == 's'):
            return 180.0
        elif(self.est_orientation == 'e'):
            return 270.0
        elif(self.est_orientation == 'w'):
            return 90.0

    def goForward(self, time, speed = 1.0):
        self.motion.moveToward(1.0, 0.0, 0.0, [["Frequency", speed]])
        stepsize = 5
        sleep(time * stepsize)
        self.motion.stopMove()
        self.update_position(time*speed)

    def turnRight(self):
        self.motion.moveToward(0.0, 0.0, -1.0, [["Frequency", 1.0]])
        sleep(4.5)
        self.motion.stopMove()
        self.update_rotation(-90)

    def turnLeft(self):
        self.motion.moveToward(0.0, 0.0, 1.0, [["Frequency", 1.0]])
        sleep(4.5)
        self.motion.stopMove()
        self.update_rotation(90)

    def test_move(self):
        self.turnLeft()
        self.turnRight()
        self.goForward(1)
    
    
if(__name__ == "__main__"):
    con = Controller()
    con.test_move()
