from controller import Controller

class Model:
    control = None
    limit_x = 24
    limit_y = 24

    object_x = 13
    object_y = 7

    def __init__(self):
        self.control = Controller()

    def restart(self):
        self.object_x = 0
        self.object_y = 0

    def get_state(self):
        x = self.control.est_x
        if (x > self.limit_x or x < self.limit_x * -1):
            x = self.limit_x + 1 #error state
        y = self.control.est_y
        if (y > self.limit_y or y < self.limit_y * -1):
            y = self.limit_y + 1 #error state
        angle = (int) (self.control.getAngle()/90.0+0.5)
        return (x, y, angle)

    def is_done(self):
        return self.control.est_x == self.object_x and self.control.est_y == self.object_y

    def calc_dist(self):
        return (self.object_x - self.control.est_x)**2+(self.object_y - self.control.est_y)**2

    def step(self, action):
        if (action == 0):
            #doing nothing is getting punished
            return -2
        elif (action == 1):
            dist_before = self.calc_dist()
            self.control.goForward(1)
            dist_after = self.calc_dist()
            if (dist_before > dist_after):
                #got closer to the goal
                return 10
            elif (dist_before < dist_after):
                #got further away from goal
                return -10
            else:
                return -1
        elif (action == 2):
            self.control.turnRight()
            #too much useless turning gets punished
            return -1
        elif (action == 3):
            self.control.turnLeft()
            #too much useless turning gets punished
            return -1
        else:
            print "Error ocurred! Wrong action number!"
            # being a dumb idiot who doesn't read the documentation gets punished
            return -100