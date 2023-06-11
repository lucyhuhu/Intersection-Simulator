from TrafficLight import*
from cars import*

class level(object):
  allCars = {"N":[],"Npass":[],"S":[],"Spass":[],"W":[],"Wpass":[],"E":[],"Epass":[]}
  addCarInterval = None
  duration = None
  startSimulation = False
  highestPassed = 0
  penalty = 0

  def __init__(self, addCarInterval, LevelDuration):
    self.trafficLights = {}
    self.addCarInterval = addCarInterval
    self.duration = LevelDuration
    self.trafficLights["N"] = TrafficLight(False, "N")
    self.trafficLights["S"] = TrafficLight(False, "S")
    self.trafficLights["W"] = TrafficLight(False, "W")
    self.trafficLights["E"] = TrafficLight(False, "E")
  
  def addCar(self):
    newCar = Car()
    start = newCar.getStart()
    self.allCars[start].append(newCar)
  
  def passedCar(self):
    count = 0
    for carList in ["Npass","Spass","Wpass","Epass"]:
      count += len(self.allCars[carList])
    if count > self.highestPassed:
      self.highestPassed = count
    return count

  def mousePressed(self, event):
    for key in self.trafficLights:
      self.trafficLights[key].mousePressed(event)
    
  def drawCrossroad(self, canvas):
    canvas.create_rectangle(0,0,200,200, fill="white", 
                            outline="black", width=3)
    canvas.create_rectangle(300,0,500,200, fill="white", 
                            outline="black", width=3)
    canvas.create_rectangle(0,300,200,500, fill="white", 
                            outline="black", width=3)
    canvas.create_rectangle(300,300,500,500, fill="white", 
                            outline="black", width=3)
    canvas.create_line(0, 250, 500, 250, dash=(8,8), width=3)
    canvas.create_line(250, 0, 250, 500, dash=(8,8), width=3)

  def checkCars(self):
        self.checkLights()
        self.checkCarPosition()
        self.checkCarDistance()
        self.checkCarCollision()

  def checkLights(self):
    for carListKey in self.trafficLights:
      pass

  def checkCarPosition(self):
      #print("check position")
      for carList in ["N","S","W","E"]:
          for car in self.allCars[carList]:
              if car.getState() == 1:
                  self.allCars[carList].remove(car)
                  curLoc = car.getStart()
                  # print(curLoc)
                  self.allCars[curLoc+"pass"].append(car)
          
  def checkCarDistance(self):
      #print("check distance")
      for carList in ["Npass","Spass","Wpass","Epass"]:
          for car in self.allCars[carList]:
              seq = self.allCars[carList].index(car)
              resultFront = None
              if seq != 0:
                  result = self.checkFrontCar(self.allCars[carList], seq)
                  if resultFront == "Stop":
                      continue
                  elif resultFront != "Stop" and car.getSpeed() == 0:
                      car.moveCar()
      for carList in ["N","S","W","E"]:
          startIndex = 0
          if self.allCars[carList] != []:
            if self.allCars[carList][0].checkLight(self.trafficLights[carList].isGreen):
              pass
            else:
              startIndex = 1
          
          for car in self.allCars[carList][startIndex:]:
                  seq = self.allCars[carList].index(car)
                  resultFront = None
                  if seq != 0:
                      result = self.checkFrontCar(self.allCars[carList], seq)
                      if result == "Stop":
                          continue
                      elif resultFront != "Stop" and car.getSpeed() == 0:
                          car.moveCar()
                  direction = car.getDirection()
                  resultCross = None
                  if direction == "Straight" and car.getLocation() == "Cross":
                      resultCross = self.checkPassedCar(self.allCars[carList+"pass"], car)
                  elif car.getLocation() != "Cross":
                      check = ["N", "W", "S", "E"]
                      for checkList in check:
                          if checkList == car.getStart():
                            continue
                          resultCross = self.checkCrossCar(self.allCars[checkList], car)  
                  if resultCross != "Stop" and car.getSpeed() == 0:
                      car.moveCar()   
      
  
  def checkFrontCar(self, carList, seq):
      #print("check front")
      cx0, cy0 = carList[seq-1].getPlace()
      cx1, cy1 = carList[seq].getPlace()
      if abs(cx1 - cx0) <= 40 and abs(cy1 - cy0) <= 40:
          carList[seq].stopCar()
          return "Stop"

  def checkPassedCar(self, carList, car):
      #print("check pass")
      if carList == []:
          return
      cx0, cy0 = carList[-1].getPlace()
      cx1, cy1 = car.getPlace()
      if abs(cx1 - cx0) <= 40 and abs(cy1 - cy0) <= 40:
          car.stopCar()
          return "Stop"
  
  def checkCrossCar(self, carList, car):
      #print("check cross")
      for crossCar in carList:
          if crossCar.getLocation() == "Cross" and crossCar.getSpeed() != 0:
              car.stopCar()
              return "Stop"

  def checkCarCollision(self):
     for carList in ["N","S","W","E"]:
        for car in self.allCars[carList]:
          if car.getLocation() == "Cross":
             self.collision(car)
  
  def collision(self, car):
     for carList in ["N","S","W","E"]:
        if carList == car.getStart():
          continue
        for checkCar in self.allCars[carList]:
          cx0, cy0 = checkCar.getPlace()
          cx1, cy1 = car.getPlace()
          if ((cx1 - cx0) ** 2 + (cy1 - cy0) ** 2) < 80:
            self.allCars[carList].remove(checkCar)
            self.allCars[car.getStart()].remove(car)
            self.penalty += 1
  def clearCars(self):
    for carList in self.allCars:
      self.allCars[carList] = []

  
