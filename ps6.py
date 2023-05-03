print("\033c")

import math
import random

import ps6_visualize
import pylab


# helper
class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
      # changes position in 1 time mark 
      # assumes new position is within room
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
# end helper




# base characteristics of room, with methods for tracking clean/not, 
# & keeping within bounds of room
class RectangularRoom(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[False for _ in range(height)] for _ in range(width)]
    
    def cleanTileAtPosition(self, pos):
        x = int(pos.getX())
        y = int(pos.getY())
        self.tiles[x][y] = True

    def isTileCleaned(self, x, y):
        return self.tiles[x][y]
    
    def getNumTiles(self):
        NumTiles = self.width * self.height
        return NumTiles
         
    def getNumCleanedTiles(self):
        return sum(sum(row) for row in self.tiles)

    def getRandomPosition(self):
        x = random.uniform(0.1, self.width)
        y = random.uniform(0.1, self.height)
        pos = Position(x, y)
        return pos

    def isPositionInRoom(self, pos):
        x = pos.getX()
        y = pos.getY()
        return 0 <= x < self.width and 0 <= y < self.height




# basic robot class structure to define base characteristics such as position, speed, etc
class Robot(object):
    def __init__(self, room, speed):
        self.room = room
        self.speed = speed
        self.position = None
        self.direction = None

    def getRobotPosition(self):
       return self.position

    def getRobotDirection(self):
        return self.direction

    def setRobotPosition(self, position):
        self.position = position

    def setRobotDirection(self, direction):
        self.direction = direction

    def updatePositionAndClean(self):
        # abstraction method of movement + cleaning
        raise NotImplementedError



class StandardRobot(Robot):
    # standard movement at set speed in current direction
    # changes direction if hits a wall
    # updates to new position and cleans single tile
    def updatePositionAndClean(self):
        InitialPos = self.position
        NewPos = InitialPos.getNewPosition(self.direction, self.speed)
        while self.room.isPositionInRoom(NewPos) == False:
            self.direction = random.randint(0, 360)
            NewPos = InitialPos.getNewPosition(self.direction, self.speed)
        self.position = NewPos
        self.room.cleanTileAtPosition(self.position)

class RandomWalkRobot(Robot):
    # standard movement at set speed in current direction
    # changes direction at every time step
    # updates to new position and cleans single tile
    def updatePositionAndClean(self):
        InitialPos = self.position
        self.direction = (random.randint(0, 360))
        NewPos = InitialPos.getNewPosition(self.direction, self.speed)
        while self.room.isPositionInRoom(NewPos) == False:
            self.direction = random.randint(0, 360)
            NewPos = InitialPos.getNewPosition(self.direction, self.speed)
        self.position = NewPos
        self.room.cleanTileAtPosition(self.position)



# simulation of robot cleaning with x number trials. 
# also can watch the animation if you want :)
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    
    Times = []
    for i in range(num_trials):
        # initialize room
        MyHouse = RectangularRoom(width, height)
        # anim = ps6_visualize.RobotVisualization(num_robots, width, height)

        # initialize robots with position and direction
        MyRoombas = []
        for j in range(num_robots):
            MyRoomba = robot_type(MyHouse, speed)
            StartingPoint = MyHouse.getRandomPosition()
            while MyHouse.isPositionInRoom(StartingPoint) == False:
                StartingPoint = MyHouse.getRandomPosition()
            MyRoomba.setRobotPosition(StartingPoint)
            MyRoomba.setRobotDirection(random.randint(0, 360))
            MyRoombas.append(MyRoomba)

        # start cleaning til she clean enough!
        # also the robots are so high tech that they can pass through each other without crashing.. lol
        FracClean = 0
        time = 0
        while FracClean < min_coverage:
            for item in MyRoombas:
                item.updatePositionAndClean()

            # anim.update(MyHouse, MyRoombas)    
            time += 1
            FracClean = MyHouse.getNumCleanedTiles() / MyHouse.getNumTiles()
        Times.append(time)
        # print(f'She clean! and it only took {time} times!')

    AveTime = sum(Times) / len(Times)

    print(f'On average {num_robots} {robot_type}s at speed {speed} take {AveTime} time to clean {min_coverage} of room.')

    # makes fun cleaning animation-- dont recommend for more than a few trials :)
    # anim.done()

    return AveTime

# runSimulation(5, 5, 10, 10, .8, 20, RandomWalkRobot)



# How long does it take to clean 80% of a 20�20 room with each of 1-10 robots?
def showPlot1():
    NumRobots = []
    Times = []
    for i in range (1, 11):
        time = runSimulation(i, 1, 20, 20, .8, 20, StandardRobot)
        Times.append(time)
        NumRobots.append(i)

    pylab.figure(1)
    pylab.plot(NumRobots, Times)
    pylab.title('Number of Robots vs Cleaning Time, for a 20x20 room')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Time to Clean')
    pylab.show()



# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20�20, 25�16, 40�10, 50�8, 80�5, and 100�4?
def showPlot2():
    Sizes = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    Times = []
    Ratios = []
    for tuple in Sizes:
        Ratio = tuple[0]/tuple[1]
        Ratios.append(Ratio)
        time = runSimulation(2, 1, tuple[0], tuple[1], .8, 500, StandardRobot)
        Times.append(time)

    pylab.figure(2)
    pylab.plot(Ratios, Times)
    pylab.title('Width/Height Ratio vs Cleaning Time, for a Standard Room Area')
    pylab.xlabel('Width/Height Ratio')
    pylab.ylabel('Time to Clean')
    pylab.show()



# comparison of randomwalk robot vs standard, at 80% of a 20x20 room
def showPlot3():

    # standard robot data
    NumSRobots = []
    STimes = []
    for i in range (1, 11):
        time = runSimulation(i, 1, 20, 20, .8, 20, StandardRobot)
        STimes.append(time)
        NumSRobots.append(i)

    # randomwalk robot data
    NumRRobots = []
    RTimes = []
    for i in range (1, 11):
        time = runSimulation(i, 1, 20, 20, .8, 20, RandomWalkRobot)
        RTimes.append(time)
        NumRRobots.append(i)

    pylab.figure(3)
    pylab.plot(NumSRobots, STimes, 'bo-', label = 'Standard Robot')
    pylab.plot(NumRRobots, RTimes, 'rx-', label = 'RandomWalk Robot')
    
    pylab.title('Number of Robots vs Cleaning Time, for a 20x20 room')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Time to Clean')
    pylab.legend()
    pylab.show()



showPlot1()
showPlot2()
showPlot3()