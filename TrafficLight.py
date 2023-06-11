from setUpBar import*

class TrafficLight(object):

  def __init__(self, isGreenAtStartOfCycle, location):
    self.transitionPoints = []
    self.upcomingTransitionIndex = 0
    self.cycleDuration = 20
    self.red, self.green = [],[]
    if isGreenAtStartOfCycle:
      self.initColor = "green"
    else:
      self.initColor = "red"
    self.cycleInitGreen = isGreenAtStartOfCycle
    self.isGreen = isGreenAtStartOfCycle
    self.location = location
    self.lastT = None
    if self.location == "N":
      self.setUpBar = setUpBar(620)
    elif self.location == "S":
      self.setUpBar = setUpBar(590)
    elif self.location == "E":
      self.setUpBar = setUpBar(560)
    else:
      self.setUpBar = setUpBar(530)
  


    
  def addTransitionPoint(self, seconds):
    if 0 < seconds < self.cycleDuration:      
      self.transitionPoints.append(seconds)
      self.transitionPoints.sort()

  def timeInCurrentCycle(self, absTime):
    return absTime % self.cycleDuration

  def updateLight(self, absTime):
    t = self.timeInCurrentCycle(absTime)
    self.setUpBar.t = t
    
    if self.lastT is None or t < self.lastT:
      self.upcomingTransitionIndex = 0
      self.isGreen = self.cycleInitGreen

    self.lastT = t
    if self.upcomingTransitionIndex == len(self.transitionPoints):
        return

    if t > self.transitionPoints[self.upcomingTransitionIndex]:
      self.isGreen = not self.isGreen
      self.upcomingTransitionIndex += 1



  def toggleInitialLight(self):
    self.cycleInitGreen = not self.cycleInitGreen

  def removeTransitionPoint(self, cycleTime):
    self.transitionPoints.pop(self.transitionPoints.find(cycleTime))
  
  def drawLight(self, canvas):
    if self.isGreen:
      color = "green"
    else:
      color = "red"

    if self.location == "N":
      canvas.create_oval(170,315,190,325, width=3, fill = color)
      canvas.create_text(160,340, text="N", font="Arial 18", fill="blue")
    elif self.location == "S":
      canvas.create_oval(310,175,330,185, width=3, fill = color)
      canvas.create_text(340,160, text="S", font="Arial 18", fill="blue")
    elif self.location == "E":
      canvas.create_oval(175,170,185,190, width=3, fill = color)
      canvas.create_text(160,160, text="E", font="Arial 18", fill="blue")
    else:
      canvas.create_oval(315,310,325,330, width=3, fill = color)
      canvas.create_text(340,340, text="W", font="Arial 18", fill="blue")
    self.setUpBar.drawBar(canvas, self.transitionPoints, self.cycleDuration, self.initColor, self.location)

  def mousePressed(self, event):
    n = self.setUpBar.mousePressed(event)
    if n is not None:
      transitionTime = n * self.cycleDuration
      for t in self.transitionPoints:
        # remove points when clicked on
        if abs(t - transitionTime) < 1:
          self.transitionPoints.remove(t)
          return None

      self.addTransitionPoint(transitionTime)

  def timerFired(self,app):
    if self.isGreen:
      self.green.append(self.location)
    else:
      self.red.append(self.location)

    


  