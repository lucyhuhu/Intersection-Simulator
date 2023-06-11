import random, math
from TrafficLight import *


class Car(object):
    def __init__(self):
        self.start, self.direction = self.randomDirection()
        self.state = 0
        self.speed = 1
        self.cx, self.cy = self.getStartPoint(self.start)
        self.turnCount = 1
        self.location = "Straight"
        self.carList = []

    def drawCar(self, canvas):
        cx, cy = self.getPlace()
        if cx >= 10 and cx <= 490 and cy >= 10 and cy <= 490:
            canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="grey")

    def getPlace(self):
        self.carList.append((self.cx, self.cy))
        return self.cx, self.cy

    def getStart(self):
        return self.start

    def getState(self):
        return self.state

    def getDirection(self):
        return self.direction

    def getLocation(self):
        return self.location

    def getSpeed(self):
        return self.speed

    def randomDirection(self):
        start = ["N", "S", "W", "E"]
        turn = ["Left", "Right", "Straight"]
        return start[random.randint(0, 3)], turn[random.randint(0, 2)]

    def getStartPoint(self, start):
        if start == "N":
            cx, cy = 225, 0
        elif start == "S":
            cx, cy = 275, 500
        elif start == "W":
            cx, cy = 0, 275
        else:
            cx, cy = 500, 225
        return cx, cy

    def move(self):
        if self.speed == 0:
            return
        cx, cy = self.cx, self.cy
        self.location = self.checkLocation()
        if self.location == "Cross":
            self.moveInCross()
        elif self.state == 0:
            dx, dy = self.moveStraight()
            self.cx, self.cy = cx + dx, cy + dy
        else:
            dx, dy = self.moveStraight()
            self.cx, self.cy = cx - dx, cy - dy

    def checkLocation(self):
        cx, cy = self.cx, self.cy
        if (cx > 200 and cx < 300) and (cy > 200 and cy < 300):
            return "Cross"
        return "Straight"

    def isAtStopLine(self):
        cx, cy = self.cx, self.cy
        return (190 < cx < 310) and (190 < cy < 310) and self.checkLocation() == "Straight"

    def moveStraight(self):
        start, speed = self.start, self.speed
        if start == "N":
            dx, dy = 0, speed
        elif start == "S":
            dx, dy = 0, -speed
        elif start == "W":
            dx, dy = speed, 0
        else:
            dx, dy = -speed, 0
        return dx, dy

    def moveInCross(self):
        if self.direction == "Right":
            self.turnRight()
        elif self.direction == "Left":
            self.turnLeft()
        else:
            location0 = self.checkLocation()
            dx, dy = self.moveStraight()
            self.cx, self.cy = self.cx + dx, self.cy + dy
            location1 = self.checkLocation()
            if self.direction == "Straight" and location0 == "Cross" and location1 == "Straight":
                self.state = 1
                start = ["N", "W", "S", "E"]
                index = start.index(self.start)
                self.start = start[index - 2]

    def turnLeft(self):
        value = int(75 * math.tan(math.pi / 12) / (1 - math.tan(math.pi / 12)))
        r = value / math.sin(math.pi / 12)
        speed = self.speed
        length = (1 / 3) * math.pi * r
        slice = (length // speed) + 1
        angle = (1 / 3) * math.pi / slice
        if self.start == "N":
            startAngle = math.pi * (13 / 12)
            cx, cy = 301 + value, 200 - value
        elif self.start == "S":
            startAngle = math.pi * (1 / 12)
            cx, cy = 200 - value, 301 + value
        elif self.start == "W":
            startAngle = math.pi * (19 / 12)
            cx, cy = 200 - value, 200 - value
        else:
            startAngle = math.pi * (7 / 12)
            cx, cy = 301 + value, 301 + value
        angle = startAngle + angle * self.turnCount
        self.cx = int(cx + r * math.cos(angle))
        self.cy = int(cy - r * math.sin(angle))
        self.turnCount += 1
        if self.turnCount >= slice:
            self.state = 1
            self.changeDirection()

    def turnRight(self):
        r = 25
        speed = self.speed
        length = 0.5 * math.pi * r
        slice = length // speed
        angle = 0.5 * math.pi / slice
        if self.start == "N":
            startAngle = 0
            cx, cy = 200, 200
        elif self.start == "S":
            startAngle = math.pi
            cx, cy = 300, 300
        elif self.start == "W":
            startAngle = math.pi * 0.5
            cx, cy = 200, 300
        else:
            startAngle = math.pi * 1.5
            cx, cy = 300, 200
        angle = startAngle - angle * self.turnCount
        self.cx = int(cx + r * math.cos(angle))
        self.cy = int(cy - r * math.sin(angle))
        self.turnCount += 1
        if self.turnCount > slice:
            self.state = 1
            self.changeDirection()

    def changeDirection(self):
        if self.direction == "Left":
            start = ["N", "W", "S", "E"]
        else:
            start = ["N", "E", "S", "W"]
        index = start.index(self.start)
        self.start = start[index - 1]

    def stopCar(self):
        self.speed = 0

    def moveCar(self):
        self.speed = 1

    def checkLight(self, isGreen):
        if self.isAtStopLine():
            if not isGreen:
                self.stopCar()
                return False
            else:
                self.moveCar()
        return True
    def stopCars(self):
        for i in range(len(self.carList)):
            x0, y0 = self.carList[i][0], self.carList[i][1]
            for (x1, y1) in self.carList[0:i]:
                d = ((x1 - x0)**2 + (y1 - y0)**2)**0.5
                if d <= 10:
                    self.stopCar()
            for (x1, y1) in self.carList[i + 1:]:
                d = ((x1 - x0)**2 + (y1 - y0)**2)**0.5
                if d <= 10:
                    self.stopCar()
